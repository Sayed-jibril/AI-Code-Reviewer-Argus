# AI Code Reviewer Argus

A static code analysis tool that scans source code in **9 languages** for security risks, performance problems, memory-safety bugs, and code-quality issues. It pairs a FastAPI backend (AST parsing + pattern matching) with a React + TypeScript frontend.

> **Your code is never executed.** All analysis is purely static.

**Author:** [Sayed Jibril](https://github.com/Sayed-jibril)

---

## Features

- **Multi-language support:** Python, JavaScript/TypeScript, C#, Java, C/C++, Go, Rust, PHP, and Ruby
- **Deep Python analysis:** AST-based detection of unused variables and imports, broad exception handlers, mutable default arguments, and nested loops
- **Security scanning:** flags `eval()`/`exec()`, hardcoded secrets, weak hashing, SQL injection, command injection, and more
- **Performance checks:** nested loops, DOM queries inside loops, `strlen` in loops, N+1 queries, and similar patterns
- **Memory safety:** buffer overflows, memory leaks, unsafe blocks, and improper resource handling
- **Complexity metrics:** McCabe-style complexity scores
- **Modern web UI:** multi-file upload, issue filtering, and a clear results view

## Tech Stack

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Backend  | Python, FastAPI, Pydantic           |
| Analysis | Python `ast` module, regex patterns |
| Frontend | React, TypeScript, Vite             |

## Project Structure

```
server/                 # FastAPI backend
├── engines/
│   ├── python_ast.py   # Python AST analysis
│   └── patterns.py     # Regex-based pattern matching
├── llm.py              # LLM enrichment (placeholder)
├── main.py             # FastAPI app
├── models.py           # Pydantic models
└── requirements.txt

web/                    # React frontend
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── api.ts          # API client
│   └── main.tsx        # App entry point
├── index.html
└── package.json
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### 1. Clone the repository

```bash
git clone https://github.com/Sayed-jibril/<repo-name>.git
cd <repo-name>
```

### 2. Run the backend

```bash
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000
```

The API runs at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 3. Run the frontend

```bash
cd web
npm install
npm run dev
```

The app runs at `http://localhost:5173` with the API proxy already configured.

## Usage

1. Open `http://localhost:5173`.
2. Select one or more source files to upload (any supported language).
3. Click **Review**.
4. Browse the detected issues, complexity metrics, and test suggestions, and filter by severity or category.

## API

### `POST /api/review`

Uploads files for analysis.

- **Request:** `multipart/form-data` with one or more files
- **Response:** JSON containing issues, metrics, and test suggestions

```bash
curl -X POST http://localhost:8000/api/review \
  -F "files=@example.py" \
  -F "files=@app.js"
```

## Supported Languages and Rules

| Language                    | Extensions                | Security                                                                               | Performance                                                  | Quality / Memory                                                                      |
| --------------------------- | ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| **Python**                  | `.py`                     | `eval()`, `exec()`, `pickle.loads()`, hardcoded secrets, MD5, SQL injection            | Nested loops                                                 | Unused variables/imports, broad `except`, mutable default arguments                   |
| **JavaScript / TypeScript** | `.js` `.jsx` `.ts` `.tsx` | `eval()`, `Function` constructor, `innerHTML`, `document.write`, unvalidated redirects | DOM queries in loops, nested loops                           | `var` usage, `any` types, `==` comparisons, broad `catch`                             |
| **C#**                      | `.cs`                     | SQL concatenation, MD5, non-cryptographic `Random`, hardcoded secrets                  | Nested loops                                                 | Empty catch, catching base `Exception`, missing `using`, `async void`                 |
| **Java**                    | `.java`                   | SQL concatenation, MD5, hardcoded secrets                                              | Nested loops                                                 | Empty catch, catching base `Exception`, excessive `System.out.println`                |
| **C / C++**                 | `.c` `.cpp` `.h` `.hpp`   | Buffer overflows (`strcpy`, `strcat`, `sprintf`), unsafe functions, hardcoded secrets  | Nested loops, `strlen` in loops                              | Memory leaks, malloc/free misuse, missing NULL checks, magic numbers, `goto`          |
| **Go**                      | `.go`                     | SQL and command injection, unsafe pointers, weak random                                | Slice append without capacity, nested loops, goroutine leaks | Ignored errors, unused imports, `panic` usage, global variables                       |
| **Rust**                    | `.rs`                     | `unsafe` blocks, `unwrap`/`expect` panics, unchecked operations                        | Nested loops, Vec/String without capacity                    | Unnecessary clones, mutable borrows, magic numbers, debug prints, suppressed warnings |
| **PHP**                     | `.php` `.phtml`           | SQL injection, XSS, `eval`/`exec`, weak hashing, dynamic includes                      | Nested loops, `foreach` with references                      | Error suppression, empty catch, global variables                                      |
| **Ruby**                    | `.rb` `.erb`              | `eval`, `system`/`exec`, backticks, SQL injection, XSS                                 | N+1 queries, nested loops, string concatenation              | Broad `rescue`, magic numbers, global variables, debug prints                         |

## Roadmap

- [ ] Real LLM integration for issue explanations and test generation
- [ ] Auto-generated pytest files for detected functions
- [ ] Unified diff patches for automatic fixes
- [ ] AST-level analysis for languages beyond Python
- [ ] Export reports as Markdown / JSON

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## Author

**Sayed Jibril** — [github.com/Sayed-jibril](https://github.com/Sayed-jibril)
