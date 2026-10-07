# server/engines/java.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    ("JAVA.SECURITY.SQL_CONCAT", r"Statement\s+\w+\s*=\s*conn\.createStatement\(\)[\s\S]*?\"[^\"]*\+\s*\w+", "SQL concatenation; use PreparedStatement"),
    ("JAVA.SECURITY.MD5", r"MessageDigest\.getInstance\(\s*\"MD5\"\s*\)", "MD5 is weak; use SHA-256"),
    ("JAVA.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret"),
    ("JAVA.QUALITY.EMPTY_CATCH", r"catch\s*\(\s*\w+\s+\w+\s*\)\s*{(\s*//.*|\s*)}", "Empty catch block"),
    ("JAVA.QUALITY.BROAD_CATCH", r"catch\s*\(\s*Exception\s+\w+\s*\)\s*{", "Catching base Exception"),
    ("JAVA.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?for\s*\(", "Nested loop (possible O(n^2)+)"),
    ("JAVA.QUALITY.SYSOUT", r"System\.out\.println\(", "Excessive System.out.println (logging hygiene)"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class JavaEngine(EngineBase):
    language = "java"
    extensions = (".java",)

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
        functions = len(re.findall(r"\b(public|private|protected)\s+\w[\w<>\[\]]*\s+\w+\s*\([^)]*\)\s*{", source))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = JavaEngine()
