#!/bin/bash
# Build script for deployment

echo "🚀 Building Logixon Smart AquaVision for deployment..."

# Backend setup
echo "📦 Setting up backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Frontend setup  
echo "🎨 Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build completed successfully!"
echo "📂 Frontend build output: ./frontend/build"
echo "🔧 Backend ready at: ./backend/app/main.py"