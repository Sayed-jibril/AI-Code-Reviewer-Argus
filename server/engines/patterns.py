import re
from typing import List
from ..models import Issue

_PATTERNS = [
    ("PY.SECURITY.EVAL", r"\beval\s*\(", "Use of eval() is dangerous"),
    ("PY.SECURITY.EXEC", r"\bexec\s*\(", "Use of exec() is dangerous"),
    ("GEN.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("PY.SECURITY.PICKLE", r"\bpickle\.loads\s*\(", "Untrusted pickle.loads can be unsafe"),
    ("GEN.SECURITY.MD5", r"\bmd5\s*\(", "MD5 is weak; prefer SHA-256"),
    ("GEN.SECURITY.SQL", r"(SELECT|UPDATE|DELETE|INSERT)\s+.+\s+FROM\s+", "Raw SQL string detected (check for injection)"),
]

def analyze_text(path: str, text: str) -> List[Issue]:
    issues: List[Issue] = []
    for rule, pat, title in _PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line = text[:m.start()].count("\n") + 1
            issues.append(Issue(
                id=f"{rule}.{line}",
                ruleId=rule,
                title=title,
                severity="security" if "SECURITY" in rule else "warning",
                filePath=path,
                lineStart=line,
                lineEnd=line,
                codeFrame=None,
                confidence=0.6,
                tags=["security"] if "SECURITY" in rule else ["pattern"]
            ))
    return issues
