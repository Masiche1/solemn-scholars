"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import { api, type Role, DEV_AUTH } from "@/lib/api";
import { useDevRole, useMe, useTheme } from "@/components/providers";
import { BrandMark, Icon, NewtonMark, type IconName } from "@/components/brand";
import { cn, programmeLabel } from "@/lib/utils";

/* ---------------------------------- nav data -------------------------------- */

const NAV: { label: string; items: { href: string; label: string; icon: IconName; newton?: boolean }[] }[] = [
  {
    label: "Learn",
    items: [
      { href: "/dashboard", label: "Dashboard", icon: "grid" },
      { href: "/courses", label: "My Learning", icon: "book" },
      { href: "/practice", label: "Practice", icon: "target" },
      { href: "/results", label: "Results", icon: "clipboard" },
      { href: "/questionbank", label: "Questionbank", icon: "db" },
    ],
  },
  {
    label: "Intelligence",
    items: [
      { href: "/newton", label: "Newton AI", icon: "zap", newton: true },
      { href: "/profile", label: "Profile", icon: "settings" },
      { href: "/subscription", label: "Subscription", icon: "folder" },
    ],
  },
];

const ADMIN_NAV: { href: string; label: string; icon: IconName } = { href: "/admin", label: "Admin", icon: "users" };

const BOTTOM_NAV: { href: string; label: string; icon: IconName }[] = [
  { href: "/dashboard", label: "Home", icon: "grid" },
  { href: "/courses", label: "Learn", icon: "book" },
  { href: "/practice", label: "Practice", icon: "target" },
  { href: "/newton", label: "Newton", icon: "zap" },
];

const ROLES: Role[] = ["student", "teacher", "school_admin", "parent", "platform_admin"];

export function roleLabel(role: string): string {
  const map: Record<string, string> = {
    student: "Student",
    teacher: "Teacher",
    school_admin: "School Admin",
    parent: "Parent",
    platform_admin: "Platform Admin",
  };
  return map[role] ?? role;
}

/* ---------------------------------- shell ---------------------------------- */

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { data: me } = useMe();
  const user = me?.user;

  const programme = useMemo(() => user?.programme ?? "dp", [user?.programme]);

  return (
    <div className="rh-app">
      <Sidebar programme={programme} pathname={pathname} isAdmin={user?.authRole === "platform_admin" || user?.authRole === "school_admin"} />
      <div className="rh-app__main">
        <TopBar />
        <main className="rh-app__content">{children}</main>
      </div>
      <BottomNav pathname={pathname} />
    </div>
  );
}

/* --------------------------------- sidebar --------------------------------- */

