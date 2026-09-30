"use client";

import UnifiedHeader from '@/components/navigation/UnifiedHeader';
import { flaskAPI, Programme, SubjectGroup, Strand, Topic } from '@/lib/flask-api';
import { useEffect, useState } from 'react';

export default function CoursesPage() {
  const [programmes, setProgrammes] = useState<Programme[]>([]);
  const [selectedProgramme, setSelectedProgramme] = useState<string>('pyp');
  const [subjectGroups, setSubjectGroups] = useState<SubjectGroup[]>([]);
  const [selectedSubjectGroup, setSelectedSubjectGroup] = useState<string | null>(null);
  const [strands, setStrands] = useState<Strand[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgrammes();
  }, []);

  useEffect(() => {
    if (selectedProgramme) {
      loadSubjectGroups(selectedProgramme);
    }
  }, [selectedProgramme]);

  useEffect(() => {
    if (selectedSubjectGroup) {
      loadStrands(selectedSubjectGroup);
    }
  }, [selectedSubjectGroup]);

  const loadProgrammes = async () => {
    try {
      const progs = await flaskAPI.getProgrammes();
      setProgrammes(progs);
    } catch (error) {
      console.error('Failed to load programmes:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSubjectGroups = async (programmeId: string) => {
    try {
      const sgs = await flaskAPI.getSubjectGroups(programmeId);
      setSubjectGroups(sgs);
      setSelectedSubjectGroup(null);
      setStrands([]);
      setTopics([]);
    } catch (error) {
      console.error('Failed to load subject groups:', error);
    }
  };

  const loadStrands = async (subjectGroupId: string) => {
    try {
      const s = await flaskAPI.getStrands(subjectGroupId);
      setStrands(s);
      setTopics([]);
    } catch (error) {
      console.error('Failed to load strands:', error);
    }
  };

  const loadTopics = async (strandId: string) => {
    try {
      const t = await flaskAPI.getTopics({ strand_id: strandId });
      setTopics(t);
    } catch (error) {
      console.error('Failed to load topics:', error);
    }
  };

  return (
    <main>
      <UnifiedHeader />
      
      <div className="ss-container ss-section">
        <div className="ss-eyebrow">Revisions Hub</div>
        <h1 className="text-navy">Courses</h1>
        <p className="ss-muted" style={{ marginTop: '8px' }}>
          Explore our comprehensive curriculum across PYP, MYP, and DP programmes.
        </p>

        {loading ? (
          <div className="ss-text-center" style={{ marginTop: '40px' }}>
            <p className="ss-muted">Loading curriculum...</p>
          </div>
        ) : (
          <>
            {/* Programme Selector */}
            <div className="ss-platform-switcher" style={{ marginBottom: '32px', justifyContent: 'flex-start' }}>
              {programmes.map((prog) => (
                <button
                  key={prog.id}
                  className={`ss-platform-btn ${selectedProgramme === prog.id ? 'active' : ''}`}
                  onClick={() => setSelectedProgramme(prog.id)}
                >
                  {prog.name}
                </button>
              ))}
            </div>

            {/* Subject Groups */}
            <div className="ss-grid ss-grid--3" style={{ marginBottom: '32px' }}>
              {subjectGroups.map((sg) => (
                <div
                  key={sg.id}
                  className="ss-card ss-card--hover"
                  style={{ 
                    borderColor: selectedSubjectGroup === sg.id ? 'var(--ss-coral)' : 'var(--ss-border)',
                    background: selectedSubjectGroup === sg.id ? 'var(--ss-coral-soft)' : 'var(--ss-surface)'
                  }}
                  onClick={() => setSelectedSubjectGroup(sg.id)}
                >
                  <div className="ss-eyebrow">{sg.kind}</div>
                  <h3 className="text-navy" style={{ marginTop: '8px' }}>{sg.name}</h3>
                  <p className="ss-muted" style={{ marginTop: '4px', fontSize: '0.9rem' }}>
                    {sg.description}
                  </p>
                  <div className="ss-muted" style={{ marginTop: '12px', fontSize: '0.85rem' }}>
                    {sg.strand_count || 0} strands
                  </div>
                </div>
              ))}
            </div>

            {/* Strands and Topics */}
            {selectedSubjectGroup && (
              <div className="ss-card" style={{ marginTop: '32px' }}>
                <h2 className="text-navy" style={{ marginBottom: '24px' }}>
                  {subjectGroups.find(sg => sg.id === selectedSubjectGroup)?.name}
                </h2>
                
                {strands.length > 0 ? (
                  <div>
                    {strands.map((strand) => (
                      <div key={strand.id} style={{ marginBottom: '32px' }}>
                        <h3 className="text-navy" style={{ marginBottom: '12px', paddingBottom: '12px', borderBottom: '1px solid var(--ss-border)' }}>
                          {strand.name}
                        </h3>
                        
                        {topics.length > 0 && topics[0].strand_id === strand.id ? (
                          <div className="ss-grid ss-grid--2">
                            {topics.filter(t => t.strand_id === strand.id).map((topic) => (
                              <div
                                key={topic.id}
                                className="ss-card ss-card--hover"
                                style={{ padding: '16px' }}
                              >
                                <h4 className="text-navy" style={{ fontSize: '1rem', marginBottom: '8px' }}>
                                  {topic.name}
                                </h4>
                                <p className="ss-muted" style={{ fontSize: '0.9rem', marginBottom: '12px' }}>
                                  {topic.summary}
                                </p>
                                <div className="ss-flex ss-flex-between">
                                  <span className="ss-badge ss-badge--navy">
                                    {topic.depth_tier}
                                  </span>
                                  <button className="ss-btn ss-btn--sm ss-btn--outline">
                                    View Details
                                  </button>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="ss-muted">
                            Click to view topics in {strand.name}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="ss-muted">Select a subject group above to view strands and topics.</p>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}