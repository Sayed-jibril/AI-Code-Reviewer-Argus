import React from 'react';

const Hero: React.FC = () => {
  return (
    <section style={{
      position: 'relative',
      overflow: 'hidden',
      padding: '3rem 0'
    }}>
      {/* Background Gradient */}
      <div style={{
        position: 'absolute',
        inset: '0',
        background: 'linear-gradient(to bottom right, var(--primary-bg), var(--secondary-bg), var(--tertiary-bg))'
      }}></div>
      
      {/* Animated Background Elements */}
      <div style={{
        position: 'absolute',
        inset: '0',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: '-10rem',
          right: '-10rem',
          width: '20rem',
          height: '20rem',
          background: 'var(--accent-primary)',
          opacity: '0.1',
          borderRadius: '50%',
          filter: 'blur(24px)'
        }}></div>
        <div style={{
          position: 'absolute',
          bottom: '-10rem',
          left: '-10rem',
          width: '20rem',
          height: '20rem',
          background: 'var(--accent-secondary)',
          opacity: '0.1',
          borderRadius: '50%',
          filter: 'blur(24px)'
        }}></div>
      </div>

      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 1.5rem',
        position: 'relative',
        zIndex: '10'
      }}>
        <div style={{
          textAlign: 'center',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          {/* Main Heading */}
          <h1 style={{
            fontSize: '3rem',
            fontWeight: 'bold',
            marginBottom: '1rem',
            lineHeight: '1.2'
          }}>
            <span style={{
              background: 'var(--gradient-primary)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>PolySpector</span>
            <br />
            <span style={{ color: 'var(--text-primary)' }}>AI Code Reviewer</span>
          </h1>
          
          {/* Subtitle */}
          <p style={{
            fontSize: '1.125rem',
            color: 'var(--text-secondary)',
            marginBottom: '1.5rem',
            lineHeight: '1.5'
          }}>
            Advanced static analysis for <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>41+ programming languages</span>
            <br />
            Detect security vulnerabilities, performance issues, and code quality problems
          </p>

          {/* CTA Buttons */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            justifyContent: 'center',
            marginBottom: '2rem'
          }}>
            <a href="#upload" style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              padding: '0.75rem 1.5rem',
              background: 'var(--gradient-primary)',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '0.5rem',
              fontWeight: '500',
              fontSize: '1rem',
              transition: 'transform 0.2s ease'
            }} onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'} onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Start Code Review
            </a>
            <a href="#languages" style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              padding: '0.75rem 1.5rem',
              background: 'var(--card-bg)',
              color: 'var(--text-primary)',
              textDecoration: 'none',
              borderRadius: '0.5rem',
              fontWeight: '500',
              fontSize: '1rem',
              border: '1px solid var(--border-color)',
              transition: 'transform 0.2s ease'
            }} onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'} onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              View Languages
            </a>
          </div>

          {/* Stats */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '1rem',
            marginBottom: '1.5rem'
          }}>
            <div style={{
              background: 'var(--gradient-card)',
              border: '1px solid var(--border-color)',
              borderRadius: '0.5rem',
              padding: '1rem',
              textAlign: 'center'
            }}>
              <div style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: 'var(--accent-primary)',
                marginBottom: '0.25rem'
              }}>41+</div>
              <div style={{
                fontSize: '0.875rem',
                color: 'var(--text-secondary)'
              }}>Languages</div>
            </div>
            <div style={{
              background: 'var(--gradient-card)',
              border: '1px solid var(--border-color)',
              borderRadius: '0.5rem',
              padding: '1rem',
              textAlign: 'center'
            }}>
              <div style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: 'var(--accent-success)',
                marginBottom: '0.25rem'
              }}>100+</div>
              <div style={{
                fontSize: '0.875rem',
                color: 'var(--text-secondary)'
              }}>Rules</div>
            </div>
            <div style={{
              background: 'var(--gradient-card)',
              border: '1px solid var(--border-color)',
              borderRadius: '0.5rem',
              padding: '1rem',
              textAlign: 'center'
            }}>
              <div style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: 'var(--accent-info)',
                marginBottom: '0.25rem'
              }}>24/7</div>
              <div style={{
                fontSize: '0.875rem',
                color: 'var(--text-secondary)'
              }}>Analysis</div>
            </div>
          </div>

          {/* Trust Indicators */}
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '1rem',
            color: 'var(--text-muted)',
            fontSize: '0.875rem'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <svg width="16" height="16" fill="var(--accent-success)" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Secure & Private</span>
            </div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <svg width="16" height="16" fill="var(--accent-success)" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>No Code Execution</span>
            </div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <svg width="16" height="16" fill="var(--accent-success)" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Free to Use</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
