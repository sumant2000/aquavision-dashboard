import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

interface AnalysisResult {
  feedAmount: number;
  confidence: number;
  costSavings: number;
  sustainabilityScore: number;
  fishActivity: string;
  timestamp: string;
}

interface AnalyticsDashboardProps {
  currentAnalysis: AnalysisResult | null;
  historicalData: any[];
}

const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({ currentAnalysis, historicalData }) => {
  // Sample data for charts
  const feedingData = [
    { time: '6:00', recommended: 2.5, actual: 3.0, cost: 12 },
    { time: '12:00', recommended: 3.2, actual: 3.5, cost: 14 },
    { time: '18:00', recommended: 2.8, actual: 2.8, cost: 11 },
  ];

  const weeklyData = [
    { day: 'Mon', feed: 8.5, growth: 2.1, cost: 34 },
    { day: 'Tue', feed: 9.2, growth: 2.3, cost: 37 },
    { day: 'Wed', feed: 8.8, growth: 2.2, cost: 35 },
    { day: 'Thu', feed: 9.0, growth: 2.4, cost: 36 },
    { day: 'Fri', feed: 8.7, growth: 2.2, cost: 35 },
    { day: 'Sat', feed: 9.1, growth: 2.3, cost: 36 },
    { day: 'Sun', feed: 8.9, growth: 2.2, cost: 36 },
  ];

  const sustainabilityData = [
    { name: 'Optimal', value: 65, color: '#10b981' },
    { name: 'Efficient', value: 25, color: '#f59e0b' },
    { name: 'Wastage', value: 10, color: '#ef4444' },
  ];

  return (
    <div className="space-y-6">
      {/* Current Analysis Cards */}
      {currentAnalysis && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-primary-100 text-sm">Feed Recommendation</p>
                <p className="text-2xl font-bold">{currentAnalysis.feedAmount} kg</p>
              </div>
              <div className="text-3xl">🍽️</div>
            </div>
          </div>

          <div className="card bg-gradient-to-r from-green-500 to-green-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100 text-sm">Confidence Score</p>
                <p className="text-2xl font-bold">{Math.round(currentAnalysis.confidence * 100)}%</p>
              </div>
              <div className="text-3xl">🎯</div>
            </div>
          </div>

          <div className="card bg-gradient-to-r from-yellow-500 to-orange-500 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-yellow-100 text-sm">Cost Savings</p>
                <p className="text-2xl font-bold">${currentAnalysis.costSavings}</p>
              </div>
              <div className="text-3xl">💰</div>
            </div>
          </div>

          <div className="card bg-gradient-to-r from-aqua-500 to-aqua-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-aqua-100 text-sm">Sustainability</p>
                <p className="text-2xl font-bold">{currentAnalysis.sustainabilityScore}/10</p>
              </div>
              <div className="text-3xl">🌱</div>
            </div>
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Feeding Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">📊 Daily Feeding Analysis</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={feedingData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="recommended" fill="#0ea5e9" name="Recommended (kg)" />
              <Bar dataKey="actual" fill="#10b981" name="Actual (kg)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Weekly Trends */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">📈 Weekly Growth Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="growth" stroke="#10b981" strokeWidth={2} name="Growth (cm)" />
              <Line type="monotone" dataKey="feed" stroke="#0ea5e9" strokeWidth={2} name="Feed (kg)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Sustainability Pie Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">🌱 Feed Efficiency Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sustainabilityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {sustainabilityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Cost Analysis */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">💰 Cost vs Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="cost" fill="#f59e0b" name="Daily Cost ($)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Fish Activity Status */}
      {currentAnalysis && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">🐟 Fish Activity Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h4 className="font-medium text-blue-800">Current Activity</h4>
              <p className="text-2xl font-bold text-blue-600">{currentAnalysis.fishActivity}</p>
              <p className="text-sm text-blue-600">Based on movement patterns</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h4 className="font-medium text-green-800">Feeding Status</h4>
              <p className="text-2xl font-bold text-green-600">Optimal</p>
              <p className="text-sm text-green-600">Fish are actively feeding</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <h4 className="font-medium text-purple-800">Water Quality</h4>
              <p className="text-2xl font-bold text-purple-600">Excellent</p>
              <p className="text-sm text-purple-600">No pollution detected</p>
            </div>
          </div>
        </div>
      )}

      {/* AI Insights */}
      <div className="card bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200">
        <h3 className="text-lg font-semibold mb-4 text-indigo-800">🤖 AI Insights & Recommendations</h3>
        <div className="space-y-3">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-green-500 rounded-full mt-2"></div>
            <p className="text-gray-700">
              <strong>Optimal Feeding Window:</strong> Fish activity is highest between 7-9 AM and 5-7 PM. 
              Consider adjusting feeding schedule for better efficiency.
            </p>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
            <p className="text-gray-700">
              <strong>Cost Optimization:</strong> Reducing feed by 8% during low-activity periods could save $156/month 
              without affecting growth rates.
            </p>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
            <p className="text-gray-700">
              <strong>Sustainability Alert:</strong> Current feeding efficiency is 89%. 
              Implementing AI recommendations could improve this to 94%.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;