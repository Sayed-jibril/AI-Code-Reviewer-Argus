# server/engines/c_cpp.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    # Security issues
    ("C.SECURITY.BUFFER_OVERFLOW", r"strcpy\s*\(", "strcpy can cause buffer overflow; use strncpy"),
    ("C.SECURITY.STRCAT", r"strcat\s*\(", "strcat can cause buffer overflow; use strncat"),
    ("C.SECURITY.SPRINTF", r"sprintf\s*\(", "sprintf can cause buffer overflow; use snprintf"),
    ("C.SECURITY.GETS", r"gets\s*\(", "gets is unsafe; use fgets"),
    ("C.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("C.SECURITY.MEMCPY", r"memcpy\s*\([^,]+,\s*[^,]+,\s*[^)]*\)", "Check memcpy bounds"),
    ("C.SECURITY.FREE", r"free\s*\(\s*[^)]+\s*\)", "Ensure pointer is not used after free"),
    
    # C++ specific security
    ("CPP.SECURITY.CIN", r"cin\s*>>\s*\w+", "cin can cause buffer overflow; use getline"),
    ("CPP.SECURITY.STRING_COPY", r"\.copy\s*\([^,]+,\s*[^,]+,\s*[^)]*\)", "Check string copy bounds"),
    
    # Memory management
    ("C.MEMORY.LEAK", r"malloc\s*\([^)]*\)", "Ensure malloc result is freed"),
    ("C.MEMORY.NULL_CHECK", r"malloc\s*\([^)]*\)\s*;", "Check malloc return for NULL"),
    ("CPP.MEMORY.NEW", r"new\s+\w+", "Ensure new allocation is deleted"),
    ("CPP.MEMORY.DELETE", r"delete\s+[^;]+;", "Check for double delete"),
    
    # Performance issues
    ("C.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?for\s*\(", "Nested loop (possible O(n^2)+)"),
    ("C.PERF.STRLEN_IN_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?strlen\s*\(", "strlen in loop (performance)"),
    
    # Quality issues
    ("C.QUALITY.MAGIC_NUMBER", r"\b\d{4,}\b", "Magic number detected"),
    ("C.QUALITY.GOTO", r"\bgoto\s+\w+", "Avoid goto statements"),
    ("C.QUALITY.BROAD_CATCH", r"catch\s*\(\s*\.\.\.\s*\)", "Catching all exceptions"),
    ("CPP.QUALITY.USING_NAMESPACE", r"using\s+namespace\s+std", "Avoid using namespace std"),
    ("CPP.QUALITY.COUT", r"cout\s*<<", "Consider using printf for performance"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class CCppEngine(EngineBase):
    language = "c/c++"
    extensions = (".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx")

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
        
        # Count functions (C and C++ style)
        c_functions = len(re.findall(r"\w+\s+\w+\s*\([^)]*\)\s*{", source))
        cpp_functions = len(re.findall(r"\w+\s*::\s*\w+\s*\([^)]*\)\s*{", source))
        functions = c_functions + cpp_functions
        
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = CCppEngine()
