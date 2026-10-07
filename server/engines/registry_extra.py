# server/engines/registry_extra.py
from typing import List, Tuple
from .generic_factory import GenericRegexEngine

# Helper: tiny aliases to shorten severity tags
SEC="security"; PERF="perf"; INFO="info"; WARN="warning"

# Each spec: (language, extensions, patterns[(ruleId, regex, title, sevTag)], func_regex, complexity_tokens)
LANG_SPECS: List[Tuple[str, Tuple[str, ...], list, str, Tuple[str, ...]]] = [

    # 1) VB.NET (.vb)
    ("vbnet", (".vb",), [
        ("VB.SECURITY.SQL_CONCAT", r"New\s+SqlCommand\s*\(\s*\"[^\"]*\+\s*\w+", "SQL concatenation; use parameters", SEC),
        ("VB.SECURITY.MD5", r"MD5\.Create\(", "MD5 is weak; prefer SHA256", SEC),
        ("VB.SECURITY.SECRET", r"(ApiKey|Secret|Password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("VB.QUALITY.ON_ERROR_RESUME", r"On\s+Error\s+Resume\s+Next", "On Error Resume Next hides failures", WARN),
        ("VB.QUALITY.EMPTY_CATCH", r"Catch\s+\w*\s*$\s*^\s*End\s+Try", "Empty catch block", WARN),
    ], r"\b(Function|Sub)\b\s+\w+\s*\(", ("if","for","while","catch","case")),

    # 2) Haskell (.hs)
    ("haskell", (".hs",), [
        ("HS.SECURITY.UNSAFE_PERFORM_IO", r"unsafePerformIO", "unsafePerformIO can break purity/safety", WARN),
        ("HS.PERF.NESTED_RECURSION", r"\brec\b|\bfix\b", "Potential heavy recursion; check termination", PERF),
        ("HS.QUALITY.PARTIAL", r"\bhead\s*\(|\btail\s*\(|\bfromJust\b", "Partial functions can crash on bad input", WARN),
        ("HS.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
    ], r"\b[a-zA-Z_]\w*\s*::", ("if","case","where","let")),

    # 3) OCaml (.ml, .mli)
    ("ocaml", (".ml",".mli"), [
        ("ML.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("ML.QUALITY.MUTABLE", r"\bmutable\b", "Mutable field; ensure thread-safety", INFO),
        ("ML.PERF.NESTED_LOOP", r"for\s+\w+\s*=.*do[\s\S]*for\s+\w+\s*=.*do", "Nested loops (O(n^2)+)", PERF),
    ], r"\blet\b\s+\w+\s*=", ("if","for","while","match")),

    # 4) F# (.fs, .fsi, .fsx)
    ("fsharp", (".fs",".fsi",".fsx"), [
        ("FS.SECURITY.SQL_CONCAT", r"SqlCommand\s*\(\s*\"[^\"]*\+\s*\w+", "SQL concatenation; use parameters", SEC),
        ("FS.SECURITY.SECRET", r"(ApiKey|Secret|Password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("FS.QUALITY.MUTABLE", r"\bmutable\b", "Mutable value; consider immutability", INFO),
        ("FS.PERF.NESTED_LOOP", r"for\s+\w+\s*=.*do[\s\S]*for\s+\w+\s*=.*do", "Nested loops", PERF),
    ], r"\blet\b\s+\w+\s*=", ("if","for","while","match","try")),

    # 5) Elixir (.ex, .exs)
    ("elixir", (".ex",".exs"), [
        ("EX.SECURITY.SYSTEM", r"\bsystem\s*\(", "system() executes OS commands; validate inputs", SEC),
        ("EX.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("EX.QUALITY.TASK_ASYNC", r"Task\.async_stream\(", "Ensure max_concurrency/backpressure", INFO),
        ("EX.PERF.NESTED_COMPREH", r"for\s+.+\s+<-.*\n\s*for\s+.+\s+<-", "Nested 'for' comprehensions (O(n^2)+)", PERF),
    ], r"\bdefp?\s+\w+\s*\(", ("if","case","with","try")),

    # 6) Erlang (.erl, .hrl)
    ("erlang", (".erl",".hrl"), [
        ("ERL.SECURITY.OS_CMD", r"os:cmd\s*\(", "os:cmd executes shell; validate inputs", SEC),
        ("ERL.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("ERL.QUALITY.CATCH_ALL", r"catch\s+_", "Broad catch-all", WARN),
        ("ERL.PERF.NESTED_LOOP", r"lists:foreach\([^\)]*\)\s*[,;]\s*lists:foreach\(", "Nested iterations", PERF),
    ], r"\b([a-z_]\w*)\s*\(", ("if","case","receive","try")),

    # 7) Clojure (.clj, .cljs, .cljc)
    ("clojure", (".clj",".cljs",".cljc"), [
        ("CLJ.SECURITY.SHELL", r"clojure.java.shell/sh", "Shell execution; validate inputs", SEC),
        ("CLJ.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s+\"[^\"]+\"", "Hardcoded secret", SEC),
        ("CLJ.QUALITY.DOSYMBOL", r"\bdef\s+\w+\s+[^(\s]", "Global var (def) with literal; check design", INFO),
        ("CLJ.PERF.NESTED_LOOP", r"\(for\s+\[.*\]\s*\(for\s+\[", "Nested 'for'", PERF),
    ], r"\b\(defn\b", ("if","when","for","case","try")),

    # 8) Fortran (.f, .for, .f90, .f95)
    ("fortran", (".f",".for",".f90",".f95"), [
        ("F.SECURITY.SYSTEM", r"\bcall\s+system\s*\(", "SYSTEM call executes shell", SEC),
        ("F.QUALITY.GOTO", r"\bgoto\b", "Use of GOTO reduces readability", WARN),
        ("F.PERF.NESTED_LOOP", r"\bdo\b[\s\S]*\bdo\b", "Nested loops (O(n^2)+)", PERF),
        ("F.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret", SEC),
    ], r"\b(subroutine|function)\b\s+\w+", ("if","do","select","case")),

    # 9) COBOL (.cob, .cbl)
    ("cobol", (".cob",".cbl"), [
        ("COBOL.SECURITY.SYSTEM", r"\bCALL\s+\"SYSTEM\"", "SYSTEM call executes shell", SEC),
        ("COBOL.QUALITY.GOTO", r"\bGO\s+TO\b", "GO TO considered harmful", WARN),
        ("COBOL.QUALITY.PERFORM_NESTED", r"\bPERFORM\b[\s\S]*\bPERFORM\b", "Nested PERFORMs", PERF),
        ("COBOL.SECURITY.SECRET", r"(API-KEY|SECRET|PASSWORD)\s+VALUE\s+\"[^\"]+\"", "Hardcoded secret", SEC),
    ], r"\b(PROCEDURE\s+DIVISION)", ("IF","PERFORM","EVALUATE")),

    # 10) Pascal/Delphi (.pas, .dpr)
    ("pascal", (".pas",".dpr"), [
        ("PAS.SECURITY.EXEC", r"\bWinExec\s*\(|\bShellExecute", "Command execution; validate inputs", SEC),
        ("PAS.SECURITY.SECRET", r"(ApiKey|Secret|Password)\s*:=\s*'[^']+'", "Hardcoded secret", SEC),
        ("PAS.QUALITY.WITH", r"\bwith\s+\w+\s+do", "WITH can hide variable scope", WARN),
        ("PAS.PERF.NESTED_LOOP", r"\bfor\s+\w+\s*:=.*do[\s\S]*for\s+\w+\s*:=.*do", "Nested loops", PERF),
    ], r"\bfunction\b|\bprocedure\b", ("if","for","while","case","try")),

    # 11) Ada (.adb, .ads)
    ("ada", (".adb",".ads"), [
        ("ADA.SECURITY.SECRET", r"(Api_Key|Secret|Password)\s*:\s*String\s*:=", "Hardcoded secret", SEC),
        ("ADA.QUALITY.GOTO", r"\bgoto\b", "Use of goto", WARN),
        ("ADA.PERF.NESTED_LOOP", r"\bfor\s+\w+\s+in\b[\s\S]*\bfor\s+\w+\s+in\b", "Nested loops", PERF),
    ], r"\bprocedure\b|\bfunction\b", ("if","for","while","case","exception")),

    # 12) Solidity (.sol)
    ("solidity", (".sol",), [
        ("SOL.SECURITY.TX_ORIGIN", r"tx\.origin", "Avoid tx.origin for auth; use msg.sender", SEC),
        ("SOL.SECURITY.REENTRANCY", r"\.call\s*\(", "Low-level call; reentrancy risk", SEC),
        ("SOL.SECURITY.SELFDESTRUCT", r"selfdestruct\s*\(", "Selfdestruct dangerous", SEC),
        ("SOL.QUALITY.PRAGMA_FLOAT", r"pragma\s+experimental", "Experimental pragma; review", WARN),
        ("SOL.PERF.UNBOUNDED_LOOP", r"for\s*\([^)]*\)", "Unbounded loops can be gas-heavy", PERF),
        ("SOL.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
    ], r"\bfunction\b\s+\w+\s*\(", ("if","for","while","require","revert","assert","catch")),

    # 13) VHDL (.vhd, .vhdl)
    ("vhdl", (".vhd",".vhdl"), [
        ("VHDL.QUALITY.LATCH_INFER", r"process\s*\([^)]*\)\s*begin[\s\S]*if\s*\([^)]+\)\s*then[\s\S]*--\s*no\s*else", "Possible latch inference", WARN),
        ("VHDL.SECURITY.SECRET", r"(APIKEY|SECRET|PASSWORD)\s*:\s*string\s*:=", "Hardcoded secret", SEC),
        ("VHDL.PERF.NESTED", r"for\s+\w+\s+in[\s\S]*for\s+\w+\s+in", "Nested 'for' loops", PERF),
    ], r"\bprocess\b|\bfunction\b|\bprocedure\b", ("if","case","for","when")),

    # 14) SystemVerilog/Verilog (.sv, .svh, .v)
    ("sv", (".sv",".svh",".v"), [
        ("SV.SECURITY.SECRET", r"(APIKEY|SECRET|PASSWORD)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("SV.QUALITY.BLOCKING_IN_SEQ", r"always_ff[\s\S]*=", "Blocking assignment in seq logic; prefer <=", WARN),
        ("SV.PERF.NESTED", r"for\s*\([^)]*\)\s*begin[\s\S]*for\s*\(", "Nested loops", PERF),
    ], r"\bmodule\b|\bfunction\b", ("if","case","for","while")),

    # 15) Tcl (.tcl)
    ("tcl", (".tcl",), [
        ("TCL.SECURITY.EVAL", r"\beval\s+", "eval executes strings; validate inputs", SEC),
        ("TCL.SECURITY.EXEC", r"\bexec\s+", "exec runs OS commands; validate inputs", SEC),
        ("TCL.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s+\"[^\"]+\"", "Hardcoded secret", SEC),
        ("TCL.PERF.NESTED_LOOP", r"for\s+\{[^}]+\}\s+\{[^}]+\}\s+\{[^}]+\}\s*\{[\s\S]*for\s+", "Nested loops", PERF),
    ], r"\bproc\b\s+\w+\s+\{", ("if","for","while","switch","catch")),

    # 16) Haxe (.hx)
    ("haxe", (".hx",), [
        ("HX.SECURITY.SECRET", r"(apiKey|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("HX.SECURITY.HTTP", r"\"http://", "Use HTTPS", SEC),
        ("HX.QUALITY.TRACE", r"\btrace\s*\(", "Excessive trace logging", INFO),
        ("HX.PERF.NESTED_LOOP", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loops", PERF),
    ], r"\bfunction\b\s+\w+\s*\(", ("if","for","while","switch","case","try")),

    # 17) Elm (.elm)
    ("elm", (".elm",), [
        ("ELM.SECURITY.HTTP", r"Http\.get\s+\"http://", "Use HTTPS in Http.get", SEC),
        ("ELM.QUALITY.DEBUG", r"Debug\.(log|todo)", "Debug functions should not ship", WARN),
        ("ELM.PERF.NESTED", r"List\.map\s+\(.*List\.map", "Nested List.map (O(n^2)+)", PERF),
    ], r"\b(\w+)\s*:\s*.*->", ("if","case","let")),

    # 18) CUDA (.cu, .cuh)
    ("cuda", (".cu",".cuh"), [
        ("CUDA.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("CUDA.PERF.UNCOALESCED", r"threadIdx|blockIdx", "Check memory coalescing; perf risk", PERF),
        ("CUDA.QUALITY.SYNC", r"__syncthreads\s*\(\s*\)", "Excess barriers can hurt perf", INFO),
        ("CUDA.PERF.NESTED", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loops", PERF),
    ], r"\b__global__\b|\b__device__\b|\b__host__\b", ("if","for","while","switch")),

    # 19) OpenCL (.cl)
    ("opencl", (".cl",), [
        ("CL.SECURITY.SECRET", r"(api[_-]?key|secret|password)\s*=\s*\"[^\"]+\"", "Hardcoded secret", SEC),
        ("CL.PERF.BARRIER", r"barrier\s*\(", "Barrier; ensure minimal use", PERF),
        ("CL.PERF.NESTED", r"for\s*\([^)]*\)\s*\{[\s\S]*?for\s*\(", "Nested loops", PERF),
    ], r"\bkernel\b\s+void\s+\w+\s*\(", ("if","for","while","switch")),

    # 20) Assembly (.asm, .s)
    ("assembly", (".asm",".s"), [
        ("ASM.SECURITY.SYSCALL", r"\bsyscall\b", "Syscall: validate usage/privileges", INFO),
        ("ASM.QUALITY.MAGIC", r"\b0x[0-9A-Fa-f]{2,}\b", "Magic constants; document meaning", INFO),
        ("ASM.PERF.REP_MOVS", r"\brep\s+movs", "Bulk move; check performance/alternatives", PERF),
        ("ASM.SECURITY.SECRET", r"(API|SECRET|PASSWORD)\s*:\s*[A-Za-z0-9\-_]+", "Embedded secret-like token", SEC),
    ], r"\b(global|extern)\b", ("jmp","jz","jnz","call","ret","cmp")),
]

ENGINES = [
    GenericRegexEngine(lang, exts, pats, func_rx, tokens)
    for (lang, exts, pats, func_rx, tokens) in LANG_SPECS
]
