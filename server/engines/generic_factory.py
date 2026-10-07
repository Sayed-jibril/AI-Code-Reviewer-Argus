# server/engines/generic_factory.py
import re
from typing import List, Dict, Tuple, Iterable
from ..models import Issue
from .base import EngineBase

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class GenericRegexEngine(EngineBase):
    """
    Parameterized regex-based engine. Provide:
    - language: str
    - extensions: tuple of extensions
    - patterns: list of (ruleId, regex, title, severity_tag['security'|'perf'|'info'|'warning'])
    - func_regex: regex string to count functions (heuristic)
    - complexity_tokens: list[str] of control words to estimate complexity
    """
    def __init__(
        self,
        language: str,
        extensions: Tuple[str, ...],
        patterns: List[Tuple[str, str, str, str]],
        func_regex: str,
        complexity_tokens: Iterable[str]
    ):
        self.language = language
        self.extensions = extensions
        self._patterns = patterns
        self._func_re = re.compile(func_regex, re.IGNORECASE | re.MULTILINE) if func_regex else None
        self._cx_tokens = list(complexity_tokens) if complexity_tokens else []

    def analyze(self, path: str, source: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title, sev_tag in self._patterns:
            for m in re.finditer(pat, source, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                ln = _line_of(source, m.start())
                if sev_tag == "security":
                    sev = "security"
                elif sev_tag == "perf":
                    sev = "warning"
                elif sev_tag == "error":
                    sev = "error"
                else:
                    sev = "info" if sev_tag == "info" else "warning"
                issues.append(Issue(
                    id=f"{rule}.{ln}",
                    ruleId=rule,
                    title=title,
                    severity=sev,
                    filePath=path,
                    lineStart=ln,
                    lineEnd=ln,
                    confidence=0.6,
                    tags=["security"] if sev == "security" else (["performance"] if sev_tag=="perf" else ["pattern"])
                ))
        funcs = 0
        if self._func_re:
            funcs = len(self._func_re.findall(source))
        cx = 1.0
        if self._cx_tokens:
            token_re = re.compile(r"\b(" + "|".join(map(re.escape, self._cx_tokens)) + r")\b", re.IGNORECASE)
            cx = float(len(token_re.findall(source)) + 1)
        return issues, {"functions": int(funcs), "complexity": cx}
