"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { flaskAPI, LearningProgress } from '@/lib/flask-api';
import { useEffect, useState } from 'react';

export default function DashboardPage() {
  const [learningProgress, setLearningProgress] = useState<LearningProgress | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const progress = await flaskAPI.getLearningProgress();
      setLearningProgress(progress);
    } catch (error) {
      console.error('Failed to load progress:', error);
      // Set default values for demo
      setLearningProgress({
        current_streak: 0,
        longest_streak: 0,
        total_practice_time_minutes: 0,
        total_questions_attempted: 0,
        total_correct_answers: 0,
        overall_accuracy: 0,
        last_practice_date: null,
        current_level: 'beginner',
        xp_points: 0,
        badges_earned: []
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Revisions Hub</div>
        <h1 className="text-navy">Dashboard</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Your personalized learning journey at a glance.
        </p>

        {loading ? (
          <div className="ss-text-center" style={{ marginTop: '40px' }}>
            <p className="ss-muted">Loading your dashboard...</p>
          </div>
        ) : (
          <>
            <div className="ss-grid ss-grid--3" style={{ marginTop: '32px' }}>
              {/* Streak Card */}
              <div className="ss-card">
                <div className="ss-eyebrow">Your Streak</div>
                <div style={{ marginTop: '16px' }}>
                  <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>
                    {learningProgress?.current_streak || 0}
                  </div>
                  <div className="ss-muted">days in a row</div>
                </div>
                <div className="ss-muted" style={{ marginTop: '12px', fontSize: '0.9rem' }}>
                  Best: {learningProgress?.longest_streak || 0} days
                </div>
              </div>

              {/* Questions Card */}
              <div className="ss-card">
                <div className="ss-eyebrow">Questions Attempted</div>
                <div style={{ marginTop: '16px' }}>
                  <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>
                    {learningProgress?.total_questions_attempted || 0}
                  </div>
                  <div className="ss-muted">total questions</div>
                </div>
                <div className="ss-flex ss-flex-between" style={{ marginTop: '12px' }}>
                  <span className="ss-muted">Correct: {learningProgress?.total_correct_answers || 0}</span>
                  <span className="ss-muted">Accuracy: {learningProgress?.overall_accuracy || 0}%</span>
                </div>
              </div>

              {/* XP Card */}
              <div className="ss-card">
                <div className="ss-eyebrow">XP Points</div>
                <div style={{ marginTop: '16px' }}>
                  <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>
                    {learningProgress?.xp_points || 0}
                  </div>
                  <div className="ss-muted">experience points</div>
                </div>
                <div className="ss-muted" style={{ marginTop: '12px', fontSize: '0.9rem' }}>
                  Level: {learningProgress?.current_level || 'beginner'}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="ss-grid ss-grid--2" style={{ marginTop: '32px' }}>
              <div className="ss-card">
                <h3 className="text-navy" style={{ marginBottom: '16px' }}>Continue Learning</h3>
                <p className="ss-muted" style={{ marginBottom: '20px' }}>
                  Pick up where you left off with your current study plan.
                </p>
                <button className="ss-btn ss-btn--primary">
                  Resume Practice
                </button>
              </div>

              <div className="ss-card">
                <h3 className="text-navy" style={{ marginBottom: '16px' }}>Take Diagnostic</h3>
                <p className="ss-muted" style={{ marginBottom: '20px' }}>
                  Assess your knowledge and get personalized recommendations.
                </p>
                <button className="ss-btn ss-btn--secondary">
                  Start Assessment
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="ss-card" style={{ marginTop: '32px' }}>
              <h3 className="text-navy" style={{ marginBottom: '16px' }}>Recent Activity</h3>
              <div className="ss-muted" style={{ marginTop: '12px' }}>
                No recent activity to display. Start practicing to see your progress here!
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  );
}