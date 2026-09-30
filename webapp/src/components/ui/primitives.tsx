import { cn } from "@/lib/utils";
import type {
  ButtonHTMLAttributes,
  CSSProperties,
  HTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";

/* ---------------------------------- Button --------------------------------- */

type ButtonVariant =
  | "primary"
  | "accent"
  | "secondary"
  | "ghost"
  | "on-ink"
  | "danger"
  | "newton"
  | "success-quiet"
  | "warning-quiet"
  | "danger-quiet";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: "sm" | "md" | "lg";
  block?: boolean;
  icon?: ReactNode;
}

export function Button({
  variant = "secondary",
  size = "md",
  block,
  icon,
  className,
  children,
  type = "button",
  ...rest
}: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(
        "rh-btn",
        variant !== "secondary" && `rh-btn--${variant}`,
        size !== "md" && `rh-btn--${size}`,
        block && "rh-btn--block",
        className,
      )}
      {...rest}
    >
      {icon}
      {children}
    </button>
  );
}

/* ----------------------------------- Card ---------------------------------- */

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  interactive?: boolean;
  lg?: boolean;
  sunk?: boolean;
  padded?: boolean;
}

export function Card({ interactive, lg, sunk, padded, className, children, ...rest }: CardProps) {
  return (
    <div
      className={cn(
        "rh-card",
        interactive && "rh-card--interactive",
        lg && "rh-card--lg",
        sunk && "rh-card--sunk",
        padded && "rh-card--padded",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export function CardHead({
  title,
  actions,
  className,
}: {
  title: ReactNode;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("rh-card__head", className)}>
      <div className="rh-card__title">{title}</div>
      {actions && <div className="rh-card__actions">{actions}</div>}
    </div>
  );
}

export function CardBody({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn("rh-card__body", className)}>{children}</div>;
}

export function CardFoot({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn("rh-card__foot", className)}>{children}</div>;
}

/* ----------------------------------- Badge --------------------------------- */

type BadgeTone =
  | "violet"
  | "cyan"
  | "success"
  | "warning"
  | "danger"
  | "ink"
  | "outline"
  | "ai"
  | "pyp"
  | "myp"
  | "dp"
  | "mastered"
  | "developing"
  | "review"
  | "new";

export function Badge({
  tone = "violet",
  dot,
  className,
  children,
  ...rest
}: {
  tone?: BadgeTone;
  dot?: boolean;
  className?: string;
  children: ReactNode;
} & HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn("rh-badge", tone !== "violet" && `rh-badge--${tone}`, dot && "rh-badge--dot", className)}
      {...rest}
    >
      {children}
    </span>
  );
}

/* ---------------------------------- Field ---------------------------------- */

export function Field({
  label,
  hint,
  error,
  className,
  children,
}: {
  label?: string;
  hint?: string;
  error?: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <label className={cn("rh-field", error && "rh-field--error", className)}>
      {label && <span className="rh-field__label">{label}</span>}
      {children}
      {hint && !error && <span className="rh-field__hint">{hint}</span>}
      {error && <span className="rh-field__error">{error}</span>}
    </label>
  );
}

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input className={cn("rh-input", props.className)} {...props} />;
}

export function Textarea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea className={cn("rh-textarea", props.className)} {...props} />;
}

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return <select className={cn("rh-select", props.className)} {...props} />;
}

/* --------------------------------- Progress -------------------------------- */

export function Progress({
  value,
  size,
  journey,
  label,
  className,
}: {
  value: number;
  size?: "sm";
  journey?: boolean;
  label?: string;
  className?: string;
}) {
  const pct = Math.max(0, Math.min(100, Math.round(value)));
  return (
    <div className={cn("rh-progress", size === "sm" && "rh-progress--sm", journey && "rh-progress--journey", className)}>
      {label && <div className="rh-progress__label">{label}</div>}
      <div className="rh-progress__track" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <div className="rh-progress__bar" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

/* ----------------------------------- Tabs ---------------------------------- */

export function Tabs({ className, style, children }: { className?: string; style?: CSSProperties; children: ReactNode }) {
  return (
    <div className={cn("rh-tabs", className)} style={style} role="tablist">
      {children}
    </div>
  );
}

export function Tab({ selected, className, children, ...rest }: { selected?: boolean } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button type="button" role="tab" aria-selected={selected} className={cn("rh-tab", className)} {...rest}>
      {children}
    </button>
  );
}

/* ---------------------------------- Kbd ------------------------------------ */

export function Kbd({ children }: { children: ReactNode }) {
  return <kbd className="rh-kbd">{children}</kbd>;
}

/* --------------------------------- Avatar ---------------------------------- */

export function Avatar({ initials, className }: { initials: string; className?: string }) {
  return <span className={cn("rh-avatar", className)}>{initials}</span>;
}

/* --------------------------------- States ---------------------------------- */

export function Spinner({ size, className }: { size?: "lg"; className?: string }) {
  return (
    <span
      className={cn("rh-spinner", size === "lg" && "rh-spinner--lg", className)}
      role="status"
      aria-label="Loading"
    />
  );
}

export function Skeleton({ className, style }: { className?: string; style?: CSSProperties }) {
  return <span className={cn("rh-skeleton", className)} style={style} />;
}

export function EmptyState({
  icon,
  title,
  description,
  action,
  className,
}: {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("rh-empty", className)}>
      {icon && <span className="rh-empty__icon">{icon}</span>}
      <h3 style={{ margin: 0 }}>{title}</h3>
      {description && <p style={{ margin: 0, maxWidth: "48ch" }}>{description}</p>}
      {action}
    </div>
  );
}

export function ErrorBox({ children, className, style }: { children: ReactNode; className?: string; style?: CSSProperties }) {
  return <div className={cn("rh-error-box", className)} style={style}>{children}</div>;
}

/* --------------------------------- Section --------------------------------- */

export function Section({
  title,
  link,
  className,
  children,
}: {
  title?: string;
  link?: ReactNode;
  className?: string;
  children: ReactNode;
}) {
  return (
    <section className={cn("rh-section", className)}>
      {(title || link) && (
        <div className="rh-section__head">
          {title && <h2 className="rh-section__title">{title}</h2>}
          {link && <div className="rh-section__link">{link}</div>}
        </div>
      )}
      {children}
    </section>
  );
}
