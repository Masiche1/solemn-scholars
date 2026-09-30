import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes + conditional classes (shadcn-style). */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/* ---------------------------------- labels --------------------------------- */

export const PROGRAMME_LABELS: Record<string, string> = {
  pyp: "PYP",
  myp: "MYP",
  dp: "DP",
};

export function programmeLabel(id: string): string {
  return PROGRAMME_LABELS[id] ?? id.toUpperCase();
}

export function programmeName(p: { name: string; fullName?: string | null }): string {
  return p.fullName || p.name;
}

/** "Sciences — Biology" -> "Biology" (drop the learning-area prefix). */
export function prettifySubjectName(name: string): string {
  // Names look like "Mathematics — Mathematics" or "Sciences — Biology".
  const parts = name.split(/\s*[—–-]\s*/).filter(Boolean);
  if (parts.length >= 2) {
    const subject = parts[parts.length - 1].trim();
    const track = parts[parts.length - 2].trim();
    // e.g. "Mathematics — Mathematics" collapses to "Mathematics"
    if (subject.toLowerCase() === track.toLowerCase()) return subject;
    return subject;
  }
  return name.trim();
}

/**
 * Map a subject-group id/name or topic id to the design-system accent key
 * used by [data-subject="…"] selectors (mathematics/biology/chemistry/…).
 * Returns undefined when no known accent applies (attribute is then omitted).
 */
export function subjectKey(subjectOrTopic: string): string | undefined {
  const k = subjectOrTopic.toLowerCase();
  if (k.includes("math")) return "mathematics";
  if (k.includes("bio")) return "biology";
  if (k.includes("chem")) return "chemistry";
  if (k.includes("phys")) return "physics";
  if (k.includes("business") || k.includes("management")) return "business";
  if (k.includes("econ")) return "economics";
  if (k.includes("psych")) return "psychology";
  if (k.includes("histor")) return "history";
  if (k.includes("literature")) return "literature";
  if (k.includes("english")) return "english-b";
  if (k.includes("spanish")) return "spanish-b";
  if (k.includes("french")) return "french-b";
  if (k.includes("language")) return "lang-lit";
  if (k.includes("tok")) return "tok";
  return undefined;
}

export function subjectAccent(subjectOrGroup: string): string | undefined {
  // Map a subject group id/name to a known accent token, if any.
  const key = subjectOrGroup.toLowerCase();
  const map: Record<string, string> = {
    mathematics: "violet",
    "math-analysis": "violet",
    sciences: "cyan",
    biology: "cyan",
    chemistry: "cyan",
    physics: "cyan",
    "computer-science": "cyan",
    english: "amber",
    humanities: "amber",
    history: "amber",
    geography: "amber",
    economics: "amber",
    arts: "rose",
    "visual-arts": "rose",
    music: "rose",
    "language-aquisition": "rose",
    individuals: "amber",
  };
  for (const [needle, accent] of Object.entries(map)) {
    if (key.includes(needle)) return accent;
  }
  return undefined;
}

/* --------------------------------- numbers --------------------------------- */

export function fmtPct(n: number | null | undefined, fallback = "—"): string {
  if (n === null || n === undefined || Number.isNaN(n)) return fallback;
  return `${Math.round(n)}%`;
}

export function fmtDuration(sec: number | null | undefined): string {
  if (sec === null || sec === undefined || Number.isNaN(sec)) return "—";
  const m = Math.floor(sec / 60);
  const s = Math.round(sec % 60);
  return s >= 10 ? `${m}:${s}` : `${m}:0${s}`;
}

export function fmtClock(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}`;
}

export function fmtMoney(amount: number, currency: string): string {
  const cur = currency?.toUpperCase() === "USD" ? "USD" : currency?.toUpperCase() === "KES" ? "KES" : currency || "";
  if (cur === "USD") return `$${(amount / 100).toLocaleString("en-US")}`;
  if (cur === "KES") return `KES ${(amount / 100).toLocaleString("en-KE")}`;
  return `${cur} ${(amount / 100).toLocaleString()}`;
}

export function fmtDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function fmtDateTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}

export function relativeTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso).getTime();
  if (Number.isNaN(d)) return "—";
  const diff = Date.now() - d;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 50);
  if (days < 7) return `${days}d ago`;
  return fmtDate(iso);
}

/* --------------------------------- session --------------------------------- */

export const SESSION_KIND_LABELS: Record<string, string> = {
  "quick-practice": "Quick Practice",
  mock_exam: "Mock Exam",
  exam: "Exam",
  revision: "Revision",
  diagnostic: "Diagnostic",
  homework: "Homework",
  "topic-practice": "Topic Practice",
  "weakness-drill": "Weakness Drill",
  mastery: "Mastery",
  challenge: "Challenge",
};

export function sessionKindLabel(kind: string): string {
  return SESSION_KIND_LABELS[kind] ?? kind.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function difficultyLabel(d: string): string {
  if (d === "mixed") return "Mixed";
  return d.charAt(0).toUpperCase() + d.slice(1);
}

/* ------------------------------- status dots ------------------------------- */

export function answerStateLabel(state: string | null | undefined): string {
  switch (state) {
    case "correct": return "Correct";
    case "incorrect": return "Incorrect";
    case "skipped": return "Skipped";
    case "answered": return "Answered";
    case "flagged": return "Flagged";
    case "unanswered": return "Unanswered";
    default: return state ?? "—";
  }
}

/* ------------------------------- subject accent ---------------------------- */

export function slugToTitle(slug: string): string {
  return slug
    .split("-")
    .map((w) => (w.length <= 3 ? w.toUpperCase() : w.charAt(0).toUpperCase() + w.slice(1)))
    .join(" ");
}

/* ------------------------- question payload helpers ------------------------ */

/** Options arrive as `{key,text}[]` (DB shape) or a key→text record; always return `[key, text][]`. */
export function normalizeOptions(options: unknown): [string, string][] {
  if (!options) return [];
  if (Array.isArray(options)) {
    return options
      .filter((o): o is { key: unknown; text: unknown } => !!o && typeof o === "object")
      .map((o, i) => [String(o.key ?? String.fromCharCode(65 + i)), String(o.text ?? "")] as [string, string]);
  }
  if (typeof options === "object") {
    return Object.entries(options as Record<string, unknown>).map(([k, v]) => [k, String(v)] as [string, string]);
  }
  return [];
}

/** Stimulus may be plain text or a JSON blob (passage / table / graph spec). Returns display text or null. */
export function stimulusText(stimulus: unknown): string | null {
  if (stimulus === null || stimulus === undefined || stimulus === "") return null;
  if (typeof stimulus === "string") return stimulus;
  if (typeof stimulus === "object") {
    const o = stimulus as Record<string, unknown>;
    for (const k of ["text", "passage", "content", "description", "caption"]) {
      if (typeof o[k] === "string" && o[k]) return o[k] as string;
    }
    if (Object.keys(o).length === 0) return null;
    return JSON.stringify(o, null, 2);
  }
  return String(stimulus);
}

export function questionTypeLabel(t: string): string {
  return t.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
