"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';

export default function TutorsIndexPage() {
  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Tutors Hub</div>
        <h1 className="text-navy">Find Tutors</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Browse our verified tutors and find the perfect match for your learning needs.
        </p>

        {/* Search Section */}
        <div className="ss-card" style={{ marginTop: '32px', padding: '28px' }}>
          <h2 className="text-navy" style={{ marginBottom: '16px' }}>Search Tutors</h2>
          <div className="ss-grid ss-grid--3" style={{ marginTop: '16px' }}>
            <div className="ss-form-group">
              <label className="ss-label">Subject</label>
              <select className="ss-select">
                <option value="">All Subjects</option>
                <option value="mathematics">Mathematics</option>
                <option value="science">Science</option>
                <option value="language">Language</option>
                <option value="humanities">Humanities</option>
              </select>
            </div>
            <div className="ss-form-group">
              <label className="ss-label">Level</label>
              <select className="ss-select">
                <option value="">All Levels</option>
                <option value="primary">Primary</option>
                <option value="secondary">Secondary</option>
                <option value="ib">IB</option>
                <option value="university">University</option>
              </select>
            </div>
            <div className="ss-form-group">
              <label className="ss-label">Location</label>
              <select className="ss-select">
                <option value="">All Locations</option>
                <option value="nairobi">Nairobi</option>
                <option value="mombasa">Mombasa</option>
                <option value="kisumu">Kisumu</option>
                <option value="online">Online Only</option>
              </select>
            </div>
          </div>
          <div className="ss-flex ss-gap" style={{ marginTop: '16px' }}>
            <input 
              type="text" 
              className="ss-input" 
              placeholder="Search by name or keyword..." 
              style={{ flex: 1 }}
            />
            <button className="ss-btn ss-btn--primary">Search</button>
          </div>
        </div>

        {/* Featured Tutors */}
        <div style={{ marginTop: '32px' }}>
          <h2 className="text-navy" style={{ marginBottom: '16px' }}>Featured Tutors</h2>
          <div className="ss-grid ss-grid--3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="ss-card ss-card--hover">
                <div className="ss-flex ss-gap-sm" style={{ marginBottom: '12px' }}>
                  <div 
                    style={{ 
                      width: '60px', 
                      height: '60px', 
                      borderRadius: '50%', 
                      background: 'var(--ss-bg-alt)',
                      display: 'grid',
                      placeItems: 'center',
                      fontSize: '1.5rem'
                    }}
                  >
                    👤
                  </div>
                  <div>
                    <h3 className="text-navy" style={{ fontSize: '1rem', marginBottom: '2px' }}>
                      Sarah Mitchell
                    </h3>
                    <p className="ss-muted" style={{ fontSize: '0.85rem' }}>
                      Mathematics Expert
                    </p>
                  </div>
                </div>
                
                <div className="ss-flex ss-flex-between" style={{ marginBottom: '12px' }}>
                  <div className="ss-flex ss-gap-sm">
                    <span className="ss-amber">★</span>
                    <span className="text-navy fw-700">4.9</span>
                    <span className="ss-muted">(87 lessons)</span>
                  </div>
                  <span className="text-navy fw-700">KES 1,500/hr</span>
                </div>

                <p className="ss-muted" style={{ fontSize: '0.9rem', marginBottom: '16px' }}>
                  IB Mathematics specialist with 5+ years experience helping students achieve their goals.
                </p>

                <div className="ss-gap-sm" style={{ marginBottom: '12px' }}>
                  <span className="ss-badge ss-badge--verified">Verified</span>
                  <span className="ss-badge ss-badge--online">Online</span>
                </div>

                <button className="ss-btn ss-btn--primary ss-btn--block">
                  View Profile
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Subject Categories */}
        <div style={{ marginTop: '32px' }}>
          <h2 className="text-navy" style={{ marginBottom: '16px' }}>Browse by Subject</h2>
          <div className="ss-grid ss-grid--4">
            {['Mathematics', 'Sciences', 'Languages', 'Humanities', 'Arts', 'Business', 'Computer Science', 'Physical Education'].map((subject) => (
              <div key={subject} className="ss-card ss-card--hover" style={{ padding: '16px', textAlign: 'center' }}>
                <div style={{ fontSize: '2rem', marginBottom: '8px' }}>📚</div>
                <h3 className="text-navy" style={{ fontSize: '1rem' }}>{subject}</h3>
                <p className="ss-muted" style={{ fontSize: '0.85rem', marginTop: '4px' }}>
                  50+ tutors
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}