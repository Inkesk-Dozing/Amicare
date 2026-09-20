import React from 'react';
import { HeartPulse, PhoneCall, Bot, Wind, BookOpen } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <nav className="navbar">
      <div className="container nav-content">
        <a href="#home" className="brand-logo" onClick={() => setActiveTab('chatbot')}>
          <img src="/authentic_care_avatar_clean.png" alt="AmiCare Logo" style={{ width: '38px', height: '38px', objectFit: 'contain' }} />
          <span>AmiCare</span>
        </a>

        <div className="nav-links">
          <button
            className={`nav-btn ${activeTab === 'chatbot' ? 'active' : ''}`}
            onClick={() => setActiveTab('chatbot')}
          >
            <Bot size={16} />
            AmiCare Assistant
          </button>

          <button
            className={`nav-btn ${activeTab === 'helplines' ? 'active' : ''}`}
            onClick={() => setActiveTab('helplines')}
          >
            <PhoneCall size={16} />
            Helpline DB
          </button>

          <button
            className={`nav-btn ${activeTab === 'breathing' ? 'active' : ''}`}
            onClick={() => setActiveTab('breathing')}
          >
            <Wind size={16} />
            Breathing Tool
          </button>

          <button
            className={`nav-btn ${activeTab === 'resources' ? 'active' : ''}`}
            onClick={() => setActiveTab('resources')}
          >
            <BookOpen size={16} />
            Self-Care Hub
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <a href="tel:14416" className="emergency-badge">
            <PhoneCall size={14} />
            <span>24/7 Crisis: 14416</span>
          </a>
        </div>
      </div>
    </nav>
  );
}
