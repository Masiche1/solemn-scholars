"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { flaskAPI } from '@/lib/flask-api';
import { useState } from 'react';

export default function NewtonPage() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessage('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      setLoading(true);
      // Start a conversation if needed
      const conversation = await flaskAPI.startNewtonConversation({
        conversation_type: 'general',
        topic_context: 'general learning'
      });

      // Send message to Newton
      const response = await flaskAPI.sendNewtonMessage(conversation.conversation_id, {
        message: userMessage,
        message_type: 'explanation'
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response.ai_response }]);
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Revisions Hub</div>
        <h1 className="text-navy">Newton AI Tutor</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Your AI-powered learning companion for personalized tutoring and concept explanations.
        </p>

        <div className="ss-card" style={{ marginTop: '32px', height: '600px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ 
            flex: 1, 
            overflowY: 'auto', 
            padding: '20px', 
            background: 'var(--ss-bg-alt)', 
            borderRadius: 'var(--ss-radius-md)',
            marginBottom: '16px'
          }}>
            {messages.length === 0 ? (
              <div className="ss-text-center" style={{ marginTop: '60px' }}>
                <p className="ss-muted">
                  👋 Hello! I'm Newton, your AI tutor. Ask me anything about your studies!
                </p>
                <p className="ss-muted" style={{ marginTop: '8px' }}>
                  I can help with explanations, practice questions, study tips, and more.
                </p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  style={{
                    marginBottom: '16px',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    maxWidth: '80%',
                    marginLeft: msg.role === 'user' ? 'auto' : '0',
                    background: msg.role === 'user' ? 'var(--ss-coral)' : 'var(--ss-surface)',
                    color: msg.role === 'user' ? '#fff' : 'var(--ss-text)'
                  }}
                >
                  <div style={{ fontSize: '0.85rem', marginBottom: '4px', opacity: 0.7 }}>
                    {msg.role === 'user' ? 'You' : 'Newton'}
                  </div>
                  <div>{msg.content}</div>
                </div>
              ))
            )}
          </div>

          <div className="ss-flex ss-gap">
            <input
              type="text"
              className="ss-input"
              placeholder="Ask Newton a question..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={loading}
            />
            <button
              className="ss-btn ss-btn--primary"
              onClick={handleSendMessage}
              disabled={loading || !message.trim()}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>

        <div className="ss-grid ss-grid--3" style={{ marginTop: '32px' }}>
          <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
            <div className="ss-eyebrow">Quick Help</div>
            <h3 className="text-navy" style={{ marginTop: '8px', fontSize: '1.1rem' }}>
              Explain a concept
            </h3>
            <p className="ss-muted" style={{ fontSize: '0.85rem', marginTop: '4px' }}>
              Get detailed explanations of difficult topics
            </p>
          </div>

          <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
            <div className="ss-eyebrow">Quick Help</div>
            <h3 className="text-navy" style={{ marginTop: '8px', fontSize: '1.1rem' }}>
              Practice questions
            </h3>
            <p className="ss-muted" style={{ fontSize: '0.85rem', marginTop: '4px' }}>
              Get help with specific practice problems
            </p>
          </div>

          <div className="ss-card ss-card--hover" style={{ padding: '16px' }}>
            <div className="ss-eyebrow">Quick Help</div>
            <h3 className="text-navy" style={{ marginTop: '8px', fontSize: '1.1rem' }}>
              Study tips
            </h3>
            <p className="ss-muted" style={{ fontSize: '0.85rem', marginTop: '4px' }}>
              Personalized learning strategies
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}