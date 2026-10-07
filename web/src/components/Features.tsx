import React from 'react';

const Features: React.FC = () => {
  const features = [
    {
      icon: "🔒",
      title: "Security Analysis",
      description: "Detect vulnerabilities, hardcoded secrets, SQL injection, XSS, and other security risks across all supported languages."
    },
    {
      icon: "⚡",
      title: "Performance Optimization",
      description: "Identify performance bottlenecks, memory leaks, inefficient algorithms, and optimization opportunities."
    },
    {
      icon: "🎯",
      title: "Code Quality",
      description: "Find code smells, maintainability issues, complexity problems, and suggest improvements."
    },
    {
      icon: "🌐",
      title: "Multi-Language Support",
      description: "Comprehensive analysis for 41+ programming languages with language-specific rules and patterns."
    },
    {
      icon: "📊",
      title: "Detailed Reports",
      description: "Get comprehensive reports with severity levels, explanations, suggestions, and code snippets."
    },
    {
      icon: "🚀",
      title: "Instant Results",
      description: "Real-time static analysis with no code execution - your code stays private and secure."
    }
  ];

  return (
    <section id="features" style={{
      padding: '2rem 0',
      backgroundColor: 'var(--secondary-bg)'
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
            fontSize: '2rem',
            fontWeight: 'bold',
            marginBottom: '0.5rem',
            color: 'var(--text-primary)'
          }}>Powerful Features</h2>
          <p style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Comprehensive code analysis with advanced detection capabilities
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1rem',
          marginBottom: '2rem'
        }}>
          {features.map((feature, index) => (
            <div key={index} style={{
              background: 'var(--gradient-card)',
              border: '1px solid var(--border-color)',
              borderRadius: '0.75rem',
              padding: '1rem',
              transition: 'transform 0.3s ease, box-shadow 0.3s ease'
            }} onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.3)';
            }} onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.2)';
            }}>
              <div style={{
                fontSize: '2rem',
                marginBottom: '0.5rem'
              }}>
                {feature.icon}
              </div>
              <h3 style={{
                fontSize: '1.125rem',
                fontWeight: '600',
                color: 'var(--text-primary)',
                marginBottom: '0.5rem'
              }}>
                {feature.title}
              </h3>
              <p style={{
                fontSize: '0.875rem',
                color: 'var(--text-secondary)',
                lineHeight: '1.5',
                margin: '0'
              }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        <div style={{
          textAlign: 'center',
          padding: '1rem',
          background: 'var(--gradient-card)',
          border: '1px solid var(--border-color)',
          borderRadius: '0.75rem'
        }}>
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: '600',
            color: 'var(--text-primary)',
            marginBottom: '0.5rem'
          }}>
            Ready to Improve Your Code?
          </h3>
          <p style={{
            color: 'var(--text-secondary)',
            marginBottom: '1rem',
            fontSize: '0.875rem'
          }}>
            Upload your code files and get instant analysis results
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
            fontSize: '0.875rem',
            transition: 'transform 0.2s ease'
          }} onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'} onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Start Analysis
          </a>
        </div>
      </div>
    </section>
  );
};

export default Features;
