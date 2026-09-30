/**
 * Typed API client for the Revisions Hub Fastify backend.
 *
 * The webapp talks to the backend through Next.js rewrites: `/api/v1/*` is
 * proxied to `API_URL` (default http://localhost:4310 in the sandbox,
 * the deployed Fastify host in production — same code path either way).
 *
 * Dev auth: the backend accepts an `x-dev-user: <role>` header in mock
 * Clerk mode. The active role is persisted in localStorage and injected
 * on every request. In production this is replaced by a real Clerk
 * session cookie — the client stays identical.
 */

export type Role = 'student' | 'teacher' | 'school_admin' | 'parent' | 'platform_admin';

export type Programme = 'pyp' | 'myp' | 'dp';

export interface User {
  id: string;
  email: string;
  fullName: string | null;
  firstName: string | null;
  lastName: string | null;
  phone: string | null;
  phoneCountryCode: string | null;
  role: Role;
  avatarUrl: string | null;
  locale: string;
  countryCode: string | null;
  programme: Programme | null;
  levelId: string | null;
  organisationId: string | null;
  isSuperadmin: boolean;
  preferences: Record<string, unknown>;
  lastActiveAt: string | null;
  createdAt: string;
  updatedAt: string;
  authRole?: Role;
}

export interface Entitlements {
  planCode: string;
  planName: string;
  tier: number;
  maxSubjects: number;
  monthlyNewtonQuestions: number | 'unlimited';
  questionBankAccess: boolean;
  mockExams: boolean;
  analytics: boolean;
  cohortAnalytics: boolean;
  parentVisibility: boolean;
  ssoProvisioning: boolean;
  isFree: boolean;
  subscriptionStatus?: string;
  periodEnd?: string;
}

