# server/engines/rust.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    # Security issues
    ("RUST.SECURITY.UNSAFE", r"unsafe\s*{", "Unsafe block detected"),
    ("RUST.SECURITY.UNSAFE_FN", r"unsafe\s+fn", "Unsafe function detected"),
    ("RUST.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("RUST.SECURITY.UNWRAP", r"\.unwrap\s*\(\s*\)", "unwrap() can panic; use proper error handling"),
    ("RUST.SECURITY.EXPECT", r"\.expect\s*\(\s*['\"][^'\"]*['\"]\s*\)", "expect() can panic; use proper error handling"),
    ("RUST.SECURITY.UNCHECKED", r"unchecked_", "Unchecked operation detected"),
    
    # Memory safety
    ("RUST.MEMORY.CLONE", r"\.clone\s*\(\s*\)", "Unnecessary clone() detected"),
    ("RUST.MEMORY.COPY", r"\.copy\s*\(\s*\)", "Unnecessary copy() detected"),
    ("RUST.MEMORY.BORROW", r"&\s*mut\s+\w+", "Mutable borrow detected"),
    ("RUST.MEMORY.BOX", r"Box::new", "Box allocation detected"),
    
    # Performance issues
    ("RUST.PERF.NESTED_LOOP", r"for\s+[^{]*{[\s\S]*?for\s+", "Nested loop (possible O(n^2)+)"),
    ("RUST.PERF.VEC_ALLOC", r"Vec::new\s*\(\s*\)", "Consider Vec::with_capacity for known size"),
    ("RUST.PERF.STRING_ALLOC", r"String::new\s*\(\s*\)", "Consider String::with_capacity for known size"),
    ("RUST.PERF.ITER_COLLECT", r"\.collect\s*::<Vec<_>>", "Consider specifying capacity for collect"),
    
    # Quality issues
    ("RUST.QUALITY.MAGIC_NUMBER", r"\b\d{4,}\b", "Magic number detected"),
    ("RUST.QUALITY.PANIC", r"panic!\s*\(", "Avoid panic! in production code"),
    ("RUST.QUALITY.UNUSED_VAR", r"let\s+_\s*=", "Unused variable with underscore"),
    ("RUST.QUALITY.DEBUG_PRINT", r"println!\s*\(", "Debug print in production code"),
    ("RUST.QUALITY.ALLOW", r"#\[allow\(", "Suppressed warning detected"),
    
    # Rust-specific patterns
    ("RUST.STYLE.MATCH", r"match\s+\w+\s*{", "Check match exhaustiveness"),
    ("RUST.STYLE.ENUM", r"enum\s+\w+\s*{", "Check enum design"),
    ("RUST.STYLE.TRAIT", r"trait\s+\w+\s*{", "Check trait design"),
    ("RUST.STYLE.IMPL", r"impl\s+\w+\s*{", "Check implementation"),
    ("RUST.STYLE.MACRO", r"macro_rules!\s+\w+", "Check macro definition"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class RustEngine(EngineBase):
    language = "rust"
    extensions = (".rs",)

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
        
        # Count functions (Rust style)
        functions = len(re.findall(r"fn\s+\w+\s*\([^)]*\)", source))
        complexity = float(len(re.findall(r"\b(if|for|while|match|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = RustEngine()
