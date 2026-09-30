# Revisions Hub — web app

Next.js 16 (App Router, Turbopack) · React 19 · Tailwind 4 · TanStack Query.
Talks to the Fastify backend in `../backend` through a same-origin proxy (`/api/v1/*`).
The visual design comes from the static design system in `../frontend` (tokens in
`src/styles/design-system.css`, screen layouts in `src/styles/screens.css`).

## Getting started

```bash
cp .env.example .env.local
npm ci
npm run dev            # http://localhost:3000  (backend expected on :4310)
```

| Script | What it does |
| --- | --- |
| `npm run dev` | Dev server |
| `npm run typecheck` | `tsc --noEmit` |
| `npm run build` | Production build (standalone output) |
| `npm start` | Run the production build |

## Environment

| Variable | When | Purpose |
| --- | --- | --- |
| `API_URL` | **build time**, required in production | Fastify origin `/api/v1/*` is proxied to. The build fails if it is missing. |
| `NEXT_PUBLIC_SITE_URL` | build time | Canonical URL for metadata, `robots.txt`, `sitemap.xml`. |
| `NEXT_PUBLIC_DEV_AUTH` | build time | `true` enables the mock `x-dev-user` header and role switcher. Always on outside production; leave unset in production. |

## Routes

| Route | Group | Notes |
| --- | --- | --- |
| `/` | marketing | Landing page, live plan pricing |
| `/dashboard` | app | Mastery, streaks, Newton insight, continue-learning |
| `/courses` | app | Programme → subject → strand → topic browser |
| `/practice` | app | Session builder + recent/open sessions |
| `/practice/[id]` | app | Session runner: one question at a time, instant Newton feedback, resume, countdown |
| `/results`, `/results/[id]` | app | Analytics overview; per-session breakdown and diagnostics |
| `/questionbank` | app | Filterable question browser (gated by `questionBankAccess`) |
| `/newton` | app | Tutor chat with conversation history, quota handling |
| `/subscription` | app | Plans, checkout (Paystack / M-Pesa), usage, payment history |
| `/profile` | app | Details, theme, account summary |
| `/admin` | app | Platform health, curriculum stats, user/role management (admins only) |

Route groups: `(marketing)` uses the public shell, `(app)` uses the authenticated `AppShell`
and has its own `error.tsx` / `loading.tsx` so the sidebar survives page errors.

## Code map

```
src/app/            routes, root layout, not-found, error, robots, sitemap
src/components/     app-shell, marketing-shell, providers (query, theme, dev role), brand icons
src/components/ui/  primitives (Button, Card, Badge, Field…), page-head (PageHead, QueryError)
src/lib/api.ts      typed API client + all response types
src/lib/utils.ts    formatting and question-payload helpers (normalizeOptions, stimulusText)
```

## Authentication (important)

The app currently authenticates with the backend's **mock Clerk mode**: the client sends
`x-dev-user: <role>` from `localStorage`. This is disabled in production builds
(`DEV_AUTH` in `src/lib/api.ts`). **Real Clerk sessions must be wired up on both the
frontend and backend before a public launch** — until then a production build has no way
to authenticate against the API.

## Deployment

**Vercel** — set `API_URL` and `NEXT_PUBLIC_SITE_URL` as environment variables and deploy.

**Docker**

```bash
docker build -t revisions-hub-web \
  --build-arg API_URL=https://api.example.com \
  --build-arg NEXT_PUBLIC_SITE_URL=https://app.example.com .
docker run -p 3000:3000 revisions-hub-web
```

Fonts are loaded with `next/font/google`, so the **build** needs outbound internet access
(or switch to `next/font/local` with vendored files).

## Known gaps / next steps

- Real authentication (see above).
- No automated tests yet (unit tests for `lib/utils`, Playwright happy-path for practice → results).
- No Content-Security-Policy header: needs a nonce-based setup for Next's inline scripts and the theme-init script.
- Errors are only `console.error`'d in the error boundaries; wire up an error reporter.
- Question bank is a read-only browser; teacher/admin markscheme view is not built.
- Lesson player and exam-shell screens from `../frontend/screens` are not ported yet.