export interface GamificationProfile {
  userId: string;
  xp: number;
  level: number;
  streakCurrent: number;
  streakBest: number;
  badges: unknown;
  lastActivityDate: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface MeResponse {
  user: User;
  entitlements: Entitlements;
  gamification: GamificationProfile | null;
  notifications: {
    id: string; channel: string; template: string;
    subject: string; status: string; createdAt: string;
  }[];
}

export interface DevRolesResponse {
  mockMode: boolean;
  header: string;
  roles: Role[];
  usage: string;
}

/* ---------------------------- curriculum ---------------------------- */

export interface ProgrammeRow {
  id: string; name: string; fullName: string; ages: string | null;
  curriculumModel: string | null; programmeMeta: Record<string, unknown>; createdAt?: string;
}

export interface SubjectGroup {
  id: string; programmeId: string; slug: string; name: string;
  kind: 'subject_group' | 'learning_area';
  description: string | null; depthTier: 'full' | 'lean' | 'scaffold';
  discipline: string | null; accentColor: string | null; sortOrder: number;
}

export interface Strand {
  id: string; programmeId: string; subjectGroupId: string;
  name: string; summary?: string | null; specRef?: string | null;
  topicCount?: number; sortOrder: number;
}

export interface TopicSummary {
  id: string; name: string; summary: string | null;
  strandId: string; subjectGroupId: string; programmeId: string;
  depthTier: 'full' | 'lean' | 'scaffold';
  keyConcepts: string[] | null;
}

export interface LearningObjectives { foundation?: string[] | null; certification?: string[] | null }
export interface InquiryQuestions { factual?: string[] | null; conceptual?: string[] | null; debatable?: string[] | null }
export interface SkillsGraph { skills?: unknown[] | null; concepts?: unknown[] | null; knowledge?: unknown[] | null; assessments?: unknown[] | null }
export interface Misconception { misconception: string; remedy: string }
export interface ProgressionStep { band: string; focus: string; level: string }
export interface PracticeSeed { type: string; prompt: string }

export interface TopicDetail {
  topic: {
    id: string; programmeId: string; subjectGroupId: string; strandId: string;
    name: string; summary: string | null;
    keyConcepts: string[] | null; relatedConcepts: string[] | null;
    globalContextLinks: string[] | null; atlLinks: string[] | null;
    criteriaFocus: string[] | null; concepts: unknown;
    vocabulary: { term: string; definition?: string | null }[] | null;
    learningObjectives: LearningObjectives | null;
    progression: ProgressionStep[] | null; misconceptions: Misconception[] | null;
    skillsGraph: SkillsGraph | null; lessonEngine: Record<string, string> | null;
    practiceSeeds: PracticeSeed[] | null; newtonPrompts: string[] | null;
    inquiryQuestions: InquiryQuestions | null; uoiLinks: unknown;
    depthTier: 'full' | 'lean' | 'scaffold';
    createdAt: string; updatedAt: string;
  };
  strand: { id: string; name: string } | null;
  subjectGroup: { id: string; name: string } | null;
  contentLayers: {
    learn: { lessonEngine: Record<string, string> | null; vocabulary: { term: string; definition?: string | null }[] | null; learningObjectives: LearningObjectives | null };
    practice: { practiceSeeds: PracticeSeed[] | null };
    assess: { skillsGraph: SkillsGraph | null; criteriaFocus: string[] | null; inquiryQuestions: InquiryQuestions | null };
    master: { misconceptions: Misconception[] | null; newtonPrompts: string[] | null; progression: ProgressionStep[] | null };
  };
}

export interface LessonProgress {
  id: string; topicId: string; topicName: string;
  percentComplete: number; completedHooks: number; totalHooks: number;
  lastHookKey: string | null; hooksCompleted: string[] | null;
  completedAt: string | null; updatedAt: string;
}

export interface SearchResults {
  results: { id: string; name: string; summary: string | null; programmeId: string; strandId: string }[];
  query: string;
}

/* ------------------------------ practice ------------------------------ */

export type SessionKind =
  | 'topic_test' | 'unit_test' | 'mock_exam' | 'skills_test' | 'diagnostic_test'
  | 'mastery_test' | 'timed_exam' | 'adaptive_exam' | 'free_practice' | 'prediction_exam';

export type Difficulty = 'guided' | 'basic' | 'intermediate' | 'advanced' | 'challenge' | 'mixed';

export type QuestionType =
  | 'mcq' | 'multiple_response' | 'true_false' | 'matching' | 'fill_in_the_blank'
  | 'short_answer' | 'structured' | 'calculation' | 'data_response' | 'graph_interpretation'
  | 'source_analysis' | 'essay' | 'case_study' | 'experimental_design' | 'coding'
  | 'simulation' | 'oral_response';

export interface PracticeSession {
  id: string; userId: string; kind: SessionKind; title: string;
  programmeId: string | null; subjectGroupId: string | null; strandId: string | null; topicId: string | null;
  status: 'created' | 'in_progress' | 'submitted' | 'graded' | 'expired';
  questionCount: number; difficulty: Difficulty | null; durationMinutes: number | null;
  startedAt: string | null; submittedAt: string | null; gradedAt: string | null;
  scorePct: number | null; accuracy: number | null;
  totalMarks: number | null; earnedMarks: number | null;
  correctCount: number | null; incorrectCount: number | null; partialCount: number | null;
  diagnostics: Record<string, unknown> | null;
  adaptiveState: Record<string, unknown> | null;
  createdAt: string; updatedAt: string;
}

export interface SessionQuestion {
  position: number; id: string; questionId: string;
  type: QuestionType; difficulty: Difficulty | null; marks: number;
  stem: string; stimulus: unknown;
  /** Backend stores `{ key, text }[]`; older payloads used a key→text record. Use `normalizeOptions()`. */
  options: { key: string; text: string }[] | Record<string, string> | null;
  commandTerm: string | null; topicId: string | null;
  correct: boolean | null; earnedMarks: number; answeredAt: string | null;
  answer?: unknown; markscheme?: unknown; explanation?: string | null;
}

export interface QuestionSummary {
  id: string; externalId: string | null; programmeId: string | null;
  topicId: string | null; strandId: string | null; subjectGroupId: string | null;
  type: QuestionType; difficulty: Difficulty; stem: string;
  marks: number; commandTerm: string | null;
  assessmentObjective: string | null; source: string | null;
}

export interface SessionDetail {
  session: PracticeSession;
  questions: SessionQuestion[];
}

export interface AnswerResult {
  position: number; correct: boolean;
  marksAwarded: number; marksTotal: number;
  explanation: string | null;
  misconception: string | null;
  followUpQuestion: string | null;
  nextDifficulty: 'easier' | 'same' | 'harder' | null;
  answer: unknown; markscheme: unknown;
}

export interface MasteryRecordApi {
  id: string; userId: string; skillNodeId: string; status: string;
  attempts: number; correct: number; masteryScore: number;
  lastPracticedAt: string | null; updatedAt: string;
}

/* ------------------------------ newton ------------------------------ */

export interface NewtonReply {
  reply: string;
  diagnosis: Record<string, unknown> | null;
  conversationId: string;
}

export interface NewtonConversation {
  id: string; userId: string; topicId: string | null; subjectGroupId: string | null;
  title: string | null; mode: string; createdAt: string; updatedAt: string;
  messages?: NewtonMessage[];
}

export interface NewtonMessage {
  id?: string; role: 'user' | 'assistant'; content: string;
  diagnosis?: Record<string, unknown> | null;
  createdAt?: string;
}

/* ------------------------------ billing ------------------------------ */

export interface Plan {
  id: string; code: string; name: string; description: string | null;
  tier: number; isDefault: boolean; currency: string;
  priceMonthly: number; priceYearly: number; perSeat: boolean; seatPrice: number;
  maxSubjects: number; maxSubjectsLabel: string | null;
  monthlyNewtonQuestions: number; unlimitedNewton: boolean;
  questionBankAccess: boolean; mockExams: boolean; analytics: boolean;
  cohortAnalytics: boolean; parentVisibility: boolean; ssoProvisioning: boolean;
  features: { highlights: string[] } | null;
  stripePriceIdMonthly: string | null; paystackPlanCode: string | null;
  sortOrder: number; active: boolean;
}

export interface Subscription {
  id: string; userId: string; planId: string; status: string;
  currentPeriodStart: string | null; currentPeriodEnd: string | null;
  cancelAtPeriodEnd: boolean; trialEndsAt: string | null; source: string | null;
  createdAt: string; updatedAt: string;
  plan?: Plan; planName?: string; planCode?: string;
}

export interface CheckoutResponse {
  simulated: boolean; reference: string; amountCents: number; currency: string;
  authorizationUrl: string | null; provider?: string; channel?: string;
}

export interface PaymentRow {
  id: string; userId: string; reference: string | null; provider: string;
  amountCents: number; currency: string; status: string;
  initiatedAt: string; completedAt: string | null; failureReason: string | null;
  meta: Record<string, unknown> | null;
}

/* ------------------------------ analytics ------------------------------ */

export interface AnalyticsOverview {
  sessions: { total: number; graded: number; avgScorePct: number | null; totalMarks: number; earnedMarks: number };
  answers: { total: number; correct: number; incorrect: number; accuracy: number | null };
  mastery: { status: string; count: number }[];
  recentSessions: {
    id: string; kind: SessionKind; title: string;
    scorePct: number | null; status: string; createdAt: string;
  }[];
}

export interface SubjectBreakdown {
  subjectGroupId: string; subject: string; programmeId: string;
  answered: number; correct: number; accuracyPct: number;
}

export interface GamificationMe {
  userId: string; xp: number; level: number;
  streakCurrent: number; streakBest: number;
  badges: unknown; lastActivityDate: string | null;
  createdAt: string; updatedAt: string;
  computedLevel: number; xpForNextLevel: number; xpToNextLevel: number;
}

export interface StreakStatus {
  streakCurrent: number; streakBest: number;
  activeToday: boolean; practicedToday: boolean; practicedYesterday: boolean;
  today: { questionsAnswered: number; correctAnswers: number; xpEarned: number; minutes: number };
}

export interface LeaderboardRow {
  rank: number; userId: string; name: string;
  xp: number; questions: number; minutes: number; daysActive: number;
}

export interface NewtonInsight {
  insight: string;
}

/* ------------------------------ admin ------------------------------ */

export interface AdminOverview {
  counts: { users: number; questions: number; topics: number; skillNodes: number; practiceSessions: number };
  serviceModes: Record<string, string>;
  newton: Record<string, unknown>;
  database: { ok: boolean; latencyMs?: number; error?: string };
}

export interface AdminUser {
  id: string; email: string; fullName: string | null; role: Role;
  programme: Programme | null; levelId: string | null;
  organisationId: string | null; isSuperadmin: boolean;
  lastActiveAt: string | null; createdAt: string;
}

export interface CurriculumStats {
  programmes: number; subjectGroups?: number; topics: number;
  skillNodes: number; unitsOfInquiry?: number; strands?: number;
  [k: string]: unknown;
}

/* ============================== client ============================== */

const ROLE_KEY = 'rh-dev-role';

/**
 * Dev/mock auth (x-dev-user header + role switcher) is on by default outside
 * production, and must be explicitly enabled in production builds with
 * NEXT_PUBLIC_DEV_AUTH=true (e.g. a staging environment backed by a mock-mode API).
 */
export const DEV_AUTH = process.env.NEXT_PUBLIC_DEV_AUTH === 'true' || process.env.NODE_ENV !== 'production';

export function getStoredRole(): Role {
  if (typeof window === 'undefined') return 'student';
  const v = window.localStorage.getItem(ROLE_KEY);
  return v === 'teacher' || v === 'school_admin' || v === 'parent' || v === 'platform_admin' || v === 'student' ? v : 'student';
}

export function setStoredRole(role: Role) {
  if (typeof window !== 'undefined') window.localStorage.setItem(ROLE_KEY, role);
}

export class ApiError extends Error {
  status: number;
  payload: unknown;
  constructor(status: number, message: string, payload?: unknown) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}

type RequestInitWithBody = Omit<RequestInit, "body"> & { body?: unknown; method?: string };

async function request<T>(path: string, init?: RequestInitWithBody): Promise<T> {
  const headers: Record<string, string> = { "content-type": "application/json" };
  if (DEV_AUTH && typeof window !== "undefined") {
    headers["x-dev-user"] = getStoredRole();
  }
  const res = await fetch(`/api/v1${path}`, {
    ...init,
    headers: { ...headers, ...(init?.headers as Record<string, string> | undefined) },
    body: init?.body !== undefined ? JSON.stringify(init.body) : undefined,
    cache: "no-store",
  });
  let payload: unknown = null;
  try { payload = await res.json(); } catch { /* non-JSON */ }
  if (!res.ok) {
    const msg =
      (payload as { error?: { message?: string } | string } | null)?.error &&
      typeof (payload as { error: { message?: string } }).error === 'object'
        ? (payload as { error: { message: string } }).error.message
        : typeof (payload as { error?: string } | null)?.error === 'string'
          ? (payload as { error: string }).error
          : `Request failed (${res.status})`;
    throw new ApiError(res.status, msg, payload);
  }
  return payload as T;
}

export const api = {
  /* health */
  health: () => request<{ ok: boolean; service: string; environment: string }>("/health").catch(() => null),

  /* auth */
  me: () => request<MeResponse>('/auth/me'),
  devRoles: () => request<DevRolesResponse>('/auth/dev-roles'),
  updateMe: (body: Partial<Pick<User, 'fullName' | 'firstName' | 'lastName' | 'programme' | 'levelId' | 'avatarUrl' | 'preferences'>>) =>
    request<{ user: User }>('/auth/me', { method: 'PATCH', body }),

  /* curriculum */
  programmes: () => request<{ programmes: ProgrammeRow[] }>('/curriculum/programmes'),
  programme: (id: string) => request<{ programme: ProgrammeRow }>(`/curriculum/programmes/${id}`),
  levels: (programmeId?: string) =>
    request<{ levels: unknown[] }>(`/curriculum/levels${programmeId ? `?programmeId=${programmeId}` : ''}`),
  subjectGroups: (programmeId?: string) =>
    request<{ subjectGroups: SubjectGroup[] }>(`/curriculum/subject-groups${programmeId ? `?programmeId=${programmeId}` : ''}`),
  strands: (params?: { programmeId?: string; subjectGroupId?: string }) => {
    const qs = new URLSearchParams();
    if (params?.programmeId) qs.set('programmeId', params.programmeId);
    if (params?.subjectGroupId) qs.set('subjectGroupId', params.subjectGroupId);
    const q = qs.toString();
    return request<{ strands: Strand[] }>(`/curriculum/strands${q ? `?${q}` : ''}`);
  },
  topics: (params?: { programmeId?: string; subjectGroupId?: string; strandId?: string; q?: string; depth?: string; limit?: number; offset?: number }) => {
    const qs = new URLSearchParams();
    if (params) {
      for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== '') qs.set(k, String(v));
    }
    const q = qs.toString();
    return request<{ topics: TopicSummary[]; total: number; limit: number; offset: number }>(`/curriculum/topics${q ? `?${q}` : ''}`);
  },
  topic: (id: string) => request<TopicDetail>(`/curriculum/topics/${id}`),
  search: (q: string, programmeId?: string) =>
    request<SearchResults>(`/curriculum/search?q=${encodeURIComponent(q)}${programmeId ? `&programmeId=${programmeId}` : ''}`),
  lessonProgressList: () => request<{ lessons: LessonProgress[] }>('/curriculum/lessons/progress'),
  lessonProgressPost: (topicId: string, hook: string) =>
    request<LessonProgress | Record<string, unknown>>(`/curriculum/topics/${topicId}/lesson/progress`, { method: 'POST', body: { hook } }),

