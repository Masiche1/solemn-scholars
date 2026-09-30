import type { ReactNode } from "react";

/** Standard screen header used across the authenticated app. */
export function PageHead({
  eyebrow,
  title,
  description,
  actions,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <div className="rh-screen-head">
      <div className="rh-cluster" style={{ justifyContent: "space-between", alignItems: "flex-end", gap: 16, flexWrap: "wrap" }}>
        <div>
          {eyebrow && <span className="rh-eyebrow">{eyebrow}</span>}
          <h1 className="rh-display rh-t-h1">{title}</h1>
          {description && <p className="rh-t-body-l rh-muted" style={{ marginTop: 8 }}>{description}</p>}
        </div>
        {actions}
      </div>
    </div>
  );
}

export function QueryError({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  const message = error instanceof Error ? error.message : "Something went wrong.";
  return (
    <div role="alert">
      <div className="rh-error-box">{message}</div>
      {onRetry && (
        <button type="button" className="rh-btn" style={{ marginTop: 12 }} onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}
