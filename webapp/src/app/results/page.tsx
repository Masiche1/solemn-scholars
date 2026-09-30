import UnifiedHeader from '@/components/navigation/UnifiedHeader';

export default function ResultsPage() {
  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Revisions Hub</div>
        <h1 className="text-navy">Results & Analytics</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Track your progress and analyze your performance across all subjects.
        </p>

        <div className="ss-grid ss-grid--2" style={{ marginTop: '32px' }}>
          <div className="ss-card">
            <h2 className="text-navy" style={{ marginBottom: '16px' }}>Performance Overview</h2>
            <div className="ss-gap" style={{ marginTop: '20px' }}>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Total Sessions:</span>
                <span className="text-navy fw-700">0</span>
              </div>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Average Score:</span>
                <span className="text-navy fw-700">--</span>
              </div>
              <div className="ss-flex ss-flex-between">
                <span className="ss-muted">Time Spent:</span>
                <span className="text-navy fw-700">0 hours</span>
              </div>
            </div>
          </div>

          <div className="ss-card">
            <h2 className="text-navy" style={{ marginBottom: '16px' }}>Subject Breakdown</h2>
            <div className="ss-muted" style={{ marginTop: '20px' }}>
              Complete practice sessions to see your performance by subject.
            </div>
          </div>
        </div>

        <div className="ss-card" style={{ marginTop: '32px' }}>
          <h2 className="text-navy" style={{ marginBottom: '16px' }}>Recent Sessions</h2>
          <div className="ss-muted" style={{ marginTop: '12px' }}>
            No practice sessions completed yet. Start practicing to see your results here.
          </div>
        </div>
      </div>
    </main>
  );
}