  /* question bank */
  questionTypes: () => request<{ types: string[]; note?: string }>('/questions/types'),
  questions: (params?: {
    programmeId?: string; subjectGroupId?: string; topicId?: string; strandId?: string;
    type?: string; difficulty?: string; source?: string; q?: string; limit?: number; offset?: number;
  }) => {
    const qs = new URLSearchParams();
    if (params) for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== '') qs.set(k, String(v));
    const q = qs.toString();
    return request<{ questions: QuestionSummary[]; total: number; limit: number; offset: number }>(`/questions${q ? `?${q}` : ''}`);
  },
  question: (id: string) => request<{ question: QuestionSummary & Record<string, unknown>; note?: string }>(`/questions/${id}`),

  /* practice */
  createSession: (body: {
    kind: SessionKind; programmeId?: string; subjectGroupId?: string; strandId?: string; topicId?: string;
    questionCount?: number; difficulty?: Difficulty; durationMinutes?: number | null;
  }) => request<PracticeSession>('/practice/sessions', { method: 'POST', body }),
  sessions: (params?: { status?: string; kind?: string }) => {
    const qs = new URLSearchParams();
    if (params?.status) qs.set('status', params.status);
    if (params?.kind) qs.set('kind', params.kind);
    const q = qs.toString();
    return request<{ sessions: PracticeSession[] }>(`/practice/sessions${q ? `?${q}` : ''}`);
  },
  session: (id: string) => request<SessionDetail>(`/practice/sessions/${id}`),
  answer: (id: string, body: { position: number; response: Record<string, unknown>; timeSpentSeconds?: number; flagged?: boolean }) =>
    request<AnswerResult>(`/practice/sessions/${id}/answers`, { method: 'POST', body }),
  submitSession: (id: string) => request<PracticeSession>(`/practice/sessions/${id}/submit`, { method: 'POST' }),
  mastery: (topicId: string) => request<{ mastery: MasteryRecordApi[] }>(`/practice/mastery?topicId=${topicId}`),
  insight: () => request<{ insight: string }>('/practice/insight'),

  /* newton */
  newtonStatus: () => request<Record<string, unknown>>('/newton/status'),
  newtonAsk: (body: { question: string; topicId?: string; conversationId?: string }) =>
    request<NewtonReply>('/newton/ask', { method: 'POST', body }),
  newtonConversations: () => request<{ conversations: NewtonConversation[] }>('/newton/conversations'),
  newtonConversation: (id: string) => request<{ conversation: NewtonConversation; messages: NewtonMessage[] }>(`/newton/conversations/${id}`),
  newtonGenerate: (body: { topicId: string; count?: number; difficulty?: string; types?: string[]; save?: boolean }) =>
    request<{ generated: unknown[]; saved: number; questionIds?: string[] } & Record<string, unknown>>('/newton/generate', { method: 'POST', body }),

  /* billing */
  plans: () => request<{ plans: Plan[] }>('/billing/plans'),
  subscription: () => request<{ subscription: Subscription | null; plan: Plan | null }>('/billing/subscription'),
  checkout: (body: { planCode: string; provider: 'mpesa' | 'paystack'; interval?: 'monthly' | 'yearly'; phone?: string; currency?: string; seats?: number }) =>
    request<CheckoutResponse>('/billing/checkout', { method: 'POST', body }),
  startTrial: (planCode: string) => request<unknown>('/billing/trial', { method: 'POST', body: { planCode } }),
  cancelSubscription: (immediate = false) => request<unknown>('/billing/subscription/cancel', { method: 'POST', body: { immediate } }),
  entitlements: () => request<Entitlements>('/billing/entitlements'),
  usage: (metric = 'newton_questions') => request<{ metric: string; period: string; used: number }>(`/billing/usage?metric=${metric}`),
  payments: () => request<{ payments: PaymentRow[] }>('/billing/payments'),

  /* analytics */
  analyticsOverview: () => request<AnalyticsOverview>('/analytics/me/overview'),
  analyticsSubjects: () => request<{ subjects: SubjectBreakdown[] }>('/analytics/me/subjects'),
  teacherOverview: () => request<{ scope: string; learners: Record<string, unknown>[]; note?: string }>('/analytics/teacher/overview'),

  /* gamification */
  gamificationMe: () => request<GamificationMe>('/gamification/me'),
  streak: () => request<StreakStatus>('/gamification/streak'),
  history: () => request<{ history: Record<string, unknown>[] }>('/gamification/history'),
  leaderboard: (programmeId?: string, scope?: 'day' | 'week' | 'month') => {
    const qs = new URLSearchParams();
    if (programmeId) qs.set('programmeId', programmeId);
    if (scope) qs.set('scope', scope);
    const q = qs.toString();
    return request<{ scope: string; leaderboard: LeaderboardRow[] }>(`/gamification/leaderboard${q ? `?${q}` : ''}`);
  },

  /* admin */
  adminOverview: () => request<AdminOverview>('/admin/overview'),
  adminUsers: (params?: { role?: string; q?: string; limit?: number; offset?: number }) => {
    const qs = new URLSearchParams();
    if (params) for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== '') qs.set(k, String(v));
    const q = qs.toString();
    return request<{ users: AdminUser[]; total: number; limit: number; offset: number }>(`/admin/users${q ? `?${q}` : ''}`);
  },
  adminUpdateUser: (id: string, body: Partial<Pick<AdminUser, 'role' | 'organisationId' | 'isSuperadmin' | 'programme' | 'levelId'>>) =>
    request<{ user: AdminUser }>(`/admin/users/${id}`, { method: 'PATCH', body }),
  adminPayments: () => request<{ payments: PaymentRow[] }>('/admin/payments'),
  adminSubscriptions: () => request<{ subscriptions: Subscription[] }>('/admin/subscriptions'),
  adminCurriculumStats: () => request<CurriculumStats>('/admin/curriculum/stats'),
};
