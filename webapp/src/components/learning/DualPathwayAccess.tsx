"use client";

import { useState, useEffect } from 'react';
import { flaskAPI, LearningProgress, TutorRecommendation } from '@/lib/flask-api';
import TutorRecommendationCard from './TutorRecommendationCard';

export default function DualPathwayAccess() {
  const [learningProgress, setLearningProgress] = useState<LearningProgress | null>(null);
  const [recommendations, setRecommendations] = useState<TutorRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activePathway, setActivePathway] = useState<'intelligent' | 'direct'>('intelligent');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to load learning progress (will fail if not authenticated)
      try {
        const progress = await flaskAPI.getLearningProgress();
        setLearningProgress(progress);
      } catch (progressError) {
        console.log('Learning progress not available (may need authentication)');
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
      }
      
      // Try to load recommendations
      try {
        const recs = await flaskAPI.getTutorRecommendations();
        setRecommendations(recs);
      } catch (recError) {
        console.log('Recommendations not available');
        setRecommendations([]);
      }
    } catch (error) {
      console.error('Failed to load data:', error);
      setError('Failed to load learning data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleContactTutor = async (recId: number) => {
    try {
      await flaskAPI.contactTutorFromRecommendation(recId);
      // Refresh recommendations
      const recs = await flaskAPI.getTutorRecommendations();
      setRecommendations(recs);
    } catch (error) {
      console.error('Failed to contact tutor:', error);
      alert('Failed to contact tutor. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="ss-container ss-section">
        <div className="ss-text-center">
          <p className="ss-muted">Loading your personalized learning experience...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ss-container ss-section">
        <div className="ss-card" style={{ padding: '32px', textAlign: 'center' }}>
          <h3 className="text-navy" style={{ marginBottom: '12px' }}>Unable to Load Data</h3>
          <p className="ss-muted">{error}</p>
          <button 
            className="ss-btn ss-btn--primary" 
            onClick={loadData}
            style={{ marginTop: '16px' }}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="ss-container ss-section">
      {/* Pathway Selector */}
      <div className="ss-platform-switcher" style={{ marginBottom: '32px', justifyContent: 'center' }}>
        <button
          className={`ss-platform-btn ${activePathway === 'intelligent' ? 'active' : ''}`}
          onClick={() => setActivePathway('intelligent')}
        >
          🎯 Intelligent Learning Path
        </button>
        <button
          className={`ss-platform-btn ${activePathway === 'direct' ? 'active' : ''}`}
          onClick={() => setActivePathway('direct')}
        >
          🎓 Direct Marketplace Access
        </button>
      </div>

      {/* Intelligent Learning Pathway */}
      {activePathway === 'intelligent' && (
        <div className="ss-grid ss-grid--2">
          {/* Learning Progress Card */}
          <div className="ss-card">
            <h2 className="text-navy">Your Learning Journey</h2>
            <div className="ss-gap" style={{ marginTop: '20px' }}>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Current Streak</span>
                <span className="text-navy fw-700">{learningProgress?.current_streak || 0} days</span>
              </div>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Questions Attempted</span>
                <span className="text-navy fw-700">{learningProgress?.total_questions_attempted || 0}</span>
              </div>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Overall Accuracy</span>
                <span className="text-navy fw-700">{learningProgress?.overall_accuracy || 0}%</span>
              </div>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">XP Points</span>
                <span className="text-navy fw-700">{learningProgress?.xp_points || 0}</span>
              </div>
            </div>
            
            <div className="ss-gap" style={{ marginTop: '24px' }}>
              <button className="ss-btn ss-btn--primary ss-btn--block">
                Continue Learning
              </button>
              <button className="ss-btn ss-btn--outline ss-btn--block">
                Take Diagnostic
              </button>
            </div>
          </div>

          {/* AI Tutor Recommendations */}
          <div className="ss-card">
            <h2 className="text-navy">Need One-on-One Help?</h2>
            <p className="ss-muted" style={{ marginTop: '8px' }}>
              Based on your learning progress, here are tutors who specialize in your areas of improvement.
            </p>

            {recommendations.length > 0 ? (
              <div className="ss-gap" style={{ marginTop: '20px' }}>
                {recommendations.slice(0, 3).map((rec) => (
                  <TutorRecommendationCard
                    key={rec.recommendation_id}
                    recommendation={rec}
                    onContact={handleContactTutor}
                  />
                ))}
              </div>
            ) : (
              <div className="ss-text-center" style={{ marginTop: '20px' }}>
                <p className="ss-muted">
                  Complete a diagnostic assessment to get personalized tutor recommendations.
                </p>
                <button className="ss-btn ss-btn--primary" style={{ marginTop: '16px' }}>
                  Start Diagnostic
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Direct Marketplace Pathway */}
      {activePathway === 'direct' && (
        <div className="ss-card">
          <div className="ss-flex ss-flex-between">
            <div>
              <h2 className="text-navy">Tutor Marketplace</h2>
              <p className="ss-muted" style={{ marginTop: '8px' }}>
                Browse our complete directory of verified tutors across all subjects.
              </p>
            </div>
            <button className="ss-btn ss-btn--primary">
              Browse All Tutors
            </button>
          </div>

          <div className="ss-grid ss-grid--3" style={{ marginTop: '24px' }}>
            {/* Quick Access Cards */}
            <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
              <div className="ss-eyebrow">Find by Subject</div>
              <h3 className="text-navy" style={{ marginTop: '8px' }}>Mathematics</h3>
              <p className="ss-muted" style={{ marginTop: '4px' }}>150+ verified tutors</p>
            </div>

            <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
              <div className="ss-eyebrow">Find by Subject</div>
              <h3 className="text-navy" style={{ marginTop: '8px' }}>Sciences</h3>
              <p className="ss-muted" style={{ marginTop: '4px' }}>120+ verified tutors</p>
            </div>

            <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
              <div className="ss-eyebrow">Find by Subject</div>
              <h3 className="text-navy" style={{ marginTop: '8px' }}>Languages</h3>
              <p className="ss-muted" style={{ marginTop: '4px' }}>80+ verified tutors</p>
            </div>
          </div>

          <div className="ss-grid ss-grid--2" style={{ marginTop: '24px' }}>
            <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
              <div className="ss-eyebrow">Quick Actions</div>
              <div className="ss-gap" style={{ marginTop: '12px' }}>
                <button className="ss-btn ss-btn--outline ss-btn--block">
                  Post a Tutoring Job
                </button>
                <button className="ss-btn ss-btn--outline ss-btn--block">
                  Become a Tutor
                </button>
              </div>
            </div>

            <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
              <div className="ss-eyebrow">Marketplace Stats</div>
              <div className="ss-gap" style={{ marginTop: '12px' }}>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Active Tutors</span>
                  <span className="text-navy fw-700">500+</span>
                </div>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Completed Lessons</span>
                  <span className="text-navy fw-700">10,000+</span>
                </div>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Average Rating</span>
                  <span className="text-navy fw-700">4.8★</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* CTA for pathway switching */}
      <div className="ss-card" style={{ marginTop: '32px', background: 'linear-gradient(135deg, var(--ss-coral), #ff8a5c)', color: '#fff' }}>
        <div className="ss-flex ss-flex-between">
          <div>
            <h2 style={{ color: '#fff' }}>Both Pathways Available</h2>
            <p style={{ color: 'rgba(255,255,255,0.9)', marginTop: '8px' }}>
              Choose your preferred learning style - let AI guide your journey or explore the marketplace directly.
            </p>
          </div>
          <button className="ss-btn" style={{ background: '#fff', color: 'var(--ss-coral-dark)' }}>
            Get Started
          </button>
        </div>
      </div>
    </div>
  );
}
