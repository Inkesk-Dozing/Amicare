import React from 'react';
import { AlertTriangle, Heart, ShieldCheck, GraduationCap } from 'lucide-react';

export default function DisclaimerFooter() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="disclaimer-box">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontWeight: 700, marginBottom: '0.4rem', color: '#f59e0b' }}>
            <AlertTriangle size={17} />
            <span>Non-Diagnostic Disclaimer</span>
          </div>
          AmiCare is designed solely as a conversational self-reflection tool and helpline referral directory for students. It does not provide medical diagnoses, psychiatric evaluation, or clinical prescriptions. If you are experiencing a severe mental health crisis or thoughts of self-harm, please call <strong>14416 (Tele-MANAS)</strong> or <strong>1800-599-0019 (KIRAN)</strong> immediately.
        </div>

        {/* Academic & Mentor Credits */}
        <div className="glass-card" style={{ padding: '1.25rem 1.5rem', marginBottom: '2rem', textAlign: 'left', background: 'rgba(15,23,42,0.6)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary-light)', fontWeight: 700, marginBottom: '0.5rem' }}>
            <GraduationCap size={18} />
            <span>K.R. Mangalam University — Community Service SDG Project</span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
            <strong>Faculty Mentor:</strong> Dr. Pinky Kumari
          </p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            <strong>Project Team:</strong> Harsh Dev Jha (2501010168), Ishan Rawat (2501010153), Hrijul Bharadwaj (2501010096), Akshay Kumar (2501010033), Anvesha Saxena (2501010144).
          </p>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <ShieldCheck size={16} color="var(--primary-light)" />
            <span>AmiCare — UN SDG 3: Good Health & Well-Being</span>
          </div>

          <div>
            Built with <Heart size={14} color="#ef4444" style={{ display: 'inline', margin: '0 2px' }} /> for Student Mental Health.
          </div>
        </div>
      </div>
    </footer>
  );
}
