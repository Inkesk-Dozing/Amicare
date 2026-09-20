import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles, PhoneCall, ShieldCheck, Activity, GraduationCap, ArrowRight, Compass, HeartPulse, AlertCircle, CheckCircle2, Award, Zap, Heart, MessageCircle } from 'lucide-react';

export default function ChatbotLanding({ onNavigateTab }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Welcome to AmiCare. I am your confidential student mental well-being companion. I am here to listen empathetically and help reflect your current stress level as we talk. How are you feeling today?",
      suggested_actions: ["I feel stressed about my exams", "I'm having trouble sleeping", "I feel overwhelmed and anxious", "Start Stress Self-Check"],
      cards: []
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentState, setCurrentState] = useState({
    state_label: "Baseline / Active Listening",
    severity: "Low",
    primary_emotion: "Manageable",
    confidence: "Medium"
  });

  // Interactive PSS-4 assessment state inside chat
  const [assessmentActive, setAssessmentActive] = useState(false);
  const [qIndex, setQIndex] = useState(0);
  const [assessmentAnswers, setAssessmentAnswers] = useState([]);

  const pssQuestions = [
    { id: 1, prompt: "In the last month, how often have you felt overwhelmed by academic deadlines or personal commitments?", opts: ["Never", "Almost Never", "Sometimes", "Fairly Often", "Very Often"] },
    { id: 2, prompt: "In the last month, how often have you felt unable to control important things in your student life?", opts: ["Never", "Almost Never", "Sometimes", "Fairly Often", "Very Often"] },
    { id: 3, prompt: "In the last month, how often have you felt confident in your ability to handle personal or study problems?", opts: ["Very Often", "Fairly Often", "Sometimes", "Almost Never", "Never"] },
    { id: 4, prompt: "In the last month, how often have you felt that difficulties were piling up so high you could not overcome them?", opts: ["Never", "Almost Never", "Sometimes", "Fairly Often", "Very Often"] }
  ];

  const chatBottomRef = useRef(null);
  const chatSectionRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping, assessmentActive, currentState]);

  const scrollToChat = () => {
    chatSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async (textToSend) => {
    const userMsg = textToSend || inputText;
    if (!userMsg.trim()) return;

    const userMessageObj = { id: Date.now(), sender: 'user', text: userMsg };
    setMessages(prev => [...prev, userMessageObj]);
    if (!textToSend) setInputText('');
    setIsTyping(true);

    if (userMsg.toLowerCase().includes('assessment') || userMsg.toLowerCase().includes('self-check') || userMsg.toLowerCase().includes('stress check')) {
      setTimeout(() => {
        setIsTyping(false);
        setAssessmentActive(true);
        setQIndex(0);
        setAssessmentAnswers([]);
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'bot',
          text: "Starting your 2-minute non-diagnostic PSS-4 Stress Self-Check. Please select an answer for the question below:",
          suggested_actions: [],
          cards: []
        }]);
      }, 500);
      return;
    }

    if (userMsg.toLowerCase().includes('breathing') || userMsg.toLowerCase().includes('breathe')) {
      setTimeout(() => {
        setIsTyping(false);
        onNavigateTab('breathing');
      }, 500);
      return;
    }

    if (userMsg.toLowerCase().includes('helpline') || userMsg.toLowerCase().includes('crisis') || userMsg.toLowerCase().includes('call')) {
      setTimeout(() => {
        setIsTyping(false);
        onNavigateTab('helplines');
      }, 500);
      return;
    }

    // Call API with chat history context to infer user's state of being
    try {
      const historyPayload = messages.map(m => ({ sender: m.sender, text: m.text }));
      const res = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, history: historyPayload })
      });

      if (res.ok) {
        const data = await res.json();
        setIsTyping(false);
        
        // Update autonomously determined state of being
        if (data.inferred_state) {
          setCurrentState(data.inferred_state);
        }

        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'bot',
          text: data.reply,
          suggested_actions: data.suggested_actions || [],
          cards: data.cards || []
        }]);
      } else {
        fallbackReply(userMsg);
      }
    } catch (err) {
      fallbackReply(userMsg);
    }
  };

  const fallbackReply = (userMsg) => {
    setIsTyping(false);
    setMessages(prev => [...prev, {
      id: Date.now() + 1,
      sender: 'bot',
      text: "I am listening closely. Based on our dialogue, taking a quick stress assessment or rhythmic breathing exercise can help bring clarity.",
      suggested_actions: ["Start Stress Self-Check", "Find Emergency Helplines", "Guided Box Breathing"],
      cards: []
    }]);
  };

  const handleAssessmentAnswer = (scoreValue, label) => {
    const newAnswers = [...assessmentAnswers, scoreValue];
    setAssessmentAnswers(newAnswers);

    setMessages(prev => [...prev, { id: Date.now(), sender: 'user', text: label }]);

    if (qIndex < pssQuestions.length - 1) {
      setQIndex(prev => prev + 1);
    } else {
      setAssessmentActive(false);
      const total = newAnswers.reduce((a, b) => a + b, 0);
      let level = total > 10 ? "Elevated Stress" : total > 5 ? "Moderate Stress" : "Low Stress";
      
      setCurrentState({
        state_label: `PSS Score: ${total}/16 (${level})`,
        severity: level.split(' ')[0],
        primary_emotion: total > 10 ? "Anxiety" : "Stress",
        confidence: "High"
      });

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'bot',
        text: `Self-Assessment Completed! Score: ${total}/16 (${level}). Reaching out for support or taking short rest breaks can make a big difference.`,
        suggested_actions: ["Find Emergency Helplines", "Guided Box Breathing", "Retake Assessment"],
        cards: [
          { type: "helpline", name: "Tele-MANAS (Govt. of India)", number: "14416", category: "24/7 National Crisis Line" },
          { type: "helpline", name: "KIRAN Helpline", number: "1800-599-0019", category: "24/7 Mental Health Line" }
        ]
      }]);
    }
  };

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      {/* Top Academic & Project Badges */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap', paddingTop: '2rem' }}>
        <span className="badge-tag"><ShieldCheck size={14} /> Confidential & Non-Diagnostic</span>
        <span className="badge-tag" style={{ background: '#EBF5F0', color: '#1B4D3E', borderColor: '#C3E2D5' }}><Activity size={14} /> UN SDG 3: Good Health</span>
        <span className="badge-tag" style={{ background: '#EEF2FF', color: '#3730A3', borderColor: '#C7D2FE' }}><GraduationCap size={14} /> K.R. Mangalam University</span>
      </div>

      {/* Main Hero Section */}
      <div className="hero-section">
        <div>
          <h1 className="hero-title" style={{ textAlign: 'left', fontSize: '2.8rem', lineHeight: '1.18', color: 'var(--text-main)' }}>
            Your Safe Haven for Campus Mental Well-Being
          </h1>
          <p className="hero-subtitle" style={{ textAlign: 'left', margin: '1.25rem 0 2rem', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
            Talk through exam pressure, sleep fatigue, or academic stress. AmiCare provides a safe, confidential space for emotional self-reflection, connects you with 24/7 helplines, and guides you through mindfulness exercises.
          </p>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <button className="btn-primary" onClick={scrollToChat}>
              <MessageCircle size={18} /> Talk to AmiCare Companion
            </button>
            <button className="btn-secondary" onClick={() => handleSend("Start Stress Self-Check")}>
              <Sparkles size={18} /> Take 2-Min Stress Check
            </button>
            <button className="btn-secondary" onClick={() => onNavigateTab('helplines')}>
              <PhoneCall size={18} /> 24/7 Helpline DB
            </button>
          </div>
        </div>

        {/* Hero Image Showcase Card */}
        <div className="hero-graphic-card">
          <img src="/authentic_student_wellness.jpg" alt="Student Mental Wellness Haven" className="hero-graphic-img" />
          
          <div className="floating-glass-badge" style={{ top: '20px', left: '20px' }}>
            <div className="logo-icon" style={{ width: '32px', height: '32px', background: '#1B4D3E' }}><PhoneCall size={16} /></div>
            <div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700 }}>24/7 CRISIS HELPLINE</div>
              <div style={{ fontSize: '0.9rem', color: '#1B4D3E', fontWeight: 800 }}>Tele-MANAS: 14416</div>
            </div>
          </div>

          <div className="floating-glass-badge" style={{ bottom: '20px', right: '20px' }}>
            <div className="logo-icon" style={{ width: '32px', height: '32px', background: '#2A725D' }}><HeartPulse size={16} /></div>
            <div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700 }}>SELF-ASSESSMENT</div>
              <div style={{ fontSize: '0.9rem', color: '#2A725D', fontWeight: 800 }}>PSS-4 Stress Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Statistics Counters */}
      <div className="stat-card-grid">
        <div className="stat-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: 'var(--primary-teal)', marginBottom: '0.4rem' }}>
            <ShieldCheck size={20} />
            <span style={{ fontWeight: 800, fontSize: '1.25rem', color: 'var(--text-main)' }}>100% Free</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Anonymous & confidential student mental support</div>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: 'var(--primary-teal)', marginBottom: '0.4rem' }}>
            <PhoneCall size={20} />
            <span style={{ fontWeight: 800, fontSize: '1.25rem', color: 'var(--text-main)' }}>24/7 Access</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Direct connection to Tele-MANAS & KIRAN lines</div>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: 'var(--primary-teal)', marginBottom: '0.4rem' }}>
            <Zap size={20} />
            <span style={{ fontWeight: 800, fontSize: '1.25rem', color: 'var(--text-main)' }}>4-4-4-4 Rhythm</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Guided Box Breathing for exam panic relief</div>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: 'var(--primary-teal)', marginBottom: '0.4rem' }}>
            <Compass size={20} />
            <span style={{ fontWeight: 800, fontSize: '1.25rem', color: 'var(--text-main)' }}>5-4-3-2-1 Tool</span>
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Sensory grounding exercise for acute stress</div>
        </div>
      </div>

      {/* Feature Showcase Grid */}
      <div style={{ margin: '3.5rem 0 2.5rem' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2.2rem', marginBottom: '0.5rem' }}>Platform Features & Support Tools</h2>
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '2rem' }}>Comprehensive resources tailored to help students manage stress early.</p>

        <div className="feature-showcase-grid">
          <div className="feature-card">
            <div>
              <div className="feature-icon-wrapper"><MessageCircle size={24} /></div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Emotional Support Companion</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                Converse naturally with AmiCare. The companion actively listens and helps reflect your emotional stress state as you talk.
              </p>
            </div>
            <button className="btn-secondary" style={{ marginTop: '1.25rem', padding: '0.55rem 1rem', fontSize: '0.85rem' }} onClick={scrollToChat}>
              Start Conversation <ArrowRight size={14} />
            </button>
          </div>

          <div className="feature-card">
            <div>
              <div className="feature-icon-wrapper" style={{ background: '#FEF3C7', color: '#D97706', borderColor: '#FDE68A' }}><Activity size={24} /></div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Stress Self-Assessment</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                Validated non-diagnostic PSS-4 Perceived Stress Scale that calculates your stress index in under 2 minutes.
              </p>
            </div>
            <button className="btn-secondary" style={{ marginTop: '1.25rem', padding: '0.55rem 1rem', fontSize: '0.85rem' }} onClick={() => handleSend("Start Stress Self-Check")}>
              Take Self-Check <ArrowRight size={14} />
            </button>
          </div>

          <div className="feature-card">
            <div>
              <div className="feature-icon-wrapper" style={{ background: '#FFF1F2', color: '#BE123C', borderColor: '#FECDD3' }}><PhoneCall size={24} /></div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Helpline Directory DB</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                Verified database of 24/7 crisis numbers (Tele-MANAS, KIRAN, Vandrevala) with instant click-to-call functionality.
              </p>
            </div>
            <button className="btn-secondary" style={{ marginTop: '1.25rem', padding: '0.55rem 1rem', fontSize: '0.85rem' }} onClick={() => onNavigateTab('helplines')}>
              View Helplines <ArrowRight size={14} />
            </button>
          </div>

          <div className="feature-card">
            <div>
              <div className="feature-icon-wrapper" style={{ background: '#F0FDF4', color: '#166534', borderColor: '#BBF7D0' }}><Compass size={24} /></div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Self-Care & Grounding</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                Interactive 5-4-3-2-1 sensory grounding and 4-4-4-4 Box Breathing tools to soothe physical anxiety immediately.
              </p>
            </div>
            <button className="btn-secondary" style={{ marginTop: '1.25rem', padding: '0.55rem 1rem', fontSize: '0.85rem' }} onClick={() => onNavigateTab('resources')}>
              Explore Self-Care <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Main Interactive AI Chatbot Window */}
      <div ref={chatSectionRef} style={{ paddingTop: '1.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.25rem' }}>
          <h2 style={{ fontSize: '2rem' }}>Interactive AmiCare Companion</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>Share what is on your mind below — AmiCare provides supportive dialogue and helps reflect your stress level.</p>
        </div>

        {/* Real-time State of Being Banner */}
        <div className="glass-card" style={{ maxWidth: '860px', margin: '0 auto 1.5rem', padding: '1rem 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', borderLeft: '4px solid var(--primary-teal)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <HeartPulse size={22} color="var(--primary-teal)" />
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 700 }}>
                Current Emotional State
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)' }}>
                {currentState.state_label}
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Severity:</span>
            <span style={{
              fontSize: '0.78rem', fontWeight: 700, padding: '0.25rem 0.75rem', borderRadius: '12px',
              background: currentState.severity === 'Elevated' ? '#FFF1F2' : currentState.severity === 'Moderate' ? '#FEF3C7' : '#EBF5F0',
              color: currentState.severity === 'Elevated' ? '#BE123C' : currentState.severity === 'Moderate' ? '#92400E' : '#1B4D3E',
              border: '1px solid var(--glass-border)'
            }}>
              {currentState.severity}
            </span>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="glass-card chat-container">
          {/* Chat Header */}
          <div className="chat-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
              <img src="/authentic_care_avatar.jpg" alt="AmiCare Companion Avatar" style={{ width: '38px', height: '38px', borderRadius: '50%', objectFit: 'cover', border: '1px solid var(--primary-teal)' }} />
              <div>
                <h3 style={{ fontSize: '1.1rem', color: 'var(--text-main)' }}>AmiCare Companion</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--primary-teal)', display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: 600 }}>
                  <span style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#10B981' }}></span>
                  Online • Active Emotional Listening
                </div>
              </div>
            </div>
            <button className="btn-secondary" style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }} onClick={() => onNavigateTab('helplines')}>
              <PhoneCall size={14} /> 24/7 Helpline: 14416
            </button>
          </div>

          {/* Chat Messages */}
          <div className="chat-messages">
            {messages.map(msg => (
              <div key={msg.id} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start' }}>
                <div style={{ display: 'flex', gap: '0.75rem', maxWidth: '82%', flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row' }}>
                  {msg.sender === 'user' ? (
                    <div style={{
                      width: '32px', height: '32px', borderRadius: '50%',
                      background: 'var(--primary-teal)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0
                    }}>
                      <User size={16} />
                    </div>
                  ) : (
                    <img src="/authentic_care_avatar.jpg" alt="Avatar" style={{ width: '32px', height: '32px', borderRadius: '50%', objectFit: 'cover', flexShrink: 0, border: '1px solid var(--primary-teal)' }} />
                  )}

                  <div className={`chat-bubble ${msg.sender === 'user' ? 'user' : ''}`}>
                    {msg.text}

                    {msg.cards && msg.cards.length > 0 && (
                      <div style={{ marginTop: '0.85rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                        {msg.cards.map((c, idx) => (
                          <div key={idx} style={{ background: '#F8FAFC', padding: '0.85rem 1rem', borderRadius: '12px', border: '1px solid #E2E8F0', color: 'var(--text-main)' }}>
                            <div style={{ fontSize: '0.75rem', color: 'var(--primary-teal)', fontWeight: 700 }}>{c.category || 'HELPLINE'}</div>
                            <div style={{ fontWeight: 700, fontSize: '0.98rem', margin: '0.2rem 0', color: 'var(--text-main)' }}>{c.name || c.title}</div>
                            {c.number && (
                              <div style={{ fontSize: '0.9rem', color: 'var(--primary-teal)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                                <PhoneCall size={14} /> {c.number}
                              </div>
                            )}
                            {c.number && (
                              <a href={`tel:${c.number.split('/')[0]}`} className="call-btn" style={{ marginTop: '0.6rem', padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>
                                <PhoneCall size={12} /> Call Helpline
                              </a>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                  <div style={{ display: 'flex', gap: '0.45rem', flexWrap: 'wrap', marginTop: '0.65rem', marginLeft: '2.5rem' }}>
                    {msg.suggested_actions.map((act, idx) => (
                      <button
                        key={idx}
                        className="action-chip"
                        onClick={() => handleSend(act)}
                      >
                        <Sparkles size={12} /> {act}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {assessmentActive && (
              <div style={{ marginLeft: '2.5rem', background: '#FFFFFF', padding: '1.25rem', borderRadius: '16px', border: '1px solid var(--primary-teal)', maxWidth: '85%', boxShadow: '0 4px 16px rgba(0,0,0,0.06)' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--primary-teal)', fontWeight: 700, marginBottom: '0.35rem' }}>
                  PSS-4 Scale • Question {qIndex + 1} of {pssQuestions.length}
                </div>
                <div style={{ fontWeight: 600, fontSize: '0.98rem', marginBottom: '1rem', color: 'var(--text-main)' }}>
                  {pssQuestions[qIndex].prompt}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {pssQuestions[qIndex].opts.map((opt, val) => (
                    <button
                      key={val}
                      className="option-btn"
                      style={{ padding: '0.65rem 1rem', fontSize: '0.88rem' }}
                      onClick={() => handleAssessmentAnswer(val, opt)}
                    >
                      <span>{opt}</span>
                      <ArrowRight size={14} />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {isTyping && (
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginLeft: '2.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                <MessageCircle size={16} color="var(--primary-teal)" /> AmiCare is preparing a response...
              </div>
            )}

            <div ref={chatBottomRef} />
          </div>

          {/* Input Bar */}
          <div style={{ padding: '1rem 1.5rem', background: '#FFFFFF', borderTop: '1px solid var(--glass-border)', display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <input
              type="text"
              placeholder="Share what is on your mind today — exams, stress, sleep, or feeling overwhelmed..."
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              style={{
                flex: 1,
                background: '#F8FAFC',
                border: '1px solid #CBD5E1',
                borderRadius: 'var(--radius-full)',
                padding: '0.8rem 1.25rem',
                color: 'var(--text-main)',
                fontSize: '0.95rem',
                outline: 'none'
              }}
            />
            <button className="btn-primary" onClick={() => handleSend()} style={{ padding: '0.8rem 1.4rem' }}>
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
