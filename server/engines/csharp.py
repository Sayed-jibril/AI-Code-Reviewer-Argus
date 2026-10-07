# server/engines/csharp.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("CS.SECURITY.SQL_CONCAT", r"SqlCommand\s*\(\s*\"[^\"]*\+\s*\w+", "SQL concatenation; use parameters"),
    ("CS.SECURITY.MD5", r"MD5\.Create\(", "MD5 is weak; use SHA256"),
    ("CS.SECURITY.RNG", r"new\s+Random\s*\(", "Random() is not cryptographically secure"),
    ("CS.SECURITY.SECRET", r"(ApiKey|Secret|Password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("CS.QUALITY.EMPTY_CATCH", r"catch\s*\(\s*\w*\s*\)\s*{(\s*//.*|\s*)}", "Empty catch block"),
    ("CS.QUALITY.BROAD_CATCH", r"catch\s*\(\s*Exception\s*\w*\)\s*{", "Catching base Exception"),
    ("CS.QUALITY.DISPOSE", r"new\s+SqlConnection\(", "Ensure IDisposable is disposed (using)"),
    ("CS.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?for\s*\(", "Nested loop (possible O(n^2)+)"),
    ("CS.QUALITY.ASYNC_VOID", r"async\s+void\s+\w+\s*\(", "Avoid async void (except event handlers)"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class CSharpEngine(EngineBase):
    language = "csharp"
    extensions = (".cs",)

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
        functions = len(re.findall(r"\b(\w+\s+)+\w+\s*\([^)]*\)\s*{", source))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = CSharpEngine()
