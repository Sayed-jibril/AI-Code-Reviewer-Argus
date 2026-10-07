import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("PERL.SECURITY.EVAL", r"\beval\s+['\"]", "eval on strings is dangerous"),
    ("PERL.SECURITY.BACKTICKS", r"`[^`]+`", "Shell backticks; command injection risk"),
    ("PERL.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=>?\s*['\"][^'\"]+['\"]", "Hardcoded secret"),
    ("PERL.QUALITY.GLOBAL", r"our\s+\$", "Global variable (our)"),
    ("PERL.PERF.NESTED_LOOP", r"for\s*\(.+?\)\s*\{[\s\S]*for\s*\(", "Nested loop"),
]

def _line(t, i): return t[:i].count("\n") + 1

class PerlEngine(EngineBase):
    language = "perl"
    extensions = (".pl", ".pm")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"\bsub\b\s+\w+", src))
        complexity = float(len(re.findall(r"\b(if|for|while)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = PerlEngine()
