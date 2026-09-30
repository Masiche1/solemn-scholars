import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import DualPathwayAccess from '@/components/learning/DualPathwayAccess';

export default function HomePage() {
  return (
    <main>
      <UnifiedHeader />
      
      {/* Hero Section */}
      <section className="ss-section ss-section--alt">
        <div className="ss-container">
          <div className="ss-grid ss-grid--2" style={{ alignItems: 'center' }}>
            <div>
              <div className="ss-eyebrow">Solemn Scholars</div>
              <h1 className="text-navy" style={{ fontSize: 'clamp(2.5rem, 5vw, 3.5rem)', marginBottom: '20px' }}>
                Your Complete Learning Journey
              </h1>
              <p className="ss-muted" style={{ fontSize: '1.18rem', marginBottom: '28px', maxWidth: '540px' }}>
                Combine intelligent diagnostics with personalized tutoring. 
                Master your subjects with AI-powered learning, then connect with expert tutors when you need extra help.
              </p>
              <div className="ss-flex ss-gap">
                <button className="ss-btn ss-btn--primary ss-btn--lg">
                  Start Learning Free
                </button>
                <button className="ss-btn ss-btn--secondary ss-btn--lg">
                  Find a Tutor
                </button>
              </div>
            </div>
            
            <div className="ss-card" style={{ padding: '32px', background: 'linear-gradient(135deg, var(--ss-navy), var(--ss-navy-light))', color: '#fff' }}>
              <div className="ss-eyebrow" style={{ color: 'var(--ss-coral)' }}>How It Works</div>
              <div className="ss-gap" style={{ marginTop: '24px' }}>
                <div className="ss-flex ss-gap-sm">
                  <div className="ss-badge ss-badge--coral" style={{ background: 'rgba(255,255,255,0.2)', color: '#fff' }}>1</div>
                  <div>
                    <h3 style={{ color: '#fff', fontSize: '1.1rem' }}>Diagnostic Assessment</h3>
                    <p className="ss-muted" style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.9rem' }}>
                      Take AI-powered diagnostics to identify your strengths and weaknesses
                    </p>
                  </div>
                </div>
                
                <div className="ss-flex ss-gap-sm">
                  <div className="ss-badge ss-badge--coral" style={{ background: 'rgba(255,255,255,0.2)', color: '#fff' }}>2</div>
                  <div>
                    <h3 style={{ color: '#fff', fontSize: '1.1rem' }}>Personalized Learning</h3>
                    <p className="ss-muted" style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.9rem' }}>
                      Get custom study plans and practice sessions tailored to your needs
                    </p>
                  </div>
                </div>
                
                <div className="ss-flex ss-gap-sm">
                  <div className="ss-badge ss-badge--coral" style={{ background: 'rgba(255,255,255,0.2)', color: '#fff' }}>3</div>
                  <div>
                    <h3 style={{ color: '#fff', fontSize: '1.1rem' }}>Smart Tutor Matching</h3>
                    <p className="ss-muted" style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.9rem' }}>
                      Connect with tutors who specialize in your specific areas of improvement
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Dual Pathway Section */}
      <section className="ss-section">
        <div className="ss-container">
          <div className="ss-text-center" style={{ marginBottom: '48px' }}>
            <div className="ss-eyebrow">Choose Your Path</div>
            <h2 className="text-navy">Two Ways to Learn, One Goal</h2>
            <p className="ss-muted" style={{ marginTop: '12px', maxWidth: '600px', margin: '12px auto 0' }}>
              Whether you prefer AI-guided learning or direct tutor access, we have the perfect pathway for your educational journey.
            </p>
          </div>
          
          <DualPathwayAccess />
        </div>
      </section>

      {/* Stats Section */}
      <section className="ss-section ss-section--alt">
        <div className="ss-container">
          <div className="ss-grid ss-grid--4">
            <div className="ss-card ss-card--hover ss-text-center">
              <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>500+</div>
              <div className="ss-muted">Verified Tutors</div>
            </div>
            <div className="ss-card ss-card--hover ss-text-center">
              <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>10,000+</div>
              <div className="ss-muted">Completed Lessons</div>
            </div>
            <div className="ss-card ss-card--hover ss-text-center">
              <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>4.8★</div>
              <div className="ss-muted">Average Rating</div>
            </div>
            <div className="ss-card ss-card--hover ss-text-center">
              <div className="text-navy fw-700" style={{ fontSize: '2.6rem', color: 'var(--ss-coral)' }}>98%</div>
              <div className="ss-muted">Student Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="ss-section">
        <div className="ss-container">
          <div className="ss-card ss-text-center" style={{ 
            padding: '56px', 
            background: 'linear-gradient(135deg, var(--ss-coral), #ff8a5c)', 
            color: '#fff' 
          }}>
            <h2 style={{ color: '#fff', marginBottom: '16px' }}>Ready to Transform Your Learning?</h2>
            <p style={{ color: 'rgba(255,255,255,0.9)', marginBottom: '24px', maxWidth: '600px', margin: '0 auto 24px' }}>
              Join thousands of students who are mastering their subjects with Solemn Scholars' intelligent learning platform.
            </p>
            <div className="ss-flex ss-gap" style={{ justifyContent: 'center' }}>
              <button className="ss-btn" style={{ background: '#fff', color: 'var(--ss-coral-dark)' }}>
                Start Free Trial
              </button>
              <button className="ss-btn" style={{ background: 'rgba(255,255,255,0.2)', color: '#fff', border: '2px solid #fff' }}>
                Browse Tutors
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ background: 'var(--ss-navy)', color: '#c6d0e0', padding: '56px 0 28px', marginTop: '80px' }}>
        <div className="ss-container">
          <div className="ss-grid ss-grid--4">
            <div>
              <div className="ss-logo" style={{ color: '#fff', marginBottom: '16px' }}>
                <div className="ss-logo-mark">SS</div>
                <span>Solemn Scholars</span>
              </div>
              <p style={{ color: '#8c98ad', fontSize: '0.9rem' }}>
                Your complete learning journey with intelligent diagnostics and personalized tutoring.
              </p>
            </div>
            
            <div>
              <h4 style={{ color: '#fff', marginBottom: '16px', fontSize: '1rem' }}>Revisions Hub</h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.9rem' }}>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Dashboard</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Courses</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Practice</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Results</a></li>
              </ul>
            </div>
            
            <div>
              <h4 style={{ color: '#fff', marginBottom: '16px', fontSize: '1rem' }}>Tutors Hub</h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.9rem' }}>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Find Tutors</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Post a Job</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Become a Tutor</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>How It Works</a></li>
              </ul>
            </div>
            
            <div>
              <h4 style={{ color: '#fff', marginBottom: '16px', fontSize: '1rem' }}>Company</h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.9rem' }}>
                <li><a href="#" style={{ color: '#c6d0e0' }}>About Us</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Contact</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Privacy Policy</a></li>
                <li><a href="#" style={{ color: '#c6d0e0' }}>Terms of Service</a></li>
              </ul>
            </div>
          </div>
          
          <div style={{ borderTop: '1px solid rgba(255,255,255,0.12)', marginTop: '40px', paddingTop: '24px', fontSize: '0.85rem', color: '#8c98ad', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
            <div>© 2024 Solemn Scholars. All rights reserved.</div>
            <div>Made with ❤️ for students everywhere</div>
          </div>
        </div>
      </footer>
    </main>
  );
}
