import Link from "next/link";

export default function NotFound() {
  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 24, textAlign: "center" }}>
      <div style={{ maxWidth: 440 }}>
        <p className="rh-eyebrow">404</p>
        <h1 className="rh-display rh-t-h1">Page not found</h1>
        <p className="rh-t-body-l rh-muted" style={{ margin: "12px 0 24px" }}>
          The page you&apos;re looking for doesn&apos;t exist or has moved.
        </p>
        <div className="rh-cluster" style={{ justifyContent: "center", gap: 12 }}>
          <Link href="/dashboard" className="rh-btn rh-btn--primary">Go to dashboard</Link>
          <Link href="/" className="rh-btn">Home</Link>
        </div>
      </div>
    </main>
  );
}
