'use client';

import { useState, useRef } from 'react';
import { Mic, Music, Sparkles, Play, Pause, RotateCcw } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface SongBlueprint {
  core_emotion: string;
  singing_to: string;
  narrative_summary: string;
  key_metaphor_or_image: string;
  sonic_vibe: string;
  tempo_and_energy: string;
  instrumentation_ideas: string[];
  vocal_style: string;
  artist_purpose: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Welcome to the studio! I'm uPOP, your AI producer. Before we dive in, some artists like to talk a bit about what kind of stories make great songs, while others prefer to jump right in. Would you like a little guidance on finding a song-worthy story, or are you ready to tell me yours?",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [blueprint, setBlueprint] = useState<SongBlueprint | null>(null);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [currentAudio, setCurrentAudio] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputValue.trim(),
          conversation: messages.map(m => ({ role: m.role, content: m.content }))
        })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: "Sorry, I'm having trouble connecting right now. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateBlueprint = async () => {
    if (messages.length < 2) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/blueprint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          conversation: messages.map(m => ({ role: m.role, content: m.content }))
        })
      });

      if (!response.ok) throw new Error('Failed to generate blueprint');

      const data = await response.json();
      setBlueprint(data.blueprint);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAudio = async () => {
    if (!blueprint) return;

    setIsGeneratingAudio(true);
    try {
      const prompt = `Create a ${blueprint.sonic_vibe} instrumental track with ${blueprint.tempo_and_energy}. The mood should capture ${blueprint.core_emotion}. ${blueprint.instrumentation_ideas.join(', ')}.`;

      const response = await fetch('/api/audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) throw new Error('Failed to generate audio');

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      setCurrentAudio(audioUrl);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsGeneratingAudio(false);
    }
  };

  const togglePlayback = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const resetSession = () => {
    setMessages([{
      role: 'assistant',
      content: "Welcome to the studio! I'm uPOP, your AI producer. Before we dive in, some artists like to talk a bit about what kind of stories make great songs, while others prefer to jump right in. Would you like a little guidance on finding a song-worthy story, or are you ready to tell me yours?",
      timestamp: new Date()
    }]);
    setBlueprint(null);
    setCurrentAudio(null);
    setIsPlaying(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/20 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
                <Music className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">uPOP</h1>
                <p className="text-sm text-gray-300">AI Music Producer</p>
              </div>
            </div>
            <button
              onClick={resetSession}
              className="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
            >
              <RotateCcw className="h-4 w-4 text-white" />
              <span className="text-white text-sm">New Session</span>
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 h-[600px] flex flex-col">
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
                <Sparkles className="h-5 w-5 mr-2" />
                Studio Conversation
              </h2>
              
              <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-4 rounded-2xl ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                          : 'bg-white/20 text-white'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      <p className="text-xs opacity-70 mt-2">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white/20 text-white p-4 rounded-2xl">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex space-x-3">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Tell me about your story..."
                  className="flex-1 px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputValue.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-medium transition-all"
                >
                  Send
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Blueprint */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Song Blueprint</h3>
                <button
                  onClick={generateBlueprint}
                  disabled={isLoading || messages.length < 2}
                  className="px-4 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-white text-sm font-medium transition-all"
                >
                  Generate
                </button>
              </div>

              {blueprint ? (
                <div className="space-y-4 text-sm">
                  <div>
                    <h4 className="text-white/80 font-medium">Core Emotion</h4>
                    <p className="text-white">{blueprint.core_emotion}</p>
                  </div>
                  <div>
                    <h4 className="text-white/80 font-medium">Sonic Vibe</h4>
                    <p className="text-white">{blueprint.sonic_vibe}</p>
                  </div>
                  <div>
                    <h4 className="text-white/80 font-medium">Tempo & Energy</h4>
                    <p className="text-white">{blueprint.tempo_and_energy}</p>
                  </div>
                  <div>
                    <h4 className="text-white/80 font-medium">Instrumentation</h4>
                    <p className="text-white">{blueprint.instrumentation_ideas.join(', ')}</p>
                  </div>
                  <div>
                    <h4 className="text-white/80 font-medium">Artist's Purpose</h4>
                    <p className="text-white italic">"{blueprint.artist_purpose}"</p>
                  </div>
                </div>
              ) : (
                <p className="text-white/60 text-sm">Your blueprint will appear here once generated.</p>
              )}
            </div>

            {/* Audio Generation */}
            {blueprint && (
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <Mic className="h-5 w-5 mr-2" />
                  Audio Sketch
                </h3>

                {currentAudio ? (
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <button
                        onClick={togglePlayback}
                        className="p-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 rounded-full text-white transition-all"
                      >
                        {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                      </button>
                      <div>
                        <p className="text-white font-medium">Generated Track</p>
                        <p className="text-white/60 text-sm">Based on your blueprint</p>
                      </div>
                    </div>
                    <audio
                      ref={audioRef}
                      src={currentAudio}
                      onEnded={() => setIsPlaying(false)}
                      className="w-full"
                    />
                  </div>
                ) : (
                  <button
                    onClick={generateAudio}
                    disabled={isGeneratingAudio}
                    className="w-full px-4 py-3 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-white font-medium transition-all"
                  >
                    {isGeneratingAudio ? 'Generating...' : 'Generate Audio Sketch'}
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}