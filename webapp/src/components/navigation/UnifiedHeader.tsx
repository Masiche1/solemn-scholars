"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function UnifiedHeader() {
  const [activePlatform, setActivePlatform] = useState<'revisions' | 'tutors'>('revisions');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const revisionsNav = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Courses', href: '/courses' },
    { name: 'Practice', href: '/practice' },
    { name: 'Results', href: '/results' },
    { name: 'Newton', href: '/newton' },
  ];

  const tutorsNav = [
    { name: 'Find Tutors', href: '/tutors' },
    { name: 'Post a Job', href: '/jobs/post' },
    { name: 'Become a Tutor', href: '/tutors/become' },
  ];

  const currentNav = activePlatform === 'revisions' ? revisionsNav : tutorsNav;

  return (
    <header className="ss-header">
      <div className="ss-header-inner">
        {/* Logo */}
        <Link href="/" className="ss-logo">
          <div className="ss-logo-mark">SS</div>
          <span>Solemn Scholars</span>
        </Link>

        {/* Platform Switcher */}
        <div className="ss-platform-switcher">
          <button
            className={`ss-platform-btn ${activePlatform === 'revisions' ? 'active' : ''}`}
            onClick={() => setActivePlatform('revisions')}
          >
            Revisions Hub
          </button>
          <button
            className={`ss-platform-btn ${activePlatform === 'tutors' ? 'active' : ''}`}
            onClick={() => setActivePlatform('tutors')}
          >
            Tutors Hub
          </button>
        </div>

        {/* Navigation */}
        <nav className="ss-nav">
          {currentNav.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="nav-link"
            >
              {item.name}
            </Link>
          ))}
        </nav>

        {/* CTA Buttons */}
        <div className="ss-header-cta">
          <button className="ss-btn ss-btn--ghost ss-btn--sm">Sign In</button>
          <button className="ss-btn ss-btn--primary ss-btn--sm">Get Started</button>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          className="ss-menu-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="ss-mobile-menu">
          <div className="ss-platform-switcher ss-mobile-platform-switcher">
            <button
              className={`ss-platform-btn ${activePlatform === 'revisions' ? 'active' : ''}`}
              onClick={() => setActivePlatform('revisions')}
            >
              Revisions Hub
            </button>
            <button
              className={`ss-platform-btn ${activePlatform === 'tutors' ? 'active' : ''}`}
              onClick={() => setActivePlatform('tutors')}
            >
              Tutors Hub
            </button>
          </div>
          <nav className="ss-mobile-nav">
            {currentNav.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="ss-mobile-nav-link"
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          </nav>
          <div className="ss-mobile-cta">
            <button className="ss-btn ss-btn--ghost ss-btn--block">Sign In</button>
            <button className="ss-btn ss-btn--primary ss-btn--block">Get Started</button>
          </div>
        </div>
      )}
    </header>
  );
}
