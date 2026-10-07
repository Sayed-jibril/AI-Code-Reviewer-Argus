import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer style={{
      backgroundColor: 'var(--secondary-bg)',
      borderTop: '1px solid var(--border-color)',
      marginTop: '5rem',
      padding: '3rem 0 2rem 0'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 1.5rem'
      }}>
        {/* Main Footer Content */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '2rem',
          marginBottom: '2rem'
        }}>
          {/* Brand Section */}
          <div style={{ gridColumn: 'span 2' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              marginBottom: '1rem'
            }}>
              <div style={{
                width: '2.5rem',
                height: '2.5rem',
                background: 'var(--gradient-primary)',
                borderRadius: '0.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <span style={{
                  color: 'white',
                  fontWeight: 'bold',
                  fontSize: '1.25rem'
                }}>P</span>
              </div>
              <div>
                <h3 style={{
                  fontSize: '1.25rem',
                  fontWeight: 'bold',
                  background: 'var(--gradient-primary)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                  margin: '0 0 0.25rem 0'
                }}>PolySpector</h3>
                <p style={{
                  fontSize: '0.875rem',
                  color: 'var(--text-muted)',
                  margin: '0'
                }}>AI Code Reviewer</p>
              </div>
            </div>
            <p style={{
              color: 'var(--text-secondary)',
              marginBottom: '1.5rem',
              maxWidth: '28rem',
              lineHeight: '1.6'
            }}>
              Advanced AI-powered code review tool supporting 41+ programming languages. 
              Detect security vulnerabilities, performance issues, and code quality problems 
              with comprehensive static analysis.
            </p>
            <div style={{
              display: 'flex',
              gap: '1rem'
            }}>
              <a href="https://github.com/ethiha-naing-18-ellison" target="_blank" rel="noopener noreferrer" style={{
                color: 'var(--text-muted)',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}>
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a href="https://www.linkedin.com/in/thiha-naing-18t43" target="_blank" rel="noopener noreferrer" style={{
                color: 'var(--text-muted)',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}>
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 style={{
              fontSize: '1.125rem',
              fontWeight: '600',
              color: 'var(--text-primary)',
              marginBottom: '1rem',
              marginTop: '0'
            }}>Quick Links</h4>
            <ul style={{
              listStyle: 'none',
              padding: '0',
              margin: '0'
            }}>
              {[
                { href: '#features', text: 'Features' },
                { href: '#languages', text: 'Supported Languages' },
                { href: '#demo', text: 'Try Demo' },
                { href: '#upload', text: 'Start Review' },
                { href: '#docs', text: 'Documentation' }
              ].map((link, index) => (
                <li key={index} style={{ marginBottom: '0.5rem' }}>
                  <a href={link.href} style={{
                    color: 'var(--text-secondary)',
                    textDecoration: 'none',
                    transition: 'color 0.15s ease-in-out'
                  }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
                    {link.text}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Information */}
          <div>
            <h4 style={{
              fontSize: '1.125rem',
              fontWeight: '600',
              color: 'var(--text-primary)',
              marginBottom: '1rem',
              marginTop: '0'
            }}>Contact</h4>
            <div style={{
              color: 'var(--text-secondary)',
              fontSize: '0.875rem',
              lineHeight: '1.6'
            }}>
              <p style={{ margin: '0 0 0.5rem 0', fontWeight: '600', color: 'var(--text-primary)' }}>
                Thiha Naing
              </p>
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Software Engineer, Data Analyst
              </p>
              <div style={{ marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: '500' }}>📧</span> 
                <a href="mailto:thiha.naing.codev@gmail.com" style={{
                  color: 'var(--text-secondary)',
                  textDecoration: 'none',
                  marginLeft: '0.5rem',
                  transition: 'color 0.15s ease-in-out'
                }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
                  thiha.naing.codev@gmail.com
                </a>
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: '500' }}>📱</span> 
                <a href="tel:+60187799581" style={{
                  color: 'var(--text-secondary)',
                  textDecoration: 'none',
                  marginLeft: '0.5rem',
                  transition: 'color 0.15s ease-in-out'
                }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
                  +60 18-779 9581
                </a>
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: '500' }}>🔗</span> 
                <a href="https://github.com/ethiha-naing-18-ellison" target="_blank" rel="noopener noreferrer" style={{
                  color: 'var(--text-secondary)',
                  textDecoration: 'none',
                  marginLeft: '0.5rem',
                  transition: 'color 0.15s ease-in-out'
                }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
                  GitHub
                </a>
              </div>
              <div>
                <span style={{ fontWeight: '500' }}>💼</span> 
                <a href="https://www.linkedin.com/in/thiha-naing-18t43" target="_blank" rel="noopener noreferrer" style={{
                  color: 'var(--text-secondary)',
                  textDecoration: 'none',
                  marginLeft: '0.5rem',
                  transition: 'color 0.15s ease-in-out'
                }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--accent-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
                  LinkedIn
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div style={{
          borderTop: '1px solid var(--border-color)',
          paddingTop: '2rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <p style={{
            color: 'var(--text-muted)',
            fontSize: '0.875rem',
            margin: '0'
          }}>
            © 2024 PolySpector. All rights reserved.
          </p>
          <div style={{
            display: 'flex',
            gap: '1.5rem'
          }}>
            {[
              { href: '#terms', text: 'Terms of Service' },
              { href: '#privacy', text: 'Privacy Policy' },
              { href: '#cookies', text: 'Cookie Policy' }
            ].map((link, index) => (
              <a key={index} href={link.href} style={{
                color: 'var(--text-muted)',
                fontSize: '0.875rem',
                textDecoration: 'none',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}>
                {link.text}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
