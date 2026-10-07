import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("KT.SECURITY.SQL_CONCAT", r"Statement\s*\(|createStatement\(\)[\s\S]*\"[^\"]*\+\s*\w+", "SQL concatenation; use prepared statements"),
    ("KT.SECURITY.MD5", r"MessageDigest\.getInstance\(\s*\"MD5\"", "MD5 is weak; use SHA-256"),
    ("KT.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("KT.SECURITY.INSECURE_HTTP", r"\"http://", "Use HTTPS"),
    ("KT.QUALITY.GLOBAL_VAR", r"\bvar\s+\w+\s*=\s*.+\s*\n", "Global mutable state"),
    ("KT.QUALITY.BROAD_CATCH", r"catch\s*\(\s*Exception", "Catching base Exception"),
    ("KT.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class KotlinEngine(EngineBase):
    language = "kotlin"
    extensions = (".kt", ".kts")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bfun\b\s+\w+\s*\(", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|when)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = KotlinEngine()
