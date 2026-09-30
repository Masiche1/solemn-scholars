"use client";

import { TutorRecommendation } from '@/lib/flask-api';
import { useState } from 'react';

interface TutorRecommendationCardProps {
  recommendation: TutorRecommendation;
  onContact?: (recId: number) => void;
}

export default function TutorRecommendationCard({ recommendation, onContact }: TutorRecommendationCardProps) {
  const [isContacting, setIsContacting] = useState(false);
  const [contacted, setContacted] = useState(recommendation.contacted);

  const handleContact = async () => {
    if (contacted) return;
    
    setIsContacting(true);
    try {
      await onContact?.(recommendation.recommendation_id);
      setContacted(true);
    } catch (error) {
      console.error('Failed to contact tutor:', error);
    } finally {
      setIsContacting(false);
    }
  };

  return (
    <div className="ss-card ss-card--hover">
      <div className="ss-flex ss-flex-between">
        <div>
          <h3 className="text-navy">{recommendation.tutor_name}</h3>
          {recommendation.tutor_headline && (
            <p className="ss-muted text-sm">{recommendation.tutor_headline}</p>
          )}
        </div>
        <div className="ss-badge ss-badge--coral">
          {recommendation.match_score}% Match
        </div>
      </div>

      {recommendation.topic_trigger && (
        <div className="ss-gap-sm" style={{ marginTop: '12px' }}>
          <span className="ss-badge ss-badge--navy">
            {recommendation.topic_trigger}
          </span>
          {recommendation.triggered_by_diagnostic && (
            <span className="ss-badge ss-badge--success">
              AI Recommended
            </span>
          )}
        </div>
      )}

      {recommendation.recommendation_reason && (
        <p className="ss-muted" style={{ marginTop: '12px', fontSize: '0.9rem' }}>
          {recommendation.recommendation_reason}
        </p>
      )}

      <div className="ss-flex ss-flex-between" style={{ marginTop: '16px' }}>
        <div className="ss-flex ss-gap-sm">
          <div className="ss-flex ss-flex-center">
            <span className="ss-amber">★</span>
            <span className="text-navy fw-700">{recommendation.rating}</span>
            <span className="ss-muted">({recommendation.review_count} reviews)</span>
          </div>
          <div className="ss-muted">
            KES {recommendation.hourly_rate}/hour
          </div>
        </div>

        <button
          className={`ss-btn ss-btn--sm ${contacted ? 'ss-btn--secondary' : 'ss-btn--primary'}`}
          onClick={handleContact}
          disabled={isContacting || contacted}
        >
          {isContacting ? 'Contacting...' : contacted ? 'Contacted' : 'Contact Tutor'}
        </button>
      </div>
    </div>
  );
}
