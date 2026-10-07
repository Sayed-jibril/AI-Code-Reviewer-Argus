import React, { useState } from 'react';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header style={{
      position: 'sticky',
      top: '0',
      zIndex: '50',
      background: 'var(--primary-bg)',
      borderBottom: '1px solid var(--border-color)',
      backdropFilter: 'blur(10px)',
      backgroundColor: 'rgba(17, 24, 39, 0.95)'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 1.5rem'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '4rem'
        }}>
          {/* Logo */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem'
          }}>
            <div style={{
              width: '2rem',
              height: '2rem',
              background: 'var(--gradient-primary)',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <span style={{
                color: 'white',
                fontWeight: 'bold',
                fontSize: '1rem'
              }}>P</span>
            </div>
            <div>
              <h1 style={{
                fontSize: '1.25rem',
                fontWeight: 'bold',
                background: 'var(--gradient-primary)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                margin: '0'
              }}>PolySpector</h1>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav style={{
            display: 'none',
            alignItems: 'center',
            gap: '2rem'
          }} className="hidden md:flex">
            <a href="#features" style={{
              color: 'var(--text-secondary)',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: '500',
              transition: 'color 0.15s ease-in-out'
            }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
              Features
            </a>
            <a href="#languages" style={{
              color: 'var(--text-secondary)',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: '500',
              transition: 'color 0.15s ease-in-out'
            }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
              Languages
            </a>
            <a href="#upload" style={{
              color: 'var(--text-secondary)',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: '500',
              transition: 'color 0.15s ease-in-out'
            }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}>
              Review
            </a>
          </nav>

          {/* CTA Buttons */}
          <div style={{
            display: 'none',
            alignItems: 'center',
            gap: '1rem'
          }} className="hidden md:flex">
            <a href="#upload" style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.5rem 1rem',
              background: 'var(--gradient-primary)',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '0.5rem',
              fontWeight: '500',
              fontSize: '0.875rem',
              transition: 'transform 0.2s ease'
            }} onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-1px)'} onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Start Review
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '0.25rem',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem'
            }} className="md:hidden"
          >
            <span style={{
              width: '1.5rem',
              height: '0.125rem',
              background: 'var(--text-primary)',
              transition: 'transform 0.3s ease'
            }} className={isMenuOpen ? 'rotate-45 translate-y-1' : ''}></span>
            <span style={{
              width: '1.5rem',
              height: '0.125rem',
              background: 'var(--text-primary)',
              transition: 'opacity 0.3s ease'
            }} className={isMenuOpen ? 'opacity-0' : ''}></span>
            <span style={{
              width: '1.5rem',
              height: '0.125rem',
              background: 'var(--text-primary)',
              transition: 'transform 0.3s ease'
            }} className={isMenuOpen ? '-rotate-45 -translate-y-1' : ''}></span>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div style={{
            padding: '1rem 0',
            borderTop: '1px solid var(--border-color)'
          }}>
            <nav style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}>
              <a href="#features" style={{
                color: 'var(--text-secondary)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                fontWeight: '500',
                padding: '0.5rem 0',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'} onClick={() => setIsMenuOpen(false)}>
                Features
              </a>
              <a href="#languages" style={{
                color: 'var(--text-secondary)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                fontWeight: '500',
                padding: '0.5rem 0',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'} onClick={() => setIsMenuOpen(false)}>
                Languages
              </a>
              <a href="#upload" style={{
                color: 'var(--text-secondary)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                fontWeight: '500',
                padding: '0.5rem 0',
                transition: 'color 0.15s ease-in-out'
              }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-secondary)'} onClick={() => setIsMenuOpen(false)}>
                Review
              </a>
              <a href="#upload" style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                padding: '0.75rem 1rem',
                background: 'var(--gradient-primary)',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '0.5rem',
                fontWeight: '500',
                fontSize: '0.875rem',
                marginTop: '0.5rem'
              }} onClick={() => setIsMenuOpen(false)}>
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Start Review
              </a>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
