import React from 'react';
import { ShieldCheck, ArrowRight, HeartHandshake, GraduationCap, Activity } from 'lucide-react';

export default function Hero({ onStartAssessment, onExploreHelplines }) {
  return (
    <section className="hero-section">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
          <div className="badge-tag">
            <ShieldCheck size={16} />
            <span>Confidential & Non-Diagnostic Student Self-Check</span>
          </div>

          <div className="badge-tag" style={{ background: 'rgba(76,159,56,0.15)', borderColor: 'rgba(76,159,56,0.4)', color: '#4ade80' }}>
            <Activity size={16} />
            <span>UN SDG 3: Good Health & Well-Being</span>
          </div>

          <div className="badge-tag" style={{ background: 'rgba(99,102,241,0.15)', borderColor: 'rgba(99,102,241,0.4)', color: '#a5b4fc' }}>
            <GraduationCap size={16} />
            {/* <span>K.R. Mangalam University Project</span> */}
          </div>
        </div>

        <h1 className="hero-title">
          From Conversation to Care — Empowering Student Mental Well-Being
        </h1>

        <p className="hero-subtitle">
          Student life involves continuous academic, personal, and social demands. AmiCare provides a safe, anonymous self-assessment tool and immediate connection to verified 24/7 crisis lines and campus counseling resources.
        </p>

        <div className="hero-actions">
          <button className="btn-primary" onClick={onStartAssessment}>
            Start Free Self-Assessment
            <ArrowRight size={18} />
          </button>

          <button className="btn-secondary" onClick={onExploreHelplines}>
            <HeartHandshake size={18} />
            Search Referral Helplines
          </button>
        </div>
      </div>
    </section>
  );
}
