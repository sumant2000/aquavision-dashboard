# Logixon Smart AquaVision Backend

FastAPI backend for AI-powered fish feed optimization.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/analyze` - Analyze video/image
- `GET /api/recommendations/{farm_id}` - Get recommendations
- `GET /api/analytics/{farm_id}` - Get analytics
- `GET /docs` - Interactive API documentation

## Environment Variables

- `DATABASE_URL` - Database connection string
- `MAX_FILE_SIZE` - Maximum upload file size
- `UPLOAD_DIR` - Upload directory path