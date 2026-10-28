import React, { useState } from 'react';
import Navbar from './components/Navbar';
import ChatbotLanding from './components/ChatbotLanding';
import HelplineDirectory from './components/HelplineDirectory';
import BreathingExercise from './components/BreathingExercise';
import ResourceHub from './components/ResourceHub';
import DisclaimerFooter from './components/DisclaimerFooter';

export default function App() {
  const [activeTab, setActiveTab] = useState('chatbot');

  return (
    <div className="app-layout">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main>
        {activeTab === 'chatbot' && <ChatbotLanding onNavigateTab={setActiveTab} />}
        {activeTab === 'helplines' && <HelplineDirectory />}
        {activeTab === 'breathing' && <BreathingExercise />}
        {activeTab === 'resources' && <ResourceHub onLaunchBreathing={() => setActiveTab('breathing')} />}
      </main>

      <DisclaimerFooter />
    </div>
  );
}
