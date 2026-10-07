import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("SCALA.SECURITY.SQL_CONCAT", r"Statement\s*\(|createStatement\(\)[\s\S]*\"[^\"]*\+\s*\w+", "SQL concatenation; use prepared statements"),
    ("SCALA.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("SCALA.QUALITY.MUTABLE_VAR", r"\bvar\b", "Prefer immutable 'val' over 'var'"),
    ("SCALA.QUALITY.BROAD_CATCH", r"case\s*_:\s*Throwable", "Catching all Throwables"),
    ("SCALA.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class ScalaEngine(EngineBase):
    language = "scala"
    extensions = (".scala",)

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bdef\b\s+\w+\s*\(", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = ScalaEngine()
