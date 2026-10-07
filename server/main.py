from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from .models import ReviewResult, ReviewMetrics
from .engines.python_ast import analyze_python_file
from .engines.patterns import analyze_text
from .engines.js_ts import ENGINE as JS_TS_ENGINE
from .engines.csharp import ENGINE as CS_ENGINE
from .engines.java import ENGINE as JAVA_ENGINE
from .engines.c_cpp import ENGINE as C_CPP_ENGINE
from .engines.go import ENGINE as GO_ENGINE
from .engines.rust import ENGINE as RUST_ENGINE
from .engines.php import ENGINE as PHP_ENGINE
from .engines.ruby import ENGINE as RUBY_ENGINE
from .engines.swift import ENGINE as SWIFT_ENGINE
from .engines.kotlin import ENGINE as KOTLIN_ENGINE
from .engines.scala import ENGINE as SCALA_ENGINE
from .engines.objc import ENGINE as OBJC_ENGINE
from .engines.dart import ENGINE as DART_ENGINE
from .engines.lua import ENGINE as LUA_ENGINE
from .engines.perl import ENGINE as PERL_ENGINE
from .engines.r_lang import ENGINE as R_ENGINE
from .engines.matlab import ENGINE as MATLAB_ENGINE
from .engines.shell_bash import ENGINE as BASH_ENGINE
from .engines.powershell import ENGINE as POWERSHELL_ENGINE
from .engines.sql_lang import ENGINE as SQL_ENGINE
from .engines.registry_extra import ENGINES as EXTRA_ENGINES
from .llm import enrich_with_llm

app = FastAPI(title="AI Code Reviewer")

SUPPORTED_EXT = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".cs": "csharp",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".hxx": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".phtml": "php",
    ".php3": "php",
    ".php4": "php",
    ".php5": "php",
    ".php7": "php",
    ".phps": "php",
    ".rb": "ruby",
    ".erb": "ruby",
    ".rake": "ruby",
    ".gemspec": "ruby",
    ".podspec": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".m": "objective-c",
    ".mm": "objective-c",
    ".dart": "dart",
    ".lua": "lua",
    ".pl": "perl",
    ".pm": "perl",
    ".r": "r",
    ".R": "r",
    ".sh": "bash",
    ".bash": "bash",
    ".ps1": "powershell",
    ".psm1": "powershell",
    ".sql": "sql",
    ".vb": "vbnet",
    ".hs": "haskell",
    ".ml": "ocaml", ".mli": "ocaml",
    ".fs": "fsharp", ".fsi": "fsharp", ".fsx": "fsharp",
    ".ex": "elixir", ".exs": "elixir",
    ".erl": "erlang", ".hrl": "erlang",
    ".clj": "clojure", ".cljs": "clojure", ".cljc": "clojure",
    ".f": "fortran", ".for": "fortran", ".f90": "fortran", ".f95": "fortran",
    ".cob": "cobol", ".cbl": "cobol",
    ".pas": "pascal", ".dpr": "pascal",
    ".adb": "ada", ".ads": "ada",
    ".sol": "solidity",
    ".vhd": "vhdl", ".vhdl": "vhdl",
    ".sv": "sv", ".svh": "sv", ".v": "sv",
    ".tcl": "tcl",
    ".hx": "haxe",
    ".elm": "elm",
    ".cu": "cuda", ".cuh": "cuda",
    ".cl": "opencl",
    ".asm": "assembly", ".s": "assembly",
}

ENGINE_REGISTRY = [
    JS_TS_ENGINE,
    CS_ENGINE,
    JAVA_ENGINE,
    C_CPP_ENGINE,
    GO_ENGINE,
    RUST_ENGINE,
    PHP_ENGINE,
    RUBY_ENGINE,
    SWIFT_ENGINE,
    KOTLIN_ENGINE,
    SCALA_ENGINE,
    OBJC_ENGINE,
    DART_ENGINE,
    LUA_ENGINE,
    PERL_ENGINE,
    R_ENGINE,
    MATLAB_ENGINE,
    BASH_ENGINE,
    POWERSHELL_ENGINE,
    SQL_ENGINE,
    # Python engine is handled separately via analyze_python_file (keep existing)
]

# Add extra engines from registry
for eng in EXTRA_ENGINES:
    if eng not in ENGINE_REGISTRY:
        ENGINE_REGISTRY.append(eng)

def _ext(path: str) -> str:
    import os
    return os.path.splitext(path)[1].lower()

def _read_text(b: bytes) -> str:
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1", errors="ignore")

@app.post("/api/review")
async def review(files: List[UploadFile] = File(...)):
    all_issues = []
    total_functions = 0
    complexities = []
    source_map = {}

    for f in files:
        name = f.filename or "unknown"
        content = await f.read()
        text = _read_text(content)
        source_map[name] = text

        ext = _ext(name)
        lang = SUPPORTED_EXT.get(ext)

        # Pattern checks (any text)
        all_issues.extend(analyze_text(name, text))

        # Language-specific AST checks
        if lang == "python":
            issues, metrics, _tags = analyze_python_file(name, text)
            all_issues.extend(issues)
            total_functions += metrics["functions"]
            complexities.append(metrics["complexity"])
        
        # Dispatch to language engines (non-Python)
        for eng in ENGINE_REGISTRY:
            if ext in eng.extensions:
                eng_issues, eng_metrics = eng.analyze(name, text)
                all_issues.extend(eng_issues)
                total_functions += int(eng_metrics.get("functions", 0))
                if "complexity" in eng_metrics:
                    complexities.append(float(eng_metrics["complexity"]))
                break  # stop after first matching engine

    # LLM enrichment (placeholder)
    tests = enrich_with_llm(all_issues, source_map)

    avg_complexity = float(sum(complexities) / len(complexities)) if complexities else 0.0
    result = ReviewResult(
        issues=all_issues,
        tests=tests,
        metrics=ReviewMetrics(files=len(files), functions=total_functions, avgComplexity=avg_complexity)
    )
    return JSONResponse(result.model_dump())
