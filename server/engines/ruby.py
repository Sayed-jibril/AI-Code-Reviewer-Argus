# server/engines/ruby.py
import re
from typing import List, Dict, Tuple
from ..models import Issue
from .base import EngineBase

_PATTERNS = [
    # Security issues
    ("RUBY.SECURITY.EVAL", r"eval\s*\(", "eval() is dangerous"),
    ("RUBY.SECURITY.SYSTEM", r"system\s*\(", "system() can be dangerous"),
    ("RUBY.SECURITY.EXEC", r"exec\s*\(", "exec() can be dangerous"),
    ("RUBY.SECURITY.BACKTICKS", r"`[^`]*`", "Backticks can execute shell commands"),
    ("RUBY.SECURITY.SQL_INJECTION", r"execute\s*\(\s*\"[^\"]*#\{[^}]*\}", "SQL injection risk"),
    ("RUBY.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]", "Possible hardcoded secret"),
    ("RUBY.SECURITY.MD5", r"Digest::MD5", "MD5 is weak; use SHA256"),
    ("RUBY.SECURITY.XSS", r"<%=[^%]*%>", "Potential XSS; use h() helper"),
    ("RUBY.SECURITY.MASS_ASSIGNMENT", r"params\[:(\w+)\]", "Mass assignment vulnerability"),
    
    # Performance issues
    ("RUBY.PERF.NESTED_LOOP", r"each\s+do[^}]*end[^}]*each\s+do", "Nested loops (possible O(n^2)+)"),
    ("RUBY.PERF.N_PLUS_ONE", r"\.each\s+do[^}]*\.[a-z_]+\s*\([^)]*\)", "N+1 query pattern"),
    ("RUBY.PERF.ARRAY_COPY", r"Array\.new", "Unnecessary array creation"),
    ("RUBY.PERF.STRING_CONCAT", r"\+\s*['\"]", "String concatenation in loop"),
    
    # Quality issues
    ("RUBY.QUALITY.RESCUE", r"rescue\s*=>\s*\w+", "Broad exception rescue"),
    ("RUBY.QUALITY.EMPTY_RESCUE", r"rescue[^}]*end", "Empty rescue block"),
    ("RUBY.QUALITY.MAGIC_NUMBER", r"\b\d{4,}\b", "Magic number detected"),
    ("RUBY.QUALITY.GLOBAL_VAR", r"\$\w+", "Global variable usage"),
    ("RUBY.QUALITY.INSTANCE_VAR", r"@\w+", "Instance variable outside class"),
    ("RUBY.QUALITY.PUTS", r"puts\s+", "puts in production code"),
    ("RUBY.QUALITY.PRINT", r"print\s+", "print in production code"),
    
    # Ruby-specific patterns
    ("RUBY.STYLE.SYMBOL", r":\w+", "Symbol usage"),
    ("RUBY.STYLE.BLOCK", r"do\s*\|[^|]*\|", "Block parameter"),
    ("RUBY.STYLE.METHOD", r"def\s+\w+", "Method definition"),
    ("RUBY.STYLE.CLASS", r"class\s+\w+", "Class definition"),
    ("RUBY.STYLE.MODULE", r"module\s+\w+", "Module definition"),
    ("RUBY.STYLE.ATTR", r"attr_accessor|attr_reader|attr_writer", "Attribute accessor"),
    ("RUBY.STYLE.REQUIRE", r"require\s+['\"]", "Require statement"),
    ("RUBY.STYLE.INCLUDE", r"include\s+\w+", "Include statement"),
]

def _line_of(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1

class RubyEngine(EngineBase):
    language = "ruby"
    extensions = (".rb", ".erb", ".rake", ".gemspec", ".podspec")

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
        
        # Count methods (Ruby style)
        methods = len(re.findall(r"def\s+\w+", source))
        complexity = float(len(re.findall(r"\b(if|unless|while|until|for|case)\b", source, re.IGNORECASE)) + 1)
        return issues, {"functions": methods, "complexity": complexity}

ENGINE = RubyEngine()
