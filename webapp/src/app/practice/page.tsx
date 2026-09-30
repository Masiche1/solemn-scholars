"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { flaskAPI, PracticeSession } from '@/lib/flask-api';
import { useState } from 'react';

export default function PracticePage() {
  const [activeSession, setActiveSession] = useState<PracticeSession | null>(null);
  const [startingSession, setStartingSession] = useState(false);

  const startNewSession = async () => {
    try {
      setStartingSession(true);
      const session = await flaskAPI.startPracticeSession({
        subject_id: 1, // Mathematics
        topic_focus: 'addition',
        session_type: 'practice',
        total_questions: 10
      });
      setActiveSession(session);
    } catch (error) {
      console.error('Failed to start session:', error);
      alert('Failed to start practice session. Please try again.');
    } finally {
      setStartingSession(false);
    }
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Revisions Hub</div>
        <h1 className="text-navy">Practice</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Practice with questions from our comprehensive curriculum to master your subjects.
        </p>

        {!activeSession ? (
          <div className="ss-card" style={{ marginTop: '32px', textAlign: 'center', padding: '48px' }}>
            <h2 className="text-navy" style={{ marginBottom: '16px' }}>Start a Practice Session</h2>
            <p className="ss-muted" style={{ marginBottom: '24px', maxWidth: '500px', margin: '0 auto 24px' }}>
              Choose your subject and topic, then practice with questions tailored to your level.
            </p>
            <button 
              className="ss-btn ss-btn--primary ss-btn--lg"
              onClick={startNewSession}
              disabled={startingSession}
            >
              {startingSession ? 'Starting...' : 'Start Practice Session'}
            </button>
          </div>
        ) : (
          <div className="ss-grid ss-grid--2" style={{ marginTop: '32px' }}>
            <div className="ss-card">
              <h2 className="text-navy" style={{ marginBottom: '16px' }}>Current Session</h2>
              <div className="ss-gap" style={{ marginTop: '20px' }}>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Session ID:</span>
                  <span className="text-navy">#{activeSession.session_id}</span>
                </div>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Type:</span>
                  <span className="text-navy">{activeSession.session_type}</span>
                </div>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Progress:</span>
                  <span className="text-navy">
                    {activeSession.completed_questions} / {activeSession.total_questions}
                  </span>
                </div>
                <div className="ss-flex ss-flex-between">
                  <span className="ss-muted">Accuracy:</span>
                  <span className="text-navy">
                    {activeSession.correct_answers} / {activeSession.completed_questions}
                  </span>
                </div>
              </div>
              
              <div className="ss-gap" style={{ marginTop: '24px' }}>
                <button className="ss-btn ss-btn--primary ss-btn--block">
                  Continue Practice
                </button>
                <button className="ss-btn ss-btn--outline ss-btn--block">
                  End Session
                </button>
              </div>
            </div>

            <div className="ss-card">
              <h2 className="text-navy" style={{ marginBottom: '16px' }}>Question</h2>
              <div style={{ marginTop: '20px', padding: '24px', background: 'var(--ss-bg-alt)', borderRadius: 'var(--ss-radius-md)' }}>
                <p className="text-navy fw-700" style={{ marginBottom: '12px' }}>
                  What is 15 + 27?
                </p>
                <div className="ss-grid ss-grid--2" style={{ marginTop: '16px' }}>
                  <button className="ss-btn ss-btn--outline">38</button>
                  <button className="ss-btn ss-btn--outline">42</button>
                  <button className="ss-btn ss-btn--outline">45</button>
                  <button className="ss-btn ss-btn--outline">52</button>
                </div>
              </div>
              
              <div className="ss-gap" style={{ marginTop: '24px' }}>
                <button className="ss-btn ss-btn--primary ss-btn--block">
                  Submit Answer
                </button>
                <button className="ss-btn ss-btn--ghost ss-btn--block">
                  Get Hint
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}