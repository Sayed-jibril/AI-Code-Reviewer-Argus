import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("PS.SECURITY.INVOKE_EXPRESSION", r"\bInvoke-Expression\b", "Invoke-Expression executes strings; validate inputs"),
    ("PS.SECURITY.PLAIN_HTTP", r"\"http://", "Use HTTPS"),
    ("PS.SECURITY.SECRET", r"(ApiKey|Secret|Password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("PS.QUALITY.WRITE_HOST", r"\bWrite-Host\b", "Prefer Write-Output or logging"),
    ("PS.PERF.NESTED_LOOP", r"for\s*\(.+?\)\s*\{[\s\S]*?for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class PowerShellEngine(EngineBase):
    language = "powershell"
    extensions = (".ps1", ".psm1")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bfunction\b\s+\w+", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|switch)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = PowerShellEngine()
