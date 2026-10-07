import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

# Note: This flags smells in .sql scripts, not in host languages.
_PATTERNS = [
    ("SQL.SECURITY.DDL_DROP", r"\bDROP\s+TABLE\b", "Potentially destructive DDL (DROP TABLE)"),
    ("SQL.SECURITY.GRANT_ALL", r"\bGRANT\s+ALL\b", "Overly broad GRANT"),
    ("SQL.QUALITY.SELECT_STAR", r"\bSELECT\s+\*\b", "SELECT * harms performance/clarity"),
    ("SQL.PERF.MISSING_WHERE", r"\bDELETE\s+FROM\s+\w+\s*;|\bUPDATE\s+\w+\s+SET\s+[^;]+;", "DELETE/UPDATE without WHERE"),
    ("SQL.PERF.NO_INDEX_HINT", r"\bWHERE\b\s+\w+\s*=\s*[^;]+", "Check indexing on filtered columns"),
]

def _line(t, i): return t[:i].count("\n") + 1

class SqlEngine(EngineBase):
    language = "sql"
    extensions = (".sql",)

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        # Metrics are less meaningful for SQL; provide minimal values
        return issues, {"functions": 0, "complexity": float(len(issues))}

ENGINE = SqlEngine()
