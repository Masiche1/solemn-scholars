"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { useState } from 'react';

export default function BecomeTutorPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subjects: '',
    level: '',
    experience: '',
    hourly_rate: '',
    bio: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Tutor application:', formData);
    alert('Application submitted successfully! We will review your profile and contact you within 24-48 hours.');
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Tutors Hub</div>
        <h1 className="text-navy">Become a Tutor</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Join our community of verified tutors and help students achieve their learning goals.
        </p>

        <div className="ss-grid ss-grid--2" style={{ marginTop: '32px' }}>
          <div className="ss-card" style={{ padding: '28px' }}>
            <h2 className="text-navy" style={{ marginBottom: '24px' }}>Tutor Application</h2>
            
            <form onSubmit={handleSubmit}>
              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Full Name *</label>
                <input 
                  type="text" 
                  className="ss-input"
                  placeholder="Enter your full name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Email Address *</label>
                <input 
                  type="email" 
                  className="ss-input"
                  placeholder="your.email@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Phone Number *</label>
                <input 
                  type="tel" 
                  className="ss-input"
                  placeholder="+254 7XX XXX XXX"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Subjects You Teach *</label>
                <input 
                  type="text" 
                  className="ss-input"
                  placeholder="e.g., Mathematics, Physics, Chemistry"
                  value={formData.subjects}
                  onChange={(e) => setFormData({...formData, subjects: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Teaching Level *</label>
                <select 
                  className="ss-select"
                  value={formData.level}
                  onChange={(e) => setFormData({...formData, level: e.target.value})}
                  required
                >
                  <option value="">Select teaching level</option>
                  <option value="primary">Primary School</option>
                  <option value="secondary">Secondary School</option>
                  <option value="ib">IB Programme</option>
                  <option value="university">University</option>
                  <option value="adult">Adult Education</option>
                  <option value="multiple">Multiple Levels</option>
                </select>
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Years of Experience *</label>
                <input 
                  type="number" 
                  className="ss-input"
                  placeholder="e.g., 3"
                  value={formData.experience}
                  onChange={(e) => setFormData({...formData, experience: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Hourly Rate (KES) *</label>
                <input 
                  type="number" 
                  className="ss-input"
                  placeholder="e.g., 1000"
                  value={formData.hourly_rate}
                  onChange={(e) => setFormData({...formData, hourly_rate: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '24px' }}>
                <label className="ss-label">Professional Bio *</label>
                <textarea 
                  className="ss-textarea"
                  rows={4}
                  placeholder="Tell us about your teaching experience, qualifications, teaching style, and what makes you a great tutor..."
                  value={formData.bio}
                  onChange={(e) => setFormData({...formData, bio: e.target.value})}
                  required
                />
              </div>

              <div className="ss-gap">
                <button type="submit" className="ss-btn ss-btn--primary ss-btn--block">
                  Submit Application
                </button>
                <button type="button" className="ss-btn ss-btn--outline ss-btn--block">
                  Save for Later
                </button>
              </div>
            </form>
          </div>

          <div>
            <div className="ss-card" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 className="text-navy" style={{ marginBottom: '12px' }}>Why Join Solemn Scholars?</h3>
              <ul style={{ color: 'var(--ss-text)', lineHeight: '1.6' }}>
                <li style={{ marginBottom: '8px' }}>✓ Access to thousands of students across Kenya</li>
                <li style={{ marginBottom: '8px' }}>✓ Flexible scheduling - teach when you want</li>
                <li style={{ marginBottom: '8px' }}>✓ Competitive rates and secure payments</li>
                <li style={{ marginBottom: '8px' }}>✓ Professional verification and profile promotion</li>
                <li>✓ Ongoing support and resources for tutors</li>
              </ul>
            </div>

            <div className="ss-card" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 className="text-navy" style={{ marginBottom: '12px' }}>Requirements</h3>
              <ul style={{ color: 'var(--ss-text)', lineHeight: '1.6' }}>
                <li style={{ marginBottom: '8px' }}>Valid identification (National ID/Passport)</li>
                <li style={{ marginBottom: '8px' }}>Minimum 1 year teaching experience</li>
                <li style={{ marginBottom: '8px' }}>Strong subject knowledge</li>
                <li style={{ marginBottom: '8px' }}>Good communication skills</li>
                <li>Reliable internet connection (for online tutoring)</li>
              </ul>
            </div>

            <div className="ss-card" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 className="text-navy" style={{ marginBottom: '12px' }}>Application Process</h3>
              <ol style={{ color: 'var(--ss-text)', lineHeight: '1.6' }}>
                <li style={{ marginBottom: '8px' }}>Submit your application form</li>
                <li style={{ marginBottom: '8px' }}>Our team reviews your profile</li>
                <li style={{ marginBottom: '8px' }}>Verification interview (video call)</li>
                <li style={{ marginBottom: '8px' }}>Profile setup and training</li>
                <li>Start receiving student inquiries!</li>
              </ol>
            </div>

            <div className="ss-card" style={{ padding: '24px', background: 'linear-gradient(135deg, var(--ss-coral), #ff8a5c)', color: '#fff' }}>
              <h3 style={{ color: '#fff', marginBottom: '12px' }}>Questions?</h3>
              <p style={{ color: 'rgba(255,255,255,0.9)', marginBottom: '16px' }}>
                Our team is here to help you get started on your tutoring journey.
              </p>
              <button className="ss-btn" style={{ background: '#fff', color: 'var(--ss-coral-dark)' }}>
                Contact Support
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}