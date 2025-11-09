#!/bin/bash

# Logixon Smart AquaVision - Local Setup Script
# This script sets up the entire development environment

set -e

echo "🐟 Setting up Logixon Smart AquaVision..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        print_success "Docker is installed"
        return 0
    else
        print_error "Docker is not installed. Please install Docker first."
        return 1
    fi
}

# Check if Docker Compose is installed
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose is installed"
        return 0
    else
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        return 1
    fi
}

# Check if Node.js is installed
check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js is installed (${NODE_VERSION})"
        return 0
    else
        print_warning "Node.js is not installed. Docker will be used for frontend."
        return 1
    fi
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python is installed (${PYTHON_VERSION})"
        return 0
    else
        print_warning "Python is not installed. Docker will be used for backend."
        return 1
    fi
}

# Setup with Docker (recommended)
setup_with_docker() {
    print_status "Setting up with Docker..."
    
    # Build and start services
    print_status "Building Docker images..."
    docker-compose build
    
    print_status "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if curl -f http://localhost:8000/api/health &> /dev/null; then
        print_success "Backend is running at http://localhost:8000"
    else
        print_error "Backend failed to start"
        return 1
    fi
    
    if curl -f http://localhost:3000 &> /dev/null; then
        print_success "Frontend is running at http://localhost:3000"
    else
        print_error "Frontend failed to start"
        return 1
    fi
    
    print_success "🎉 Logixon Smart AquaVision is ready!"
    echo
    echo "Access the application:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo
    echo "To stop the application:"
    echo "  docker-compose down"
}

# Setup without Docker (manual)
setup_manual() {
    print_status "Setting up manually..."
    
    # Setup backend
    print_status "Setting up backend..."
    cd backend
    
    if command -v python3 &> /dev/null; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        
        print_status "Starting backend server in background..."
        nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
        BACKEND_PID=$!
        echo $BACKEND_PID > ../logs/backend.pid
    else
        print_error "Python 3 is required for manual setup"
        return 1
    fi
    
    cd ..
    
    # Setup frontend
    print_status "Setting up frontend..."
    cd frontend
    
    if command -v npm &> /dev/null; then
        npm install
        
        print_status "Starting frontend server in background..."
        nohup npm start > ../logs/frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > ../logs/frontend.pid
    else
        print_error "Node.js and npm are required for manual setup"
        return 1
    fi
    
    cd ..
    
    # Wait for services
    print_status "Waiting for services to start..."
    sleep 15
    
    print_success "🎉 Logixon Smart AquaVision is ready!"
    echo
    echo "Access the application:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo
    echo "To stop the application, run:"
    echo "  ./scripts/stop.sh"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p logs
    mkdir -p data
    mkdir -p uploads
    print_success "Directories created"
}

# Main setup function
main() {
    echo "🚀 Logixon Smart AquaVision Setup"
    echo "================================="
    echo
    
    # Create directories
    create_directories
    
    # Check requirements
    print_status "Checking requirements..."
    
    DOCKER_AVAILABLE=false
    NODE_AVAILABLE=false
    PYTHON_AVAILABLE=false
    
    if check_docker && check_docker_compose; then
        DOCKER_AVAILABLE=true
    fi
    
    if check_node; then
        NODE_AVAILABLE=true
    fi
    
    if check_python; then
        PYTHON_AVAILABLE=true
    fi
    
    echo
    
    # Choose setup method
    if [ "$DOCKER_AVAILABLE" = true ]; then
        print_status "Docker is available. Using Docker setup (recommended)..."
        setup_with_docker
    elif [ "$NODE_AVAILABLE" = true ] && [ "$PYTHON_AVAILABLE" = true ]; then
        print_status "Setting up manually..."
        setup_manual
    else
        print_error "Insufficient requirements for setup."
        echo "Please install either:"
        echo "  1. Docker and Docker Compose (recommended)"
        echo "  2. Node.js and Python 3"
        exit 1
    fi
}

# Run main function
main "$@"