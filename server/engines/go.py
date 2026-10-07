# server/engines/go.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    # Security issues
    ("GO.SECURITY.SQL_INJECTION", r"db\.Query\s*\(\s*\"[^\"]*\+\s*\w+", "SQL injection risk; use parameterized queries"),
    ("GO.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("GO.SECURITY.CMD_INJECTION", r"exec\.Command\s*\(\s*[^,]+,\s*[^)]*\+\s*\w+", "Command injection risk"),
    ("GO.SECURITY.UNSAFE_POINTER", r"unsafe\.Pointer", "Unsafe pointer usage"),
    ("GO.SECURITY.CRYPTO_RAND", r"math/rand", "Use crypto/rand for cryptographic operations"),
    
    # Performance issues
    ("GO.PERF.SLICE_APPEND", r"append\s*\([^,]+,\s*[^)]*\)", "Check slice capacity for append operations"),
    ("GO.PERF.NESTED_LOOP", r"for\s+[^{]*{[\s\S]*?for\s+", "Nested loop (possible O(n^2)+)"),
    ("GO.PERF.GOROUTINE_LEAK", r"go\s+func\s*\([^)]*\)\s*{", "Ensure goroutines are properly managed"),
    ("GO.PERF.CHANNEL_LEAK", r"make\s*\(\s*chan\s+", "Ensure channels are properly closed"),
    
    # Quality issues
    ("GO.QUALITY.ERROR_IGNORE", r"_\s*=\s*[^;]+\.Error\s*\(\s*\)", "Error is being ignored"),
    ("GO.QUALITY.UNUSED_IMPORT", r"import\s+[^)]+", "Check for unused imports"),
    ("GO.QUALITY.MAGIC_NUMBER", r"\b\d{4,}\b", "Magic number detected"),
    ("GO.QUALITY.PANIC", r"panic\s*\(", "Avoid panic in production code"),
    ("GO.QUALITY.GOTO", r"goto\s+\w+", "Avoid goto statements"),
    ("GO.QUALITY.GLOBAL_VAR", r"var\s+\w+\s+[^=]+$", "Consider avoiding global variables"),
    
    # Go-specific patterns
    ("GO.STYLE.IF_ERR", r"if\s+err\s*!=\s*nil\s*{", "Check error handling pattern"),
    ("GO.STYLE.DEFER", r"defer\s+[^;]+", "Ensure defer is used appropriately"),
    ("GO.STYLE.INTERFACE", r"interface\s*{[^}]*}", "Check interface design"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class GoEngine(EngineBase):
    language = "go"
    extensions = (".go",)

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
        
        # Count functions (Go style)
        functions = len(re.findall(r"func\s+\w+\s*\([^)]*\)", source))
        complexity = float(len(re.findall(r"\b(if|for|switch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = GoEngine()
