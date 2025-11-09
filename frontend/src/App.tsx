import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './index.css';

interface AnalysisResult {
  feedAmount: number;
  confidence: number;
  costSavings: number;
  sustainabilityScore: number;
  fishActivity: string;
  timestamp: string;
}

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState<AnalysisResult | null>(null);
  const [historicalData, setHistoricalData] = useState<any[]>([]);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Simulate API call for video analysis
  const handleVideoUpload = async (file: File) => {
    setIsAnalyzing(true);
    
    // Simulate processing time
    setTimeout(() => {
      const mockResult: AnalysisResult = {
        feedAmount: 2.5 + Math.random() * 1.5, // 2.5-4.0 kg
        confidence: 0.85 + Math.random() * 0.14, // 85-99%
        costSavings: 10 + Math.random() * 20, // $10-30
        sustainabilityScore: 7 + Math.random() * 2.5, // 7-9.5
        fishActivity: ['Active', 'Moderate', 'High', 'Feeding'][Math.floor(Math.random() * 4)],
        timestamp: new Date().toISOString()
      };
      
      setCurrentAnalysis(mockResult);
      setIsAnalyzing(false);
    }, 3000);
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'} transition-colors duration-200`}>
      {/* Header */}
      <header className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} shadow-sm border-b`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="text-2xl">🐟</div>
              <div>
                <h1 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                  Logixon Smart AquaVision
                </h1>
                <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-500'}`}>
                  AI-Powered Fish Feed Optimization
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className={`p-2 rounded-lg ${isDarkMode ? 'bg-gray-700 text-gray-200' : 'bg-gray-100 text-gray-600'} hover:opacity-80 transition-opacity`}
              >
                {isDarkMode ? '☀️' : '🌙'}
              </button>
              
              <div className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                📍 UAE Aquaculture
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Welcome Section */}
          <div className={`${isDarkMode ? 'card-dark' : 'card'}`}>
            <div className="text-center">
              <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'} mb-2`}>
                Welcome to Smart AquaVision Dashboard
              </h2>
              <p className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'} max-w-2xl mx-auto`}>
                Upload fish pond videos and get AI-powered feeding recommendations to optimize costs 
                and promote sustainable aquaculture practices in the UAE.
              </p>
            </div>
          </div>

          {/* Status Bar */}
          {(isAnalyzing || currentAnalysis) && (
            <div className={`${isDarkMode ? 'card-dark border-primary-500' : 'card border-primary-200'} border-l-4`}>
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${isAnalyzing ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></div>
                <div>
                  <p className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                    {isAnalyzing ? 'Analyzing fish behavior...' : 'Analysis Complete'}
                  </p>
                  <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    {isAnalyzing ? 'AI is processing your video feed' : `Last updated: ${new Date().toLocaleTimeString()}`}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload Section */}
            <div className="lg:col-span-1">
              <VideoUpload onVideoUpload={handleVideoUpload} isAnalyzing={isAnalyzing} />
              
              {/* Quick Stats */}
              <div className={`${isDarkMode ? 'card-dark' : 'card'} mt-6`}>
                <h3 className={`text-lg font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                  🎯 Quick Stats
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Total Analyses</span>
                    <span className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>127</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Cost Saved (Month)</span>
                    <span className={`font-medium text-green-600`}>$1,245</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>Efficiency</span>
                    <span className={`font-medium text-blue-600`}>94.2%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Analytics Section */}
            <div className="lg:col-span-2">
              <AnalyticsDashboard 
                currentAnalysis={currentAnalysis} 
                historicalData={historicalData}
              />
            </div>
          </div>

          {/* Footer Info */}
          <div className={`${isDarkMode ? 'bg-gray-800' : 'bg-primary-50'} rounded-lg p-6 border ${isDarkMode ? 'border-gray-700' : 'border-primary-200'}`}>
            <div className="text-center">
              <h3 className={`text-lg font-semibold ${isDarkMode ? 'text-white' : 'text-primary-800'} mb-2`}>
                🇦🇪 Supporting UAE Vision 2071
              </h3>
              <p className={`${isDarkMode ? 'text-gray-300' : 'text-primary-600'} max-w-3xl mx-auto`}>
                Logixon Smart AquaVision contributes to the UAE's vision for food security and sustainability 
                through innovative AI technology, helping local aquaculture farms reduce costs while promoting 
                environmentally responsible practices.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;