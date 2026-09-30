/**
 * API client for Solemn Scholars Flask backend.
 * 
 * This client connects to the Flask backend at localhost:8000
 * and provides methods for both learning/diagnostic features, tutor marketplace,
 * and curriculum content.
 */

const API_BASE = process.env.API_URL || 'http://localhost:8000';

// Types for Flask backend responses
export interface FlaskUser {
  id: number;
  email: string;
  name: string;
  role: 'student' | 'tutor' | 'admin';
  avatar_url: string | null;
  status: string;
  created_at: string;
}

export interface LearningProgress {
  current_streak: number;
  longest_streak: number;
  total_practice_time_minutes: number;
  total_questions_attempted: number;
  total_correct_answers: number;
  overall_accuracy: number;
  last_practice_date: string | null;
  current_level: string;
  xp_points: number;
  badges_earned: string[];
}

export interface TopicProgress {
  id: number;
  subject_id: number | null;
  topic_name: string;
  topic_code: string | null;
  mastery_level: number;
  questions_attempted: number;
  questions_correct: number;
  accuracy: number;
  last_practiced: string | null;
  recommended_priority: string;
}

export interface PracticeSession {
  session_id: number;
  started_at: string;
  subject_id?: number;
  topic_focus?: string;
  session_type: string;
  total_questions: number;
  completed_questions: number;
  correct_answers: number;
  time_spent_minutes: number;
  status: string;
}

export interface DiagnosticAssessment {
  diagnostic_id: number;
  subject_id?: number;
  assessment_type: string;
  total_questions: number;
  correct_answers: number;
  accuracy_percentage: number;
  topics_mastered: string[];
  topics_struggling: string[];
  started_at: string;
  completed_at: string | null;
}

export interface TutorRecommendation {
  recommendation_id: number;
  tutor_id: number;
  tutor_name: string;
  tutor_headline: string | null;
  hourly_rate: number;
  rating: number;
  review_count: number;
  match_score: number;
  topic_trigger: string | null;
  recommendation_reason: string | null;
  triggered_by_diagnostic: boolean;
  contacted: boolean;
}

export interface StudyPlan {
  id: number;
  plan_name: string | null;
  primary_focus_subject: number | null;
  weekly_goal_hours: number;
  current_week: number;
  total_weeks: number;
  priority_topics: string[];
  generated_from_diagnostic: boolean;
}

export interface DailyTask {
  id: number;
  scheduled_date: string;
  task_type: string;
  subject_id: number | null;
  topic: string | null;
  target_questions: number;
  completed_questions: number;
  duration_minutes: number;
  status: string;
}

// Curriculum types
export interface Programme {
  id: string;
  name: string;
  full_name: string;
  ages: string;
  curriculum_model: string;
  programme_meta: Record<string, unknown>;
}

export interface SubjectGroup {
  id: string;
  programme_id: string;
  slug: string;
  name: string;
  kind: string;
  description: string | null;
  depth_tier: string;
  discipline: string | null;
  accent_color: string | null;
  sort_order: number;
  strand_count?: number;
}

export interface Strand {
  id: string;
  programme_id: string;
  subject_group_id: string;
  name: string;
  summary: string | null;
  spec_ref: string | null;
  topic_count: number;
  sort_order: number;
}

export interface Topic {
  id: string;
  programme_id: string;
  subject_group_id: string;
  strand_id: string;
  name: string;
  summary: string | null;
  depth_tier: string;
  key_concepts: string[];
  vocabulary: { term: string; definition: string }[];
  learning_objectives: Record<string, string[]>;
  progression: { level: string; band: string; focus: string }[];
  misconceptions: { misconception: string; remedy: string }[];
  skills_graph: {
    knowledge: string[];
    skills: string[];
    concepts: string[];
    assessments: string[];
  };
  lesson_engine: Record<string, string>;
  practice_seeds: { type: string; prompt: string }[];
  newton_prompts: string[];
  question_count?: number;
}

export interface QuestionBankItem {
  id: string;
  topic_id: string;
  question_text: string;
  question_type: string;
  difficulty_level: string;
  options: string[];
  correct_answer: string;
  explanation: string | null;
  hints: string[];
  marks: number;
  subject_tag: string | null;
  tags: string[];
}

// API Client Class
class FlaskAPIClient {
  private baseURL: string;
  private authToken: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setAuthToken(token: string) {
    this.authToken = token;
  }

  clearAuthToken() {
    this.authToken = null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.authToken) {
      headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Request failed' }));
      throw new Error(error.message || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Learning Progress Endpoints
  async getLearningProgress(): Promise<LearningProgress> {
    return this.request<LearningProgress>('/api/learning/progress');
  }

  async getTopicProgress(subjectId?: number): Promise<TopicProgress[]> {
    const params = subjectId ? `?subject_id=${subjectId}` : '';
    return this.request<TopicProgress[]>(`/api/learning/progress/topic${params}`);
  }

  // Practice Session Endpoints
  async startPracticeSession(data: {
    subject_id?: number;
    topic_focus?: string;
    session_type?: string;
    total_questions?: number;
  }): Promise<{ session_id: number; started_at: string }> {
    return this.request('/api/learning/practice/start', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async submitQuestionAttempt(
    sessionId: number,
    data: {
      question_id: string;
      subject_id?: number;
      topic?: string;
      question_text?: string;
      user_answer: string;
      correct_answer?: string;
      is_correct: boolean;
      time_spent_seconds?: number;
      hints_used?: number;
      difficulty_level?: string;
      topic_code?: string;
    }
  ): Promise<{
    attempt_id: number;
    is_correct: boolean;
    session_progress: {
      completed: number;
      total: number;
      accuracy: number;
    };
  }> {
    return this.request(`/api/learning/practice/${sessionId}/submit`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async completePracticeSession(
    sessionId: number,
    data: { time_spent_minutes: number }
  ): Promise<{
    session_id: number;
    completed_at: string;
    total_correct: number;
    total_questions: number;
    accuracy: number;
    time_spent_minutes: number;
  }> {
    return this.request(`/api/learning/practice/${sessionId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Diagnostic Assessment Endpoints
  async startDiagnostic(data: {
    subject_id?: number;
    assessment_type?: string;
    total_questions?: number;
  }): Promise<{ diagnostic_id: number; started_at: string }> {
    return this.request('/api/learning/diagnostic/start', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async completeDiagnostic(
    diagnosticId: number,
    data: {
      correct_answers: number;
      topics_mastered: string[];
      topics_struggling: string[];
    }
  ): Promise<{
    diagnostic_id: number;
    accuracy: number;
    topics_struggling: string[];
    recommendations_generated: boolean;
  }> {
    return this.request(`/api/learning/diagnostic/${diagnosticId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Tutor Recommendations Endpoints
  async getTutorRecommendations(): Promise<TutorRecommendation[]> {
    return this.request<TutorRecommendation[]>('/api/learning/recommendations');
  }

  async contactTutorFromRecommendation(
    recId: number
  ): Promise<{ success: boolean; contacted_at: string }> {
    return this.request(`/api/learning/recommendations/${recId}/contact`, {
      method: 'POST',
    });
  }

  // Study Plan Endpoints
  async getStudyPlan(): Promise<{
    plan: StudyPlan | null;
    upcoming_tasks: DailyTask[];
  }> {
    return this.request('/api/learning/study-plan');
  }

  async createStudyPlan(data: {
    plan_name?: string;
    primary_focus_subject?: number;
    weekly_goal_hours?: number;
    priority_topics?: string[];
    generated_from_diagnostic?: boolean;
  }): Promise<{ success: boolean; plan_id: number }> {
    return this.request('/api/learning/study-plan', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Newton AI Tutor Endpoints
  async startNewtonConversation(data: {
    session_id?: number;
    conversation_type?: string;
    topic_context?: string;
  }): Promise<{ conversation_id: number; started_at: string }> {
    return this.request('/api/learning/newton/conversation', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async sendNewtonMessage(
    conversationId: number,
    data: {
      message: string;
      question_context?: string;
      message_type?: string;
    }
  ): Promise<{
    user_message_id: number;
    ai_message_id: number;
    ai_response: string;
  }> {
    return this.request(`/api/learning/newton/${conversationId}/message`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Health Check
  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.request('/api/learning/health');
  }

  // Curriculum API Endpoints
  async getProgrammes(): Promise<Programme[]> {
    return this.request<Programme[]>('/api/curriculum/programmes');
  }

  async getProgramme(programmeId: string): Promise<Programme & { subject_groups: SubjectGroup[] }> {
    return this.request(`/api/curriculum/programmes/${programmeId}`);
  }

  async getSubjectGroups(programmeId?: string): Promise<SubjectGroup[]> {
    const params = programmeId ? `?programme_id=${programmeId}` : '';
    return this.request<SubjectGroup[]>(`/api/curriculum/subject-groups${params}`);
  }

  async getSubjectGroup(sgId: string): Promise<SubjectGroup & { strands: Strand[] }> {
    return this.request(`/api/curriculum/subject-groups/${sgId}`);
  }

  async getStrands(subjectGroupId?: string): Promise<Strand[]> {
    const params = subjectGroupId ? `?subject_group_id=${subjectGroupId}` : '';
    return this.request<Strand[]>(`/api/curriculum/strands${params}`);
  }

  async getStrand(strandId: string): Promise<Strand & { topics: Topic[] }> {
    return this.request(`/api/curriculum/strands/${strandId}`);
  }

  async getTopics(filters?: {
    programme_id?: string;
    subject_group_id?: string;
    strand_id?: string;
    search?: string;
  }): Promise<Topic[]> {
    const params = new URLSearchParams();
    if (filters?.programme_id) params.append('programme_id', filters.programme_id);
    if (filters?.subject_group_id) params.append('subject_group_id', filters.subject_group_id);
    if (filters?.strand_id) params.append('strand_id', filters.strand_id);
    if (filters?.search) params.append('search', filters.search);
    
    const queryString = params.toString();
    return this.request<Topic[]>(`/api/curriculum/topics${queryString ? `?${queryString}` : ''}`);
  }

  async getTopic(topicId: string): Promise<Topic> {
    return this.request(`/api/curriculum/topics/${topicId}`);
  }

  async getQuestions(filters?: {
    topic_id?: string;
    subject_tag?: string;
    difficulty?: string;
    question_type?: string;
  }): Promise<QuestionBankItem[]> {
    const params = new URLSearchParams();
    if (filters?.topic_id) params.append('topic_id', filters.topic_id);
    if (filters?.subject_tag) params.append('subject_tag', filters.subject_tag);
    if (filters?.difficulty) params.append('difficulty', filters.difficulty);
    if (filters?.question_type) params.append('question_type', filters.question_type);
    
    const queryString = params.toString();
    return this.request<QuestionBankItem[]>(`/api/curriculum/questions${queryString ? `?${queryString}` : ''}`);
  }

  async getQuestion(questionId: string): Promise<QuestionBankItem> {
    return this.request(`/api/curriculum/questions/${questionId}`);
  }

  async getRandomQuestions(filters?: {
    topic_id?: string;
    count?: number;
    difficulty?: string;
  }): Promise<QuestionBankItem[]> {
    const params = new URLSearchParams();
    if (filters?.topic_id) params.append('topic_id', filters.topic_id);
    if (filters?.count) params.append('count', filters.count.toString());
    if (filters?.difficulty) params.append('difficulty', filters.difficulty);
    
    const queryString = params.toString();
    return this.request<QuestionBankItem[]>(`/api/curriculum/questions/random${queryString ? `?${queryString}` : ''}`);
  }

  async curriculumHealthCheck(): Promise<{ status: string; service: string }> {
    return this.request('/api/curriculum/health');
  }
}

// Export singleton instance
export const flaskAPI = new FlaskAPIClient(API_BASE);

// Export types for use in components
export type {
  FlaskUser,
  LearningProgress,
  TopicProgress,
  PracticeSession,
  DiagnosticAssessment,
  TutorRecommendation,
  StudyPlan,
  DailyTask,
  Programme,
  SubjectGroup,
  Strand,
  Topic,
  QuestionBankItem,
};
