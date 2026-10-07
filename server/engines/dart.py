import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("DART.SECURITY.INSECURE_HTTP", r"\"http://", "Use HTTPS"),
    ("DART.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("DART.QUALITY.PRINT", r"\bprint\s*\(", "Excessive print logging"),
    ("DART.QUALITY.BROAD_CATCH", r"catch\s*\(\s*\w*\s*\)", "Broad catch; check handling"),
    ("DART.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class DartEngine(EngineBase):
    language = "dart"
    extensions = (".dart",)

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\b(\w+\s+)?\w+\s*\([^)]*\)\s*\{", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = DartEngine()
