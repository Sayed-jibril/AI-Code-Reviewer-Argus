import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("OBJC.SECURITY.INSECURE_HTTP", r"@\"http://", "Use HTTPS"),
    ("OBJC.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*@\"[^\"]+\"", "Hardcoded secret"),
    ("OBJC.SECURITY.NSSTRING_FMT", r"\[NSString stringWithFormat:@\".*%s", "Potential format string issues"),
    ("OBJC.QUALITY.NSLOG", r"NSLog\s*\(", "Excessive NSLog (leaks info)"),
    ("OBJC.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loop"),
    ("OBJC.QUALITY.EMPTY_CATCH", r"@catch\s*\(\s*NSException\s*\*\s*\w+\s*\)\s*\{\s*\}", "Empty catch block"),
]

def _line(t, i): return t[:i].count("\n") + 1

class ObjCEngine(EngineBase):
    language = "objective-c"
    extensions = (".m", ".mm")

    def analyze(self, path: str, src: str) -> Tuple[List[Issue], Dict[str, float]]:
        issues: List[Issue] = []
        for rule, pat, title in _PATTERNS:
            for m in re.finditer(pat, src, re.IGNORECASE | re.MULTILINE):
                ln = _line(src, m.start())
                sev = "security" if "SECURITY" in rule else ("warning" if "PERF" in rule else "info")
                issues.append(Issue(id=f"{rule}.{ln}", ruleId=rule, title=title,
                                    severity=sev, filePath=path, lineStart=ln, lineEnd=ln,
                                    confidence=0.6, tags=["security"] if "SECURITY" in rule else ["pattern"]))
        funcs = len(re.findall(r"[-+]\s*\([^)]*\)\s*\w+\s*:", src)) + len(re.findall(r"[-+]\s*\([^)]*\)\s*\w+\s*\{", src))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case|@try|@catch)\b", src, re.IGNORECASE)) + 1)
        return issues, {"functions": funcs, "complexity": complexity}

ENGINE = ObjCEngine()
