import ast
from typing import List, Tuple, Dict
from ..models import Issue

class _ComplexityCounter(ast.NodeVisitor):
    def __init__(self):
        self.score = 1
    def visit_If(self, node): self.score += 1; self.generic_visit(node)
    def visit_For(self, node): self.score += 1; self.generic_visit(node)
    def visit_While(self, node): self.score += 1; self.generic_visit(node)
    def visit_Try(self, node): self.score += 1; self.generic_visit(node)
    def visit_BoolOp(self, node): self.score += 1; self.generic_visit(node)
    def visit_With(self, node): self.score += 1; self.generic_visit(node)

def _code_frame(source: str, start: int, end: int, pad: int = 3) -> str:
    lines = source.splitlines()
    a = max(1, start - pad); b = min(len(lines), end + pad)
    out = []
    for i in range(a, b + 1):
        out.append(f"{i}: {lines[i-1]}")
    return "\n".join(out)

def analyze_python_file(path: str, source: str) -> Tuple[List[Issue], Dict[str, float], List[str]]:
    issues: List[Issue] = []
    tags: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        issues.append(Issue(
            id="PY.SYNTAX.ERROR",
            ruleId="PY.SYNTAX.ERROR",
            title=f"Syntax error: {e.msg}",
            severity="error",
            filePath=path,
            lineStart=e.lineno or 1,
            lineEnd=e.lineno or 1,
            codeFrame=_code_frame(source, e.lineno or 1, e.lineno or 1),
            confidence=0.95,
            tags=["syntax"]
        ))
        return issues, {"complexity": 0.0, "functions": 0}, tags

    assigned: Dict[str, List[int]] = {}
    used: Dict[str, List[int]] = {}
    imports: Dict[str, int] = {}
    import_used: Dict[str, bool] = {}

    loop_depth = 0
    max_loop_depth = 0
    functions = 0
    total_complexity = 0

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            nonlocal functions, total_complexity
            functions += 1
            # Mutable default args
            for i, default in enumerate(node.args.defaults):
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(Issue(
                        id=f"PY.AST.MUTABLE_DEFAULT.{node.name}.{i}",
                        ruleId="PY.AST.MUTABLE_DEFAULT",
                        title=f"Function '{node.name}' uses a mutable default argument",
                        severity="error",
                        filePath=path,
                        lineStart=node.lineno,
                        lineEnd=node.end_lineno or node.lineno,
                        codeFrame=_code_frame(source, node.lineno, node.end_lineno or node.lineno),
                        confidence=0.9,
                        tags=["bug"]
                    ))
            # Complexity
            cc = _ComplexityCounter()
            cc.visit(node)
            total_complexity += cc.score
            self.generic_visit(node)

        def visit_Assign(self, node: ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    assigned.setdefault(t.id, []).append(node.lineno)
            self.generic_visit(node)

        def visit_Name(self, node: ast.Name):
            if isinstance(node.ctx, ast.Load):
                used.setdefault(node.id, []).append(node.lineno)
            self.generic_visit(node)

        def visit_Import(self, node: ast.Import):
            for alias in node.names:
                imports[alias.asname or alias.name] = node.lineno
                import_used[alias.asname or alias.name] = False

        def visit_ImportFrom(self, node: ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                imports[name] = node.lineno
                import_used[name] = False

        def visit_ExceptHandler(self, node: ast.ExceptHandler):
            # Broad except: except: or except Exception:
            if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
                issues.append(Issue(
                    id=f"PY.AST.BROAD_EXCEPT.{node.lineno}",
                    ruleId="PY.AST.BROAD_EXCEPT",
                    title="Broad exception handler",
                    severity="warning",
                    filePath=path,
                    lineStart=node.lineno,
                    lineEnd=node.end_lineno or node.lineno,
                    codeFrame=_code_frame(source, node.lineno, node.end_lineno or node.lineno),
                    confidence=0.85,
                    tags=["reliability"]
                ))

        def visit_For(self, node: ast.For):
            nonlocal loop_depth, max_loop_depth
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
            self.generic_visit(node)
            loop_depth -= 1

        def visit_While(self, node: ast.While):
            nonlocal loop_depth, max_loop_depth
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
            self.generic_visit(node)
            loop_depth -= 1

    Visitor().visit(tree)

    # Detect unused variables
    for name, lines in assigned.items():
        if name.startswith("_"):  # ignore intentionally unused
            continue
        if name not in used:
            l = lines[0]
            issues.append(Issue(
                id=f"PY.AST.UNUSED_VAR.{name}.{l}",
                ruleId="PY.AST.UNUSED_VAR",
                title=f"Unused variable '{name}'",
                severity="info",
                filePath=path,
                lineStart=l,
                lineEnd=l,
                codeFrame=_code_frame(source, l, l),
                confidence=0.8,
                tags=["style"]
            ))

    # Track import usage (simple heuristic by token match)
    for name in list(used.keys()):
        if name in import_used:
            import_used[name] = True
    for name, line in imports.items():
        if not import_used.get(name, False):
            issues.append(Issue(
                id=f"PY.AST.UNUSED_IMPORT.{name}.{line}",
                ruleId="PY.AST.UNUSED_IMPORT",
                title=f"Unused import '{name}'",
                severity="info",
                filePath=path,
                lineStart=line,
                lineEnd=line,
                codeFrame=_code_frame(source, line, line),
                confidence=0.8,
                tags=["style"]
            ))

    # Nested loop heuristic
    if max_loop_depth >= 2:
        issues.append(Issue(
            id=f"PY.PERF.NESTED_LOOPS",
            ruleId="PY.PERF.NESTED_LOOPS",
            title=f"Nested loop depth = {max_loop_depth} (possible O(n^2)+ hotspot)",
            severity="warning",
            filePath=path,
            lineStart=1,
            lineEnd=max(1, source.count('\n') + 1),
            codeFrame=None,
            confidence=0.7,
            tags=["performance","complexity"]
        ))

    avg_complexity = (total_complexity / max(functions, 1))
    metrics = {"complexity": float(avg_complexity), "functions": functions}
    return issues, metrics, tags
