# Logixon Smart AquaVision - Testing Guide

## Running Tests

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Run integration tests
./scripts/test-integration.sh

# Stop services
docker-compose down
```

## Test Coverage

- Backend: Aim for >90% code coverage
- Frontend: Test components and utilities
- Integration: Test API endpoints end-to-end

## Test Data

Sample test videos and images are provided in the `test-data/` directory.