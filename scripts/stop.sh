#!/bin/bash

# Stop Logixon Smart AquaVision Services
# This script stops all running services

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Stop Docker services
stop_docker_services() {
    print_status "Stopping Docker services..."
    
    if command -v docker-compose &> /dev/null; then
        if [ -f "docker-compose.yml" ]; then
            docker-compose down
            print_success "Docker services stopped"
        else
            print_warning "docker-compose.yml not found"
        fi
    else
        print_warning "Docker Compose not available"
    fi
}

# Stop manual services
stop_manual_services() {
    print_status "Stopping manual services..."
    
    # Stop backend
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill $BACKEND_PID
            print_success "Backend stopped (PID: $BACKEND_PID)"
        else
            print_warning "Backend process not found"
        fi
        rm -f logs/backend.pid
    fi
    
    # Stop frontend
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill $FRONTEND_PID
            print_success "Frontend stopped (PID: $FRONTEND_PID)"
        else
            print_warning "Frontend process not found"
        fi
        rm -f logs/frontend.pid
    fi
    
    # Kill any remaining processes on ports 3000 and 8000
    print_status "Checking for processes on ports 3000 and 8000..."
    
    PORT_3000_PID=$(lsof -t -i:3000 2>/dev/null || echo "")
    if [ ! -z "$PORT_3000_PID" ]; then
        kill $PORT_3000_PID
        print_success "Killed process on port 3000 (PID: $PORT_3000_PID)"
    fi
    
    PORT_8000_PID=$(lsof -t -i:8000 2>/dev/null || echo "")
    if [ ! -z "$PORT_8000_PID" ]; then
        kill $PORT_8000_PID
        print_success "Killed process on port 8000 (PID: $PORT_8000_PID)"
    fi
}

# Clean up temporary files
cleanup_temp_files() {
    print_status "Cleaning up temporary files..."
    
    # Clean upload directory
    if [ -d "uploads" ]; then
        rm -rf uploads/*
        print_success "Cleaned uploads directory"
    fi
    
    # Clean log files
    if [ -d "logs" ]; then
        rm -f logs/*.log
        print_success "Cleaned log files"
    fi
}

# Main function
main() {
    echo "🛑 Stopping Logixon Smart AquaVision"
    echo "===================================="
    echo
    
    stop_docker_services
    stop_manual_services
    cleanup_temp_files
    
    print_success "🎉 All services stopped successfully!"
    echo
    echo "To start the application again, run:"
    echo "  ./scripts/setup.sh"
}

# Run main function
main "$@"