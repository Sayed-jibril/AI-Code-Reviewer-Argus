import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("BASH.SECURITY.USETMP", r"/tmp/", "Use of /tmp; ensure safe mktemp and permissions"),
    ("BASH.SECURITY.EVAL", r"\beval\s", "eval executes arbitrary strings"),
    ("BASH.SECURITY.CURL_HTTP", r"curl\s+http://", "Insecure HTTP download"),
    ("BASH.SECURITY.SUDO", r"\bsudo\s", "Ensure least-privilege usage"),
    ("BASH.QUALITY.SET_E", r"^\s*set\s+-e\b", "Consider 'set -euo pipefail' for safety"),
    ("BASH.PERF.USE_XARGS", r"for\s+\w+\s+in\s+\$\(.+\)", "Use xargs/find -print0 for performance/robustness"),
]

def _line(t, i): return t[:i].count("\n") + 1

class BashEngine(EngineBase):
    language = "bash"
    extensions = (".sh", ".bash")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else "info"
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\b\w+\s*\(\)\s*\{", src))
        complexity = float(len(re.findall(r"\b(if|for|while|case)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = BashEngine()
