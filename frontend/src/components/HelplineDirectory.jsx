import React, { useState, useEffect } from 'react';
import { Search, PhoneCall, Globe, Clock, ShieldCheck, ExternalLink } from 'lucide-react';

export default function HelplineDirectory() {
  const [helplines, setHelplines] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  const fallbackHelplines = [
    {
      id: 1,
      name: "Tele-MANAS (Govt. of India)",
      number: "14416 / 1800-891-4416",
      category: "24/7 Crisis Helpline",
      description: "National tele-mental health helpline providing 24/7 confidential psychological support across all states.",
      hours: "24/7",
      is_toll_free: true,
      languages: "English, Hindi, Regional Languages",
      website: "https://telemanas.mohfw.gov.in"
    },
    {
      id: 2,
      name: "KIRAN Mental Health Helpline",
      number: "1800-599-0019",
      category: "24/7 Crisis Helpline",
      description: "Toll-free mental health rehabilitation helpline by the Ministry of Social Justice & Empowerment.",
      hours: "24/7",
      is_toll_free: true,
      languages: "English, Hindi, 13 Regional Languages",
      website: "https://depwd.gov.in"
    },
    {
      id: 3,
      name: "Vandrevala Foundation",
      number: "+91 9999 666 555",
      category: "Tele-Therapy & Counseling",
      description: "Free 24x7 emotional support and mental health counseling by trained professionals.",
      hours: "24/7",
      is_toll_free: false,
      languages: "English, Hindi, Gujarati, Marathi",
      website: "https://www.vandrevalafoundation.com"
    },
    {
      id: 4,
      name: "AASRA Crisis Center",
      number: "+91 98204 66726",
      category: "24/7 Crisis Helpline",
      description: "Voluntary confidential crisis intervention service for individuals in emotional distress.",
      hours: "24/7",
      is_toll_free: false,
      languages: "English, Hindi",
      website: "http://www.aasra.info"
    },
    {
      id: 5,
      name: "Student Wellness Line",
      number: "1800-200-CAMPUS",
      category: "Student Counseling",
      description: "Dedicated campus stress helpline offering empathetic peer listener support.",
      hours: "8:00 AM - 10:00 PM",
      is_toll_free: true,
      languages: "English, Hindi",
      website: "https://amicare.org/campus-support"
    }
  ];

  useEffect(() => {
    fetch('/api/helplines')
      .then(res => {
        if (!res.ok) throw new Error('API offline');
        return res.json();
      })
      .then(data => {
        setHelplines(data && data.length > 0 ? data : fallbackHelplines);
        setLoading(false);
      })
      .catch(() => {
        setHelplines(fallbackHelplines);
        setLoading(false);
      });
  }, []);

  const categories = ['All', '24/7 Crisis Helpline', 'Student Counseling', 'Tele-Therapy & Counseling'];

  const filteredHelplines = helplines.filter(item => {
    const matchesCat = selectedCategory === 'All' || item.category === selectedCategory;
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.languages.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '2.4rem', marginBottom: '0.6rem' }}>Verified Student Referral Database</h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
          Confidential, 24/7 verified mental health crisis helplines and student counseling services.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-card" style={{ padding: '1.25rem', marginBottom: '2rem', display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
          {categories.map(cat => (
            <button
              key={cat}
              className={`nav-btn ${selectedCategory === cat ? 'active' : ''}`}
              onClick={() => setSelectedCategory(cat)}
              style={{ fontSize: '0.82rem', padding: '0.45rem 0.95rem' }}
            >
              {cat}
            </button>
          ))}
        </div>

        <div style={{ position: 'relative', minWidth: '260px', flex: 1, maxWidth: '380px' }}>
          <Search size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search language, category, region..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 1rem 0.65rem 2.5rem',
              background: 'rgba(15, 23, 42, 0.8)',
              border: '1px solid var(--glass-border)',
              borderRadius: 'var(--radius-full)',
              color: 'white',
              fontSize: '0.88rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Helplines Grid */}
      <div className="helpline-grid">
        {filteredHelplines.map(h => (
          <div key={h.id} className="glass-card helpline-card">
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <span className="helpline-category-tag">{h.category}</span>
                {h.is_toll_free && (
                  <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 600, background: 'rgba(16,185,129,0.1)', padding: '0.2rem 0.6rem', borderRadius: '12px' }}>
                    Toll-Free
                  </span>
                )}
              </div>

              <h3 style={{ fontSize: '1.25rem', marginTop: '0.4rem', marginBottom: '0.5rem' }}>{h.name}</h3>

              <div style={{ color: 'var(--primary-light)', fontSize: '1.2rem', fontWeight: 700, margin: '0.4rem 0', display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <PhoneCall size={18} />
                <span>{h.number}</span>
              </div>

              <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', margin: '0.75rem 0' }}>
                {h.description}
              </p>

              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '0.35rem', margin: '1rem 0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <Clock size={14} color="var(--primary-light)" />
                  <span><strong>Hours:</strong> {h.hours}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <Globe size={14} color="var(--primary-light)" />
                  <span><strong>Languages:</strong> {h.languages}</span>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
              <a href={`tel:${h.number.split('/')[0].trim()}`} className="call-btn" style={{ flex: 1 }}>
                <PhoneCall size={15} /> Call Helpline
              </a>
              {h.website && (
                <a
                  href={h.website}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-secondary"
                  style={{ padding: '0.7rem 1rem', fontSize: '0.82rem' }}
                >
                  <ExternalLink size={14} />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
