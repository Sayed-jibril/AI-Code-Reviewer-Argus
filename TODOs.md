# Future Enhancements - TODOs

## AST-Based Analyzers (Future Implementation)

### JavaScript/TypeScript
- **TODO**: Swap to AST via `esprima`/`espree` (Node microservice) or tree-sitter Python binding
- **Benefits**: More accurate unused variable detection, better scope analysis, type checking
- **Implementation**: Create separate Node.js service or integrate tree-sitter

### C#
- **TODO**: Integrate Roslyn via a tiny .NET sidecar that returns JSON issues
- **Benefits**: Full semantic analysis, unused using statements, better exception analysis
- **Implementation**: Create minimal .NET console app with Roslyn SDK

### Java
- **TODO**: Integrate JavaParser to extract AST, method metrics, and exceptions per method
- **Benefits**: Accurate unused import detection, better method complexity analysis
- **Implementation**: Use JavaParser library or create Java service

## Additional Features

### Configuration & Customization
- **TODO**: Add rule toggles and severity config via JSON
- **TODO**: Support for custom rule definitions
- **TODO**: Language-specific configuration files

### Test Generation
- **TODO**: Generate language-specific unit tests (jest, NUnit, JUnit) in a `/tests` bundle
- **TODO**: Test coverage analysis and suggestions

### Report Generation
- **TODO**: Export reports in Markdown/JSON format
- **TODO**: Integration with CI/CD pipelines
- **TODO**: Historical analysis and trend tracking

### Additional Languages
- **TODO**: Go (.go) - security patterns, unused imports, error handling
- **TODO**: Rust (.rs) - unsafe blocks, memory management patterns
- **TODO**: PHP (.php) - SQL injection, XSS, security patterns
- **TODO**: Ruby (.rb) - security patterns, performance issues

### Performance Improvements
- **TODO**: Parallel analysis for multiple files
- **TODO**: Caching of analysis results
- **TODO**: Incremental analysis for large codebases

### UI Enhancements
- **TODO**: File tree view for multi-file projects
- **TODO**: Issue grouping by category/severity
- **TODO**: Code diff view for suggested fixes
- **TODO**: Integration with popular IDEs (VS Code extension)

## Current Status

✅ **Completed**:
- Multi-language support with regex-based analysis
- Pluggable engine architecture
- Security, performance, and quality pattern detection
- Web UI with filtering capabilities
- Python AST analysis (unchanged)

🔄 **In Progress**:
- None currently

⏳ **Planned**:
- AST-based analyzers for JS/TS, C#, Java
- Enhanced test generation
- Report export functionality
