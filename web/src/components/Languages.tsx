import React from 'react';

const Languages: React.FC = () => {
  const languageCategories = [
    {
      title: "General Purpose",
      languages: [
        { name: "Python", ext: ".py", icon: "🐍" },
        { name: "JavaScript", ext: ".js", icon: "📜" },
        { name: "TypeScript", ext: ".ts", icon: "📘" },
        { name: "Java", ext: ".java", icon: "☕" },
        { name: "C#", ext: ".cs", icon: "🔷" },
        { name: "C/C++", ext: ".c/.cpp", icon: "⚡" },
        { name: "Go", ext: ".go", icon: "🐹" },
        { name: "Rust", ext: ".rs", icon: "🦀" },
        { name: "PHP", ext: ".php", icon: "🐘" },
        { name: "Ruby", ext: ".rb", icon: "💎" },
        { name: "Swift", ext: ".swift", icon: "🍎" },
        { name: "Kotlin", ext: ".kt", icon: "🔶" },
        { name: "Scala", ext: ".scala", icon: "⚡" },
        { name: "Dart", ext: ".dart", icon: "🎯" },
        { name: "Lua", ext: ".lua", icon: "🌙" },
        { name: "Perl", ext: ".pl", icon: "🐪" },
        { name: "R", ext: ".r", icon: "📊" },
        { name: "MATLAB", ext: ".m", icon: "🔬" },
        { name: "Shell/Bash", ext: ".sh", icon: "🐚" },
        { name: "PowerShell", ext: ".ps1", icon: "💻" },
        { name: "SQL", ext: ".sql", icon: "🗄️" },
        { name: "VB.NET", ext: ".vb", icon: "🔵" },
        { name: "Haskell", ext: ".hs", icon: "λ" },
        { name: "OCaml", ext: ".ml", icon: "🐫" },
        { name: "F#", ext: ".fs", icon: "🔷" },
        { name: "Elixir", ext: ".ex", icon: "⚗️" },
        { name: "Erlang", ext: ".erl", icon: "📞" },
        { name: "Clojure", ext: ".clj", icon: "()" },
        { name: "Fortran", ext: ".f", icon: "🔢" },
        { name: "COBOL", ext: ".cob", icon: "💼" },
        { name: "Pascal", ext: ".pas", icon: "📝" },
        { name: "Ada", ext: ".adb", icon: "🛡️" },
        { name: "Solidity", ext: ".sol", icon: "🔗" },
        { name: "VHDL", ext: ".vhd", icon: "🔌" },
        { name: "SystemVerilog", ext: ".sv", icon: "🔧" },
        { name: "Tcl", ext: ".tcl", icon: "🛠️" },
        { name: "Haxe", ext: ".hx", icon: "⚡" },
        { name: "Elm", ext: ".elm", icon: "🌳" },
        { name: "CUDA", ext: ".cu", icon: "🚀" },
        { name: "OpenCL", ext: ".cl", icon: "⚙️" },
        { name: "Assembly", ext: ".asm", icon: "🔧" }
      ]
    }
  ];

  return (
    <section id="languages" style={{
      padding: '3rem 0',
      backgroundColor: 'var(--primary-bg)'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 1.5rem'
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: '2rem'
        }}>
          <h2 style={{
            fontSize: '2.5rem',
            fontWeight: 'bold',
            marginBottom: '1rem',
            color: 'var(--text-primary)'
          }}>Supported Languages</h2>
          <p style={{
            fontSize: '1.125rem',
            color: 'var(--text-secondary)',
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            PolySpector supports 41+ programming languages with comprehensive static analysis capabilities
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
          gap: '1rem',
          marginBottom: '2rem'
        }}>
          {languageCategories[0].languages.map((lang, index) => (
            <div key={index} style={{
              background: 'var(--gradient-card)',
              border: '1px solid var(--border-color)',
              borderRadius: '0.75rem',
              padding: '1rem',
              textAlign: 'center',
              transition: 'transform 0.3s ease, box-shadow 0.3s ease',
              cursor: 'pointer'
            }} onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.3)';
              e.currentTarget.style.borderColor = 'var(--accent-primary)';
            }} onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.2)';
              e.currentTarget.style.borderColor = 'var(--border-color)';
            }}>
              <div style={{
                fontSize: '2rem',
                marginBottom: '0.5rem'
              }}>
                {lang.icon}
              </div>
              <h3 style={{
                fontSize: '1rem',
                fontWeight: '600',
                color: 'var(--text-primary)',
                margin: '0 0 0.25rem 0'
              }}>
                {lang.name}
              </h3>
              <p style={{
                fontSize: '0.75rem',
                color: 'var(--text-muted)',
                margin: '0',
                fontFamily: 'monospace'
              }}>
                {lang.ext}
              </p>
            </div>
          ))}
        </div>

        <div style={{
          textAlign: 'center',
          padding: '1.5rem',
          background: 'var(--gradient-card)',
          border: '1px solid var(--border-color)',
          borderRadius: '0.75rem'
        }}>
          <h3 style={{
            fontSize: '1.25rem',
            fontWeight: '600',
            color: 'var(--text-primary)',
            marginBottom: '0.5rem'
          }}>
            Ready to Analyze Your Code?
          </h3>
          <p style={{
            color: 'var(--text-secondary)',
            marginBottom: '1rem'
          }}>
            Upload files in any of these supported languages and get instant analysis results
          </p>
          <a href="#upload" style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.75rem 1.5rem',
            background: 'var(--gradient-primary)',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '0.5rem',
            fontWeight: '500',
            transition: 'transform 0.2s ease'
          }} onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'} onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Start Code Review
          </a>
        </div>
      </div>
    </section>
  );
};

export default Languages;
