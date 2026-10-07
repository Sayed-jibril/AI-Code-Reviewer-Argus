import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("SWIFT.SECURITY.INSECURE_HASH", r"MD5\(", "MD5 is weak; prefer SHA256"),
    ("SWIFT.SECURITY.EVAL", r"NSExpression\s*\(", "Dynamic eval-like usage; validate inputs"),
    ("SWIFT.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("SWIFT.SECURITY.URL_STRING", r"URL\s*\(\s*string\s*:\s*\"http://", "Insecure HTTP URL"),
    ("SWIFT.QUALITY.FORCE_UNWRAP", r"!\b", "Force unwrap (!) may crash; use safe optional handling"),
    ("SWIFT.QUALITY.TRY!", r"try!", "Force try may crash; handle errors explicitly"),
    ("SWIFT.PERF.NESTED_LOOP", r"for\s+.*\{\s*for\s+", "Nested loop (possible O(n^2)+)"),
    ("SWIFT.QUALITY.EMPTY_CATCH", r"catch\s*\{\s*\}", "Empty catch block"),
]

def _line(text, idx): return text[:idx].count("\n") + 1

class SwiftEngine(EngineBase):
    language = "swift"
    extensions = (".swift",)

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bfunc\b\s+\w+\s*\(", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case|guard)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = SwiftEngine()