function Sidebar({
  programme,
  pathname,
  isAdmin,
}: {
  programme: string;
  pathname: string;
  isAdmin: boolean;
}) {
  return (
    <aside className="rh-sidebar">
      <div className="rh-cluster" style={{ padding: "8px 10px 14px", gap: 10 }}>
        <BrandMark size={36} />
        <div>
          <div className="rh-display" style={{ fontSize: 14, lineHeight: 1.2 }}>
            Revisions Hub
          </div>
          <div className="rh-t-caption rh-faint" style={{ fontWeight: 600 }}>
            {programmeLabel(programme)} · Learning
          </div>
        </div>
      </div>

      {NAV.map((group) => (
        <nav key={group.label} aria-label={group.label}>
          <div className="rh-sidebar__group-label">{group.label}</div>
          {group.items.map((item) => {
            const active = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className="rh-sidebar__item"
                aria-current={active ? "page" : undefined}
              >
                {item.newton ? <NewtonMark size={18} /> : <Icon name={item.icon} />}
                {item.label}
                {item.newton && (
                  <span className="rh-badge rh-badge--ai" style={{ marginLeft: "auto" }}>
                    AI
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      ))}

      {isAdmin && (
        <nav aria-label="Administration">
          <div className="rh-sidebar__group-label">Admin</div>
          <Link
            href={ADMIN_NAV.href}
            className="rh-sidebar__item"
            aria-current={pathname.startsWith("/admin") ? "page" : undefined}
          >
            <Icon name={ADMIN_NAV.icon} />
            {ADMIN_NAV.label}
          </Link>
        </nav>
      )}

      <SidebarFoot />
    </aside>
  );
}

function SidebarFoot() {
  const { data: me } = useMe();
  const name = me?.user?.fullName ?? me?.user?.email ?? "Guest User";
  const role = me?.user?.authRole ?? me?.user?.role ?? "student";
  const plan = me?.entitlements?.planName ?? "Learner";
  const initials = useMemo(
    () =>
      name
        .split(/\s+/)
        .filter(Boolean)
        .map((p) => p[0])
        .slice(0, 2)
        .join("")
        .toUpperCase(),
    [name],
  );
  return (
    <div className="rh-sidebar__foot rh-cluster" style={{ justifyContent: "space-between" }}>
      <span className="rh-avatar">{initials}</span>
      <div style={{ minWidth: 0 }}>
        <div className="rh-t-body-sm" style={{ fontWeight: 700 }}>
          {name.split(" ")[0]}
        </div>
        <div className="rh-t-caption rh-faint">
          {roleLabel(role)} · {plan}
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------- topbar --------------------------------- */

function TopBar() {
  const { theme, toggle } = useTheme();
  const [paletteOpen, setPaletteOpen] = useState(false);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((v) => !v);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <>
      <header className="rh-topbar">
        <button
          type="button"
          className="rh-topbar__search"
          onClick={() => setPaletteOpen(true)}
          aria-label="Open search palette (Command K)"
          style={{ cursor: "text" }}
        >
          <span className="rh-search" style={{ display: "flex", alignItems: "center", gap: "var(--rh-space-3)", width: "100%" }}>
            <Icon name="search" size={16} className="rh-faint" />
            <span className="rh-t-body-sm rh-faint" style={{ flex: 1, textAlign: "left" }}>
              Search topics, pages…
            </span>
            <span style={{ display: "inline-flex", gap: 4 }}>
              <kbd className="rh-kbd">⌘</kbd>
              <kbd className="rh-kbd">K</kbd>
            </span>
          </span>
        </button>

        <div className="rh-topbar__actions">
          <Link href="/newton" className="rh-btn rh-btn--newton" style={{ textDecoration: "none" }}>
            <NewtonMark size={16} />
            Ask Newton
          </Link>
          <button
            type="button"
            className="rh-theme-toggle"
            onClick={toggle}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} theme`}
          >
            {theme === "dark" ? <Icon name="sun" /> : <Icon name="moon" />}
          </button>
          {DEV_AUTH && <RoleSwitcher />}
          <ProfileLink />
        </div>
      </header>

      {paletteOpen && <CommandPalette onClose={() => setPaletteOpen(false)} />}
    </>
  );
}

function ProfileLink() {
  const { data: me } = useMe();
  const name = me?.user?.fullName ?? "Guest User";
  const initials = useMemo(
    () =>
      name
        .split(/\s+/)
        .filter(Boolean)
        .map((p) => p[0])
        .slice(0, 2)
        .join("")
        .toUpperCase(),
    [name],
  );
  return (
    <Link href="/profile" aria-label={`Profile: ${name}`} style={{ display: "inline-flex" }}>
      <span className="rh-avatar">{initials}</span>
    </Link>
  );
}

/* ------------------------------ role switcher ------------------------------ */

function RoleSwitcher() {
  const { role, setRole } = useDevRole();
  const [open, setOpen] = useState(false);

  return (
    <div style={{ position: "relative" }}>
      <button
        type="button"
        className="rh-btn rh-btn--secondary rh-btn--sm"
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="listbox"
        aria-expanded={open}
        title="Switch dev role (auth preview)"
      >
        <Icon name="users" size={14} />
        {roleLabel(role)}
      </button>
      {open && (
        <>
          <div style={{ position: "fixed", inset: 0, zIndex: 60 }} onClick={() => setOpen(false)} />
          <div
            className="rh-card"
            style={{ position: "absolute", top: "calc(100% + 6px)", right: 0, zIndex: 61, padding: 6, minWidth: 190 }}
          >
            <div
              className="rh-t-caption rh-faint"
              style={{ padding: "6px 10px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em" }}
            >
              Dev role
            </div>
            {ROLES.map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => {
                  setRole(r);
                  setOpen(false);
                }}
                className="rh-sidebar__item"
                style={{
                  width: "100%",
                  border: 0,
                  background: role === r ? "var(--rh-violet-soft)" : "transparent",
                  color: role === r ? "var(--rh-violet-hover)" : undefined,
                }}
              >
                {roleLabel(r)}
                {role === r && <span style={{ marginLeft: "auto", display: "inline-flex" }}><Icon name="check" size={14} /></span>}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

/* ----------------------------- command palette ----------------------------- */

type PaletteItem = {
  group: string;
  label: string;
  href: string;
  icon?: IconName;
};

const STATIC_ITEMS: PaletteItem[] = [
  { group: "Navigate", label: "Dashboard", href: "/dashboard", icon: "grid" },
  { group: "Navigate", label: "My Learning", href: "/courses", icon: "book" },
  { group: "Navigate", label: "Practice", href: "/practice", icon: "target" },
  { group: "Navigate", label: "Results & Analytics", href: "/results", icon: "clipboard" },
  { group: "Navigate", label: "Questionbank", href: "/questionbank", icon: "db" },
  { group: "Navigate", label: "Newton AI", href: "/newton", icon: "zap" },
  { group: "Navigate", label: "Profile", href: "/profile", icon: "settings" },
  { group: "Navigate", label: "Subscription", href: "/subscription", icon: "folder" },
];

function CommandPalette({ onClose }: { onClose: () => void }) {
  const [q, setQ] = useState("");
  const [active, setActive] = useState(0);
  const [topicResults, setTopicResults] = useState<{ id: string; title: string }[]>([]);
  const [searching, setSearching] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  // debounced topic search
  useEffect(() => {
    if (!q.trim() || q.trim().length < 2) {
      setTopicResults([]);
      return;
    }
    let cancelled = false;
    const t = setTimeout(async () => {
      try {
        setSearching(true);
        const res = await api.search(q.trim());
        if (!cancelled) {
          setTopicResults(res.results.slice(0, 5).map((r) => ({ id: r.id, title: r.name })));
        }
      } catch {
        /* ignore search failures */
      } finally {
        if (!cancelled) setSearching(false);
      }
    }, 250);
    return () => {
      cancelled = true;
      clearTimeout(t);
    };
  }, [q]);

  const items = useMemo<PaletteItem[]>(() => {
    const staticMatches = STATIC_ITEMS.filter((i) => i.label.toLowerCase().includes(q.toLowerCase()));
    const topics: PaletteItem[] = topicResults.map((t) => ({
      group: "Topics",
      label: t.title,
      href: `/courses/${t.id}`,
      icon: "book" as const,
    }));
    return [...staticMatches, ...topics];
  }, [q, topicResults]);

  useEffect(() => setActive(0), [q]);

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((a) => Math.min(a + 1, items.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((a) => Math.max(a - 1, 0));
    } else if (e.key === "Enter" && items[active]) {
      window.location.href = items[active].href;
    }
  }

  let lastGroup = "";
  return (
    <div
      className="rh-cmdk-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="rh-cmdk">
        <input
          ref={inputRef}
          className="rh-cmdk__input"
          placeholder="Search topics, pages, actions…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={onKeyDown}
        />
        <div className="rh-cmdk__list" role="listbox">
          {items.length === 0 && (
            <div className="rh-cmdk__item" style={{ opacity: 0.7 }}>
              {searching ? "Searching…" : "No results found"}
            </div>
          )}
          {items.map((item, i) => {
            const showGroup = item.group !== lastGroup;
            lastGroup = item.group;
            return (
              <Fragment key={`${item.group}-${item.label}-${i}`}>
                {showGroup && <div className="rh-cmdk__group">{item.group}</div>}
                <a href={item.href} className={cn("rh-cmdk__item", i === active && "rh-cmdk__item--active")}>
                  {item.icon && <Icon name={item.icon} size={16} />}
                  {item.label}
                </a>
              </Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* -------------------------------- bottom nav ------------------------------- */

function BottomNav({ pathname }: { pathname: string }) {
  return (
    <nav className="rh-bottomnav" aria-label="Mobile navigation">
      {BOTTOM_NAV.map((item) => {
        const active = pathname === item.href || pathname.startsWith(item.href + "/");
        return (
          <Link
            key={item.href}
            href={item.href}
            className="rh-bottomnav__item"
            aria-current={active ? "page" : undefined}
          >
            {item.icon === "zap" ? <NewtonMark size={20} /> : <Icon name={item.icon} size={20} />}
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
