import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("R.SECURITY.EVAL_PARSE", r"eval\s*\(\s*parse\s*\(", "eval(parse(...)) executes arbitrary code"),
    ("R.SECURITY.SYSTEM", r"\bsystem\(", "system() command execution; validate inputs"),
    ("R.SECURITY.HTTP", r"\"http://", "Insecure HTTP URL"),
    ("R.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*<-\s*['\"][^'\"]+['\"]", "Hardcoded secret"),
    ("R.QUALITY.ATTACH", r"\battach\s*\(", "attach() pollutes search path"),
    ("R.QUALITY.GLOBAL_ASSIGN", r"<<-", "Global assignment <<- (hidden side effects)"),
    ("R.PERF.NESTED_LOOP", r"for\s*\(.+?\)\s*\{[\s\S]*for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class REngine(EngineBase):
    language = "r"
    extensions = (".r", ".R")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\b(\w+)\s*<-\s*function\s*\(", src))
        complexity = float(len(re.findall(r"\b(if|for|while|tryCatch)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = REngine()
