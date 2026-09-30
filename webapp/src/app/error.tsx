"use client";

import { useEffect } from "react";

export default function RootError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    // Hook point for an error reporting service (Sentry etc.)
    console.error(error);
  }, [error]);

  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 24, textAlign: "center" }}>
      <div style={{ maxWidth: 460 }}>
        <p className="rh-eyebrow">Something went wrong</p>
        <h1 className="rh-display rh-t-h1">We hit an unexpected error</h1>
        <p className="rh-t-body-l rh-muted" style={{ margin: "12px 0 24px" }}>
          Please try again. If it keeps happening, contact support{error.digest ? ` and quote ${error.digest}` : ""}.
        </p>
        <button type="button" className="rh-btn rh-btn--primary" onClick={reset}>Try again</button>
      </div>
    </main>
  );
}
