import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("M.SECURITY.SYSTEM", r"\bsystem\s*\(", "system() command execution; validate inputs"),
    ("M.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret"),
    ("M.QUALITY.CLEAR_ALL", r"\bclear\s+all\b", "clear all nukes workspace"),
    ("M.PERF.NESTED_LOOP", r"for\s+.*\s*[\r\n]+[\s\S]*for\s+", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class MatlabEngine(EngineBase):
    language = "matlab"
    extensions = (".m",)

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        # Heuristic guard: if it looks like a C header, skip (to avoid .m header conflicts)
        if re.search(r"#\s*include\s*<", src):
            return [], {"functions": 0, "complexity": 0.0}
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bfunction\b\s+\[?.*?\]?\s*=\s*\w+\s*\(", src))
        complexity = float(len(re.findall(r"\b(if|for|while|try|catch|case)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = MatlabEngine()
