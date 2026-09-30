"use client";

/** Last-resort boundary: replaces the root layout, so it must render its own <html>/<body> and can't rely on app CSS. */
export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif", display: "grid", placeItems: "center", minHeight: "100vh", padding: 24, textAlign: "center" }}>
        <div style={{ maxWidth: 440 }}>
          <h1 style={{ fontSize: 28, margin: "0 0 12px" }}>Something went wrong</h1>
          <p style={{ color: "#64748b", margin: "0 0 24px" }}>An unexpected error occurred{error.digest ? ` (ref ${error.digest})` : ""}.</p>
          <button type="button" onClick={reset} style={{ padding: "10px 20px", borderRadius: 10, border: 0, background: "#7C3AED", color: "#fff", fontWeight: 700, cursor: "pointer" }}>
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
