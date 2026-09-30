"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { useState } from 'react';

export default function PostJobPage() {
  const [formData, setFormData] = useState({
    subject: '',
    level: '',
    location: '',
    schedule: '',
    budget: '',
    description: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Job posted:', formData);
    alert('Job posted successfully! Tutors will contact you shortly.');
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Tutors Hub</div>
        <h1 className="text-navy">Post a Tutoring Job</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Tell us what you need and qualified tutors will reach out to you.
        </p>

        <div className="ss-grid ss-grid--2" style={{ marginTop: '32px' }}>
          <div className="ss-card" style={{ padding: '28px' }}>
            <h2 className="text-navy" style={{ marginBottom: '24px' }}>Job Details</h2>
            
            <form onSubmit={handleSubmit}>
              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Subject *</label>
                <select 
                  className="ss-select"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  required
                >
                  <option value="">Select a subject</option>
                  <option value="mathematics">Mathematics</option>
                  <option value="science">Science</option>
                  <option value="language">Language</option>
                  <option value="humanities">Humanities</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Level *</label>
                <select 
                  className="ss-select"
                  value={formData.level}
                  onChange={(e) => setFormData({...formData, level: e.target.value})}
                  required
                >
                  <option value="">Select level</option>
                  <option value="primary">Primary School</option>
                  <option value="secondary">Secondary School</option>
                  <option value="ib">IB Programme</option>
                  <option value="university">University</option>
                  <option value="adult">Adult Education</option>
                </select>
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Location *</label>
                <select 
                  className="ss-select"
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                  required
                >
                  <option value="">Select location</option>
                  <option value="nairobi">Nairobi</option>
                  <option value="mombasa">Mombasa</option>
                  <option value="kisumu">Kisumu</option>
                  <option value="nakuru">Nakuru</option>
                  <option value="online">Online Only</option>
                </select>
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Schedule *</label>
                <select 
                  className="ss-select"
                  value={formData.schedule}
                  onChange={(e) => setFormData({...formData, schedule: e.target.value})}
                  required
                >
                  <option value="">Select schedule</option>
                  <option value="weekdays">Weekdays (Morning)</option>
                  <option value="weekdays-evening">Weekdays (Evening)</option>
                  <option value="weekends">Weekends</option>
                  <option value="flexible">Flexible</option>
                </select>
              </div>

              <div className="ss-form-group" style={{ marginBottom: '20px' }}>
                <label className="ss-label">Budget (KES per hour) *</label>
                <input 
                  type="number" 
                  className="ss-input"
                  placeholder="e.g., 1000"
                  value={formData.budget}
                  onChange={(e) => setFormData({...formData, budget: e.target.value})}
                  required
                />
              </div>

              <div className="ss-form-group" style={{ marginBottom: '24px' }}>
                <label className="ss-label">Description *</label>
                <textarea 
                  className="ss-textarea"
                  rows={4}
                  placeholder="Describe your learning goals, specific topics you need help with, and any other relevant details..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required
                />
              </div>

              <div className="ss-gap">
                <button type="submit" className="ss-btn ss-btn--primary ss-btn--block">
                  Post Job
                </button>
                <button type="button" className="ss-btn ss-btn--outline ss-btn--block">
                  Save as Draft
                </button>
              </div>
            </form>
          </div>

          <div>
            <div className="ss-card" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 className="text-navy" style={{ marginBottom: '12px' }}>Tips for a Great Job Post</h3>
              <ul style={{ color: 'var(--ss-text)', lineHeight: '1.6' }}>
                <li style={{ marginBottom: '8px' }}>Be specific about your learning goals</li>
                <li style={{ marginBottom: '8px' }}>Include your current level and expected outcomes</li>
                <li style={{ marginBottom: '8px' }}>Mention any specific topics or exam preparation needs</li>
                <li style={{ marginBottom: '8px' }}>Set a realistic budget based on market rates</li>
                <li>Be clear about your preferred schedule and location</li>
              </ul>
            </div>

            <div className="ss-card" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 className="text-navy" style={{ marginBottom: '12px' }}>What Happens Next?</h3>
              <ol style={{ color: 'var(--ss-text)', lineHeight: '1.6' }}>
                <li style={{ marginBottom: '8px' }}>Your job is posted to our tutor network</li>
                <li style={{ marginBottom: '8px' }}>Qualified tutors can apply with their profiles</li>
                <li style={{ marginBottom: '8px' }}>You'll receive notifications of new applications</li>
                <li style={{ marginBottom: '8px' }}>Review profiles and contact tutors you like</li>
                <li>Schedule sessions and start learning!</li>
              </ol>
            </div>

            <div className="ss-card" style={{ padding: '24px', background: 'linear-gradient(135deg, var(--ss-coral), #ff8a5c)', color: '#fff' }}>
              <h3 style={{ color: '#fff', marginBottom: '12px' }}>Need Help Finding a Tutor?</h3>
              <p style={{ color: 'rgba(255,255,255,0.9)', marginBottom: '16px' }}>
                Browse our tutor directory directly and contact tutors who match your requirements.
              </p>
              <button className="ss-btn" style={{ background: '#fff', color: 'var(--ss-coral-dark)' }}>
                Browse Tutors
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}