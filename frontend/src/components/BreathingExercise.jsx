import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Wind, HeartPulse } from 'lucide-react';

export default function BreathingExercise() {
  const [isActive, setIsActive] = useState(false);
  const [phase, setPhase] = useState('Inhale'); // Inhale, Hold, Exhale, Pause
  const [countdown, setCountdown] = useState(4);
  const [technique, setTechnique] = useState('box'); // box (4-4-4-4) or 478 (4-7-8)

  useEffect(() => {
    let timer = null;
    if (isActive) {
      timer = setInterval(() => {
        setCountdown(prev => {
          if (prev > 1) return prev - 1;

          // Cycle phases based on chosen technique
          if (technique === 'box') {
            if (phase === 'Inhale') { setPhase('Hold'); return 4; }
            if (phase === 'Hold') { setPhase('Exhale'); return 4; }
            if (phase === 'Exhale') { setPhase('Rest'); return 4; }
            if (phase === 'Rest') { setPhase('Inhale'); return 4; }
          } else {
            // 4-7-8 method
            if (phase === 'Inhale') { setPhase('Hold'); return 7; }
            if (phase === 'Hold') { setPhase('Exhale'); return 8; }
            if (phase === 'Exhale') { setPhase('Inhale'); return 4; }
          }
          return 4;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isActive, phase, countdown, technique]);

  const toggleStart = () => {
    setIsActive(!isActive);
  };

  const handleReset = () => {
    setIsActive(false);
    setPhase('Inhale');
    setCountdown(4);
  };

  const handleSwitchTechnique = (tech) => {
    setTechnique(tech);
    setIsActive(false);
    setPhase('Inhale');
    setCountdown(4);
  };

  const getPhaseClass = () => {
    if (phase === 'Inhale') return 'expand';
    if (phase === 'Exhale') return 'shrink';
    return '';
  };

  return (
    <div className="container" style={{ maxWidth: '700px', paddingBottom: '4rem' }}>
      <div className="glass-card" style={{ padding: '3rem 2rem', textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary-light)', marginBottom: '0.5rem', fontWeight: 600 }}>
          <Wind size={20} />
          <span>Acute Stress Relief Tool</span>
        </div>

        <h2 style={{ fontSize: '2.2rem', marginBottom: '1rem' }}>Guided Rhythmic Breathing</h2>

        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
          Follow the expanding circle to slow down your heart rate and ease nervous tension during study stress or exams.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginBottom: '2rem' }}>
          <button
            className={`nav-btn ${technique === 'box' ? 'active' : ''}`}
            onClick={() => handleSwitchTechnique('box')}
          >
            Box Breathing (4-4-4-4)
          </button>
          <button
            className={`nav-btn ${technique === '478' ? 'active' : ''}`}
            onClick={() => handleSwitchTechnique('478')}
          >
            4-7-8 Relaxation Method
          </button>
        </div>

        {/* Breathing Animation Circle */}
        <div className={`breathing-box ${isActive ? getPhaseClass() : ''}`}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{isActive ? phase : 'Ready'}</div>
            <div style={{ fontSize: '2.5rem', fontWeight: 700, opacity: 0.9 }}>{isActive ? countdown : ''}</div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '2.5rem' }}>
          <button className="btn-primary" onClick={toggleStart} style={{ padding: '0.9rem 2.5rem' }}>
            {isActive ? <Pause size={18} /> : <Play size={18} />}
            {isActive ? 'Pause Exercise' : 'Begin Breathing'}
          </button>
          
          <button className="btn-secondary" onClick={handleReset}>
            <RotateCcw size={18} />
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
