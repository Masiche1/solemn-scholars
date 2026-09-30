"use client";

import Link from "next/link";
import { useTheme } from "@/components/providers";
import { BrandMark, Icon, NewtonMark } from "@/components/brand";

export function MarketingShell({ children }: { children: React.ReactNode }) {
  const { theme, toggle } = useTheme();

  return (
    <div className="rh-mkt">
      <header className="rh-mkt__nav">
        <Link href="/" className="rh-cluster" style={{ gap: 10, textDecoration: "none", color: "inherit" }}>
          <BrandMark size={36} />
          <span className="rh-display" style={{ fontSize: 17 }}>
            Revisions Hub
          </span>
        </Link>
        <nav className="rh-mkt__navlinks">
          <Link href="/#programmes">Programmes</Link>
          <Link href="/#newton">Newton AI</Link>
          <Link href="/#features">Features</Link>
          <Link href="/#pricing">Pricing</Link>
          <Link href="/dashboard" style={{ color: "var(--rh-violet-hover)" }}>
            Live demo →
          </Link>
        </nav>
        <div className="rh-cluster" style={{ gap: 8, marginLeft: "auto" }}>
          <button
            type="button"
            className="rh-theme-toggle"
            onClick={toggle}
            style={{ width: 32, height: 32 }}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <Icon name="sun" size={16} /> : <Icon name="moon" size={16} />}
          </button>
          <Link href="/dashboard" className="rh-btn rh-btn--secondary rh-btn--sm">
            Sign in
          </Link>
          <Link href="/subscription" className="rh-btn rh-btn--primary rh-btn--sm">
            Start free
          </Link>
        </div>
      </header>

      {children}

      <MarketingFooter />
    </div>
  );
}

function MarketingFooter() {
  return (
    <footer className="rh-mkt__foot">
      <div className="rh-mkt__footgrid">
        <div>
          <div className="rh-cluster" style={{ gap: 10, marginBottom: 12 }}>
            <BrandMark size={34} />
            <span className="rh-display" style={{ fontSize: 16, color: "#F8FAFC" }}>
              Revisions Hub
            </span>
          </div>
          <p className="rh-t-caption" style={{ maxWidth: 280, margin: 0 }}>
            The premium academic intelligence platform for the IB continuum. Not affiliated with the International Baccalaureate Organization.
          </p>
        </div>
        <div style={{ display: "grid", gap: 8, alignContent: "start" }}>
          <div
            className="rh-t-caption"
            style={{ fontWeight: 800, textTransform: "uppercase", letterSpacing: ".08em", color: "#64748B" }}
          >
            Product
          </div>
          <Link href="/dashboard">Live demo</Link>
          <Link href="/#programmes">Programmes</Link>
          <Link href="/newton">Newton AI</Link>
          <Link href="/#pricing">Pricing</Link>
        </div>
        <div style={{ display: "grid", gap: 8, alignContent: "start" }}>
          <div
            className="rh-t-caption"
            style={{ fontWeight: 800, textTransform: "uppercase", letterSpacing: ".08em", color: "#64748B" }}
          >
            Design
          </div>
          <Link href="/dashboard">App shell</Link>
          <Link href="/questionbank">Questionbank</Link>
          <Link href="/practice">Practice lab</Link>
          <Link href="/results">Results</Link>
        </div>
        <div style={{ display: "grid", gap: 8, alignContent: "start" }}>
          <div
            className="rh-t-caption"
            style={{ fontWeight: 800, textTransform: "uppercase", letterSpacing: ".08em", color: "#64748B" }}
          >
            Company
          </div>
          <a href="#">About</a>
          <a href="#">Contact</a>
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
        </div>
      </div>
      <div
        className="rh-mkt__container rh-space-between"
        style={{ marginTop: 40, paddingTop: 20, borderTop: "1px solid rgba(148,163,184,.18)", alignItems: "center" }}
      >
        <span className="rh-t-caption">© 2025 Revisions Hub · Learn deeper. Practice smarter. Master your IB journey.</span>
        <span className="rh-t-caption">Made with Ink, Ivory, Violet &amp; Cyan.</span>
      </div>
    </footer>
  );
}
