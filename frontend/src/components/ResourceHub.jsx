import React, { useState } from 'react';
import { BookOpen, Sparkles, Clock, Eye, Hand, Volume2, Smile, Heart, CheckCircle2, Wind } from 'lucide-react';

export default function ResourceHub({ onLaunchBreathing }) {
  const [activeTab, setActiveTab] = useState('grounding'); // 'grounding', 'articles'
  const [groundingStep, setGroundingStep] = useState(5);
  const [selectedArticle, setSelectedArticle] = useState(null);

  const groundingSteps = [
    { step: 5, icon: <Eye size={28} color="var(--primary-light)" />, title: "Look around you", prompt: "Acknowledge 5 things you can SEE near your desk or room right now." },
    { step: 4, icon: <Hand size={28} color="var(--accent-indigo)" />, title: "Feel your body", prompt: "Acknowledge 4 things you can TOUCH (your chair, phone, feet on the floor)." },
    { step: 3, icon: <Volume2 size={28} color="#f59e0b" />, title: "Listen closely", prompt: "Acknowledge 3 things you can HEAR (fan hum, distant birds, your breath)." },
    { step: 2, icon: <Sparkles size={28} color="#ec4899" />, title: "Notice scents", prompt: "Acknowledge 2 things you can SMELL around you." },
    { step: 1, icon: <Smile size={28} color="#10b981" />, title: "Taste & breathe", prompt: "Acknowledge 1 thing you can TASTE or take 1 deep refreshing breath." }
  ];

  const articles = [
    {
      id: 1,
      title: "Overcoming Academic Burnout & Procrastination",
      category: "Exam Resilience",
      read_time: "4 min guide",
      description: "How to break massive university study loads into 25-minute Pomodoro focus intervals without feeling paralyzed.",
      content: "Academic burnout often stems from trying to tackle a full semester syllabus all at once. Solution: Break tasks into 25-minute micro-focus sessions followed by 5 minutes of physical stretch. Keep your study zone separate from your bed."
    },
    {
      id: 2,
      title: "Optimizing Sleep Hygiene During Exam Peaks",
      category: "Sleep Care",
      read_time: "3 min guide",
      description: "Simple evening habits to stop racing thoughts and achieve restful sleep before important tests.",
      content: "Avoid blue light exposure from smartphones 30 minutes before bed. Write down tomorrow's to-do list on paper before getting into bed to unload brain memory buffers."
    },
    {
      id: 3,
      title: "Handling Imposter Syndrome & Social Comparison",
      category: "Mindset",
      read_time: "5 min guide",
      description: "Recognizing that every student struggles in silence and re-framing your personal progress.",
      content: "Imposter syndrome tricks you into comparing your internal doubts with others' external highlights. Remind yourself that learning is a personal trajectory, and asking for help is a sign of strength."
    }
  ];

  const currentGrounding = groundingSteps.find(g => g.step === groundingStep);

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2.4rem', marginBottom: '0.5rem' }}>Student Self-Care & Resilience Hub</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
          Interactive anxiety reduction exercises and evidence-based mental health guides.
        </p>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginBottom: '2rem' }}>
        <button
          className={`nav-btn ${activeTab === 'grounding' ? 'active' : ''}`}
          onClick={() => setActiveTab('grounding')}
        >
          <Sparkles size={16} /> 5-4-3-2-1 Sensory Grounding Tool
        </button>
        
        <button
          className={`nav-btn ${activeTab === 'articles' ? 'active' : ''}`}
          onClick={() => setActiveTab('articles')}
        >
          <BookOpen size={16} /> Self-Care Guides
        </button>

        <button
          className="nav-btn"
          onClick={onLaunchBreathing}
          style={{ background: 'rgba(20,184,166,0.15)', color: 'var(--primary-light)' }}
        >
          <Wind size={16} /> Guided Box Breathing
        </button>
      </div>

      {activeTab === 'grounding' && (
        <div className="glass-card" style={{ maxWidth: '650px', margin: '0 auto', padding: '3rem 2rem', textAlign: 'center' }}>
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1.25rem' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--glass-border)' }}>
              {currentGrounding.icon}
            </div>
          </div>

          <span className="helpline-category-tag" style={{ background: 'rgba(20,184,166,0.15)', color: 'var(--primary-light)' }}>
            Step {6 - groundingStep} of 5
          </span>

          <h2 style={{ fontSize: '2rem', margin: '0.75rem 0' }}>{currentGrounding.title}</h2>
          <p style={{ color: 'var(--text-primary)', fontSize: '1.15rem', maxWidth: '480px', margin: '0 auto 2rem', lineHeight: '1.6' }}>
            {currentGrounding.prompt}
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            {groundingStep > 1 ? (
              <button
                className="btn-primary"
                onClick={() => setGroundingStep(prev => prev - 1)}
              >
                Next Step ({groundingStep - 1}) →
              </button>
            ) : (
              <button
                className="btn-primary"
                onClick={() => setGroundingStep(5)}
                style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}
              >
                <CheckCircle2 size={18} /> Exercise Completed! Restart
              </button>
            )}
          </div>
        </div>
      )}

      {activeTab === 'articles' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.5rem' }}>
          {articles.map(art => (
            <div key={art.id} className="glass-card" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <span className="helpline-category-tag">{art.category}</span>
                <h3 style={{ fontSize: '1.2rem', marginTop: '0.5rem', marginBottom: '0.75rem' }}>{art.title}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
                  {art.description}
                </p>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '1.5rem' }}>
                  <Clock size={14} color="var(--primary-light)" />
                  <span>{art.read_time}</span>
                </div>
              </div>

              <button className="btn-secondary" style={{ justifyContent: 'center' }} onClick={() => setSelectedArticle(art)}>
                Read Full Guide
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Article Modal */}
      {selectedArticle && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(15,23,42,0.85)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: '1.5rem' }}>
          <div className="glass-card" style={{ maxWidth: '600px', width: '100%', padding: '2.5rem' }}>
            <span className="helpline-category-tag">{selectedArticle.category}</span>
            <h2 style={{ fontSize: '1.8rem', marginTop: '0.5rem', marginBottom: '1rem' }}>{selectedArticle.title}</h2>
            <p style={{ color: 'var(--text-primary)', fontSize: '1rem', lineHeight: '1.7', marginBottom: '2rem' }}>
              {selectedArticle.content}
            </p>
            <div style={{ textAlign: 'right' }}>
              <button className="btn-primary" onClick={() => setSelectedArticle(null)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
