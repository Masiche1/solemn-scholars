"use client";

import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api, getStoredRole, setStoredRole, type Role } from "@/lib/api";

/* --------------------------------- theme ----------------------------------- */

type Theme = "light" | "dark";
const THEME_KEY = "rh-theme";

type ThemeCtx = { theme: Theme; toggle: () => void; setTheme: (t: Theme) => void };
const ThemeContext = createContext<ThemeCtx | null>(null);

export function useTheme(): ThemeCtx {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within <Providers>");
  return ctx;
}

/* -------------------------------- dev role --------------------------------- */

type DevRoleCtx = { role: Role; setRole: (r: Role) => void };
const DevRoleContext = createContext<DevRoleCtx | null>(null);

export function useDevRole(): DevRoleCtx {
  const ctx = useContext(DevRoleContext);
  if (!ctx) throw new Error("useDevRole must be used within <Providers>");
  return ctx;
}

/* ------------------------------- query client ------------------------------ */

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        refetchOnWindowFocus: false,
        retry: 1,
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined;

function getQueryClient() {
  if (typeof window === "undefined") {
    // Server: fresh client per request (no shared state)
    return makeQueryClient();
  }
  if (!browserQueryClient) {
    browserQueryClient = makeQueryClient();
  }
  return browserQueryClient;
}

/* -------------------------------- providers -------------------------------- */

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(getQueryClient);

  const [theme, setThemeState] = useState<Theme>("light");
  const [role, setRoleState] = useState<Role>("student");
  const [hydrated, setHydrated] = useState(false);

  // hydrate theme + role on mount. The inline init script in <head> has already
  // applied the right data-theme (stored choice, else system preference), so
  // adopt whatever it set instead of overriding it with a default.
  useEffect(() => {
    let stored: string | null = null;
    try { stored = localStorage.getItem(THEME_KEY); } catch { /* storage unavailable */ }
    const applied = document.documentElement.getAttribute("data-theme");
    setThemeState(stored === "dark" || stored === "light" ? stored : applied === "dark" ? "dark" : "light");
    setRoleState(getStoredRole());
    setHydrated(true);
  }, []);

  // reflect theme on <html data-theme> (only after hydration, to avoid a flash)
  useEffect(() => {
    if (hydrated) document.documentElement.setAttribute("data-theme", theme);
  }, [theme, hydrated]);

  const toggle = useCallback(() => {
    setThemeState((t) => {
      const next = t === "dark" ? "light" : "dark";
      try { localStorage.setItem(THEME_KEY, next); } catch { /* ignore */ }
      return next;
    });
  }, []);

  const setTheme = useCallback((t: Theme) => {
    setThemeState(t);
    try { localStorage.setItem(THEME_KEY, t); } catch { /* ignore */ }
  }, []);

  const setRole = useCallback((r: Role) => {
    setStoredRole(r);
    setRoleState(r);
    // refetch everything — the role determines the served user
    queryClient.invalidateQueries();
  }, [queryClient]);

  const themeValue = useMemo(() => ({ theme, toggle, setTheme }), [theme, toggle, setTheme]);
  const roleValue = useMemo(() => ({ role, setRole }), [role, setRole]);

  return (
    <QueryClientProvider client={queryClient}>
      <DevRoleContext.Provider value={roleValue}>
        <ThemeContext.Provider value={themeValue}>{children}</ThemeContext.Provider>
      </DevRoleContext.Provider>
    </QueryClientProvider>
  );
}

/* ------------------------------ session hook ------------------------------- */

/**
 * Convenience hook: the current user's profile + entitlements.
 * Refetches automatically when the dev role changes (queryKey includes role).
 */
export function useMe() {
  const { role } = useDevRole();
  return useQuery({
    queryKey: ["me", role],
    queryFn: () => api.me(),
    // `me` should always be fresh (entitlements/gamification change often)
    staleTime: 10_000,
  });
}
