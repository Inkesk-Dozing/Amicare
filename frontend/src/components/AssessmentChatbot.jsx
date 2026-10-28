import React, { useState, useEffect } from 'react';
import { Sparkles, CheckCircle2, RotateCcw, Phone, ArrowRight, ShieldCheck, Activity } from 'lucide-react';

export default function AssessmentChatbot({ onNavigateHelplines }) {
  const [assessmentType, setAssessmentType] = useState('pss'); // 'pss', 'gad7', 'phq9'
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [evaluation, setEvaluation] = useState(null);

  // Assessment Scale Data Sets
  const pssQuestions = [
    {
      id: 1,
      prompt: "In the last month, how often have you felt overwhelmed by academic deadlines or personal commitments?",
      options: [
        { label: "Never", value: 0 },
        { label: "Almost Never", value: 1 },
        { label: "Sometimes", value: 2 },
        { label: "Fairly Often", value: 3 },
        { label: "Very Often", value: 4 }
      ]
    },
    {
      id: 2,
      prompt: "In the last month, how often have you felt unable to control the important things in your student life?",
      options: [
        { label: "Never", value: 0 },
        { label: "Almost Never", value: 1 },
        { label: "Sometimes", value: 2 },
        { label: "Fairly Often", value: 3 },
        { label: "Very Often", value: 4 }
      ]
    },
    {
      id: 3,
      prompt: "In the last month, how often have you felt confident in your ability to handle personal or study problems?",
      options: [
        { label: "Very Often", value: 0 },
        { label: "Fairly Often", value: 1 },
        { label: "Sometimes", value: 2 },
        { label: "Almost Never", value: 3 },
        { label: "Never", value: 4 }
      ]
    },
    {
      id: 4,
      prompt: "In the last month, how often have you felt that difficulties were piling up so high that you could not overcome them?",
      options: [
        { label: "Never", value: 0 },
        { label: "Almost Never", value: 1 },
        { label: "Sometimes", value: 2 },
        { label: "Fairly Often", value: 3 },
        { label: "Very Often", value: 4 }
      ]
    }
  ];

  const gad7Questions = [
    {
      id: 1,
      prompt: "Over the last 2 weeks, how often have you felt nervous, anxious, or on edge regarding study performance?",
      options: [
        { label: "Not at all", value: 0 },
        { label: "Several days", value: 1 },
        { label: "More than half the days", value: 2 },
        { label: "Nearly every day", value: 3 }
      ]
    },
    {
      id: 2,
      prompt: "Over the last 2 weeks, how often have you not been able to stop or control worrying?",
      options: [
        { label: "Not at all", value: 0 },
        { label: "Several days", value: 1 },
        { label: "More than half the days", value: 2 },
        { label: "Nearly every day", value: 3 }
      ]
    },
    {
      id: 3,
      prompt: "Over the last 2 weeks, how often have you experienced trouble relaxing before exams or presentations?",
      options: [
        { label: "Not at all", value: 0 },
        { label: "Several days", value: 1 },
        { label: "More than half the days", value: 2 },
        { label: "Nearly every day", value: 3 }
      ]
    }
  ];

  const questions = assessmentType === 'pss' ? pssQuestions : gad7Questions;

  const handleSelectOption = (questionId, scoreValue) => {
    const updatedAnswers = [...answers.filter(a => a.question_id !== questionId), { question_id: questionId, score: scoreValue }];
    setAnswers(updatedAnswers);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      evaluateResult(updatedAnswers);
    }
  };

  const evaluateResult = (finalAnswers) => {
    const total = finalAnswers.reduce((sum, item) => sum + item.score, 0);
    const maxScore = assessmentType === 'pss' ? 16 : 9;
    let level = "Low Stress";
    let summary = "Your stress levels appear manageable right now. You are handling current demands well.";
    let recommendations = [
      "Maintain your healthy daily routines and consistent sleep schedule.",
      "Try our Box Breathing exercise for quick 2-minute relaxation micro-breaks.",
      "Keep up social connections and regular physical activity."
    ];

    if (total > maxScore * 0.6) {
      level = "Elevated Stress";
      summary = "Your stress level is currently high. Reaching out for support can make a big difference.";
      recommendations = [
        "Pause demanding tasks and take immediate rest.",
        "Connect directly with one of our free 24/7 confidential helplines below.",
        "Talk to a campus counselor or professional helper."
      ];
    } else if (total > maxScore * 0.3) {
      level = "Moderate Stress";
      summary = "You are experiencing moderate stress. It is common during exam peaks.";
      recommendations = [
        "Break large academic projects into smaller 25-minute focus intervals.",
        "Use the 4-7-8 Breathing Tool to reduce physical tension.",
        "Consider reaching out to a student counselor or peer mentor."
      ];
    }

    setEvaluation({
      total_score: total,
      max_score: maxScore,
      level,
      summary,
      recommendations,
      recommended_helplines: [
        {
          id: 1,
          name: "Tele-MANAS (Govt. of India)",
          number: "14416 / 1800-891-4416",
          category: "24/7 Crisis Helpline",
          description: "National tele-mental health helpline providing 24/7 confidential psychological support.",
          hours: "24/7",
          is_toll_free: true
        },
        {
          id: 2,
          name: "KIRAN Mental Health Helpline",
          number: "1800-599-0019",
          category: "24/7 Crisis Helpline",
          description: "Toll-free mental health helpline by the Ministry of Social Justice & Empowerment.",
          hours: "24/7",
          is_toll_free: true
        }
      ]
    });
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setAnswers([]);
    setEvaluation(null);
  };

  const handleSwitchType = (type) => {
    setAssessmentType(type);
    setCurrentIndex(0);
    setAnswers([]);
    setEvaluation(null);
  };

  const currentQ = questions[currentIndex];
  const progressPercent = questions.length ? Math.round(((currentIndex + 1) / questions.length) * 100) : 0;

  return (
    <div className="assessment-container glass-card">
      <div className="chat-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Sparkles color="var(--primary-light)" size={24} />
          <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)' }}>AmiCare Student Self-Check</h3>
        </div>
        
        {/* Assessment Framework Switcher */}
        <div style={{ display: 'flex', gap: '0.35rem', background: 'rgba(15,23,42,0.6)', padding: '0.25rem', borderRadius: 'var(--radius-full)' }}>
          <button
            className={`nav-btn ${assessmentType === 'pss' ? 'active' : ''}`}
            onClick={() => handleSwitchType('pss')}
            style={{ fontSize: '0.75rem', padding: '0.3rem 0.8rem' }}
          >
            PSS-4 Stress Scale
          </button>
          <button
            className={`nav-btn ${assessmentType === 'gad7' ? 'active' : ''}`}
            onClick={() => handleSwitchType('gad7')}
            style={{ fontSize: '0.75rem', padding: '0.3rem 0.8rem' }}
          >
            GAD Anxiety Check
          </button>
        </div>
      </div>

      {!evaluation ? (
        <div>
          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }}></div>
          </div>

          <div className="question-card">
            <div className="question-number">
              {assessmentType.toUpperCase()} Scale • Question {currentIndex + 1} of {questions.length}
            </div>
            <h2 className="question-prompt">{currentQ.prompt}</h2>

            <div className="options-grid">
              {currentQ.options.map((opt, idx) => {
                const isSelected = answers.some(a => a.question_id === currentQ.id && a.score === opt.value);
                return (
                  <button
                    key={idx}
                    className={`option-btn ${isSelected ? 'selected' : ''}`}
                    onClick={() => handleSelectOption(currentQ.id, opt.value)}
                  >
                    <span>{opt.label}</span>
                    <ArrowRight size={16} />
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        <div className="result-card">
          <div className={`result-badge ${evaluation.level.toLowerCase().split(' ')[0]}`}>
            {evaluation.level}
          </div>

          <div className="result-score">
            {evaluation.total_score} <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ {evaluation.max_score} Score</span>
          </div>

          <p className="result-summary">{evaluation.summary}</p>

          <div className="recommendations-list">
            <h4>Recommended Next Steps:</h4>
            <ul>
              {evaluation.recommendations.map((rec, i) => (
                <li key={i}>
                  <CheckCircle2 size={18} color="var(--primary-light)" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>

          <h4 style={{ textAlign: 'left', marginBottom: '1rem', color: 'var(--text-primary)' }}>High-Priority Verified Helplines:</h4>
          <div className="helpline-grid" style={{ marginTop: '1rem', marginBottom: '2rem' }}>
            {evaluation.recommended_helplines.map(h => (
              <div key={h.id} className="glass-card helpline-card" style={{ padding: '1.25rem' }}>
                <div>
                  <span className="helpline-category-tag">{h.category}</span>
                  <h4 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}>{h.name}</h4>
                  <div className="helpline-number">
                    <Phone size={16} />
                    <span>{h.number}</span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{h.description}</p>
                </div>
                <a href={`tel:${h.number.split('/')[0].trim()}`} className="call-btn" style={{ marginTop: '1rem' }}>
                  <Phone size={14} /> Call Helpline Now
                </a>
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            <button className="btn-secondary" onClick={handleRestart}>
              <RotateCcw size={16} />
              Retake Assessment
            </button>
            
            <button className="btn-primary" onClick={onNavigateHelplines}>
              Browse Full Helpline DB
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
