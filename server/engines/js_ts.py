# server/engines/js_ts.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

# Heuristic patterns for JS/TS risks & smells
_PATTERNS = [
    ("JS.SECURITY.EVAL", r"\beval\s*\(", "Use of eval() is dangerous"),
    ("JS.SECURITY.FUNCTION_CONSTRUCTOR", r"new\s+Function\s*\(", "Function constructor is dangerous"),
    ("JS.SECURITY.INNERHTML", r"\.innerHTML\s*=", "Direct innerHTML assignment (XSS risk)"),
    ("JS.SECURITY.DOCUMENT_WRITE", r"document\.write\s*\(", "document.write can be unsafe"),
    ("JS.SECURITY.LOCATION_HREF", r"location\.href\s*=\s*[^;]+", "Unvalidated redirect via location.href"),
    ("JS.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("JS.SECURITY.MD5", r"\bmd5\s*\(", "MD5 is weak; prefer stronger hashes"),
    ("JS.PERF.DOM_QUERY_IN_LOOP", r"for\s*\([\s\S]*?\)\s*{[\s\S]*?document\.querySelector", "DOM queries inside loop (performance)"),
    ("JS.QUALITY.VAR", r"\bvar\s+", "Use 'let' or 'const' instead of 'var'"),
    ("TS.QUALITY.ANY", r":\s*any\b", "Usage of 'any' weakens type safety"),
    ("JS.QUALITY.EQ", r"[^=!]==[^=]|[^=!]!=[^=]", "Prefer strict equality (=== / !==)"),
    ("JS.QUALITY.BROAD_CATCH", r"catch\s*\(\s*\w*\s*\)\s*{", "Check for overly broad catch without handling"),
    ("JS.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?for\s*\(", "Nested loop (possible O(n^2)+)"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class JsTsEngine(EngineBase):
    language = "javascript/typescript"
    extensions = (".js", ".jsx", ".ts", ".tsx")

    def analyze(self, path: str, source: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, source, re.IGNORECASE | re.MULTILINE):
                ln = _line_of(source, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(
                    id=f"{rule}.{ln}",
                    ruleId=rule,
                    title=title,
                    severity=sev, filePath=path,
                    lineStart=ln, lineEnd=ln,
                    confidence=0.6,
                    tags=["security"] if "SECURITY" in rule else ["pattern"]
                ))
        # Simple metrics
        functions = len(re.findall(r"\bfunction\b|\b=>\s*{", source))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = JsTsEngine()
