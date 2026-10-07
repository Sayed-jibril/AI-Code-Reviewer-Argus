# server/engines/php.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    # Security issues
    ("PHP.SECURITY.SQL_INJECTION", r"mysql_query\s*\(\s*\"[^\"]*\+\s*\$\w+", "SQL injection risk; use prepared statements"),
    ("PHP.SECURITY.XSS", r"echo\s+\$\w+", "Potential XSS; use htmlspecialchars()"),
    ("PHP.SECURITY.EVAL", r"eval\s*\(", "eval() is dangerous"),
    ("PHP.SECURITY.EXEC", r"exec\s*\(", "exec() can be dangerous"),
    ("PHP.SECURITY.SHELL_EXEC", r"shell_exec\s*\(", "shell_exec() can be dangerous"),
    ("PHP.SECURITY.SYSTEM", r"system\s*\(", "system() can be dangerous"),
    ("PHP.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("PHP.SECURITY.MD5", r"md5\s*\(", "MD5 is weak; use password_hash()"),
    ("PHP.SECURITY.SHA1", r"sha1\s*\(", "SHA1 is weak; use password_hash()"),
    
    # Performance issues
    ("PHP.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*{[\s\S]*?for\s*\(", "Nested loop (possible O(n^2)+)"),
    ("PHP.PERF.FOREACH_REF", r"foreach\s*\(\s*\$\w+\s+as\s+&\s*\$\w+\s*\)", "Reference in foreach can cause issues"),
    ("PHP.PERF.ARRAY_COPY", r"array_merge\s*\(\s*array\s*\(\s*\)", "Unnecessary array merge"),
    
    # Quality issues
    ("PHP.QUALITY.ERROR_SUPPRESSION", r"@\s*\w+\s*\(", "Error suppression with @"),
    ("PHP.QUALITY.EMPTY_CATCH", r"catch\s*\(\s*\w+\s+\$\w+\s*\)\s*{(\s*//.*|\s*)}", "Empty catch block"),
    ("PHP.QUALITY.BROAD_CATCH", r"catch\s*\(\s*Exception\s+\$\w+\s*\)\s*{", "Catching base Exception"),
    ("PHP.QUALITY.MAGIC_NUMBER", r"\b\d{4,}\b", "Magic number detected"),
    ("PHP.QUALITY.GLOBAL", r"\$GLOBALS\s*\[", "Global variable usage"),
    ("PHP.QUALITY.SUPER_GLOBAL", r"\$_GET\s*\[|\$_POST\s*\[|\$_REQUEST\s*\[", "Direct superglobal access"),
    ("PHP.QUALITY.REGISTER_GLOBALS", r"register_globals", "register_globals is deprecated"),
    
    # PHP-specific patterns
    ("PHP.STYLE.SHORT_TAG", r"<\?=", "Short tags may not be enabled"),
    ("PHP.STYLE.OLD_STYLE", r"mysql_", "Old MySQL functions are deprecated"),
    ("PHP.STYLE.INCLUDE", r"include\s+['\"]\s*\$\w+", "Dynamic include can be dangerous"),
    ("PHP.STYLE.REQUIRE", r"require\s+['\"]\s*\$\w+", "Dynamic require can be dangerous"),
    ("PHP.STYLE.UNSET", r"unset\s*\(\s*\$\w+\s*\)", "Check unset usage"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class PhpEngine(EngineBase):
    language = "php"
    extensions = (".php", ".phtml", ".php3", ".php4", ".php5", ".php7", ".phps")

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
        
        # Count functions (PHP style)
        functions = len(re.findall(r"function\s+\w+\s*\([^)]*\)", source))
        complexity = float(len(re.findall(r"\b(if|for|while|catch|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": functions, "complexity": complexity}

ENGINE = PhpEngine()
