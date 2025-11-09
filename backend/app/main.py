from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
import logging

from .database import engine, SessionLocal, get_db
from .models import Base
from .schemas import AnalysisResponse, FeedRecommendation, HealthCheck
from .ai_model import FishActivityAnalyzer
from .utils import save_upload_file, cleanup_temp_files

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Logixon Smart AquaVision API",
    description="AI-Powered Fish Feed Optimization API for UAE Aquaculture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",  # Replace with actual domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI model
ai_analyzer = FishActivityAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🐟 Logixon Smart AquaVision API Starting...")
    logger.info("🤖 Loading AI models...")
    await ai_analyzer.load_model()
    logger.info("✅ API Ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🔄 Cleaning up temporary files...")
    cleanup_temp_files()
    logger.info("👋 API Shutdown Complete")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🐟 Welcome to Logixon Smart AquaVision API",
        "description": "AI-Powered Fish Feed Optimization for UAE Aquaculture",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        database_connected=True,
        ai_model_loaded=ai_analyzer.is_loaded()
    )

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_video(
    file: UploadFile = File(...),
    farm_id: Optional[str] = "UAE_Farm_001",
    db: Session = Depends(get_db)
):
    """
    Analyze uploaded video/image for fish activity and generate feed recommendations
    
    - **file**: Video or image file (MP4, AVI, MOV, JPG, PNG)
    - **farm_id**: Unique identifier for the fish farm
    - **returns**: Analysis results with feed recommendations
    """
    try:
        # Validate file type
        allowed_types = ["video/mp4", "video/avi", "video/mov", "image/jpeg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Supported: MP4, AVI, MOV, JPG, PNG"
            )
        
        # Validate file size (max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size: 100MB"
            )
        
        # Save uploaded file temporarily
        temp_file_path = await save_upload_file(file, content)
        
        # Run AI analysis
        analysis_result = await ai_analyzer.analyze_fish_activity(
            file_path=temp_file_path,
            farm_id=farm_id
        )
        
        # Save results to database
        # (Database operations would be implemented here)
        
        logger.info(f"✅ Analysis completed for farm {farm_id}")
        
        return AnalysisResponse(**analysis_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/recommendations/{farm_id}", response_model=FeedRecommendation)
async def get_recommendations(
    farm_id: str,
    db: Session = Depends(get_db)
):
    """
    Get latest feed recommendations for a specific farm
    
    - **farm_id**: Unique identifier for the fish farm
    - **returns**: Current feed recommendations and insights
    """
    try:
        # Generate recommendations based on latest analysis
        recommendations = await ai_analyzer.get_feed_recommendations(farm_id)
        
        logger.info(f"📊 Generated recommendations for farm {farm_id}")
        
        return FeedRecommendation(**recommendations)
        
    except Exception as e:
        logger.error(f"❌ Failed to get recommendations: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@app.get("/api/analytics/{farm_id}")
async def get_analytics(
    farm_id: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get historical analytics and trends for a farm
    
    - **farm_id**: Unique identifier for the fish farm
    - **days**: Number of days to include in analytics (default: 7)
    - **returns**: Historical data and trends
    """
    try:
        analytics_data = await ai_analyzer.get_historical_analytics(farm_id, days)
        
        logger.info(f"📈 Generated analytics for farm {farm_id} ({days} days)")
        
        return analytics_data
        
    except Exception as e:
        logger.error(f"❌ Failed to get analytics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get analytics: {str(e)}"
        )

@app.get("/api/farms")
async def list_farms(db: Session = Depends(get_db)):
    """Get list of all registered fish farms"""
    try:
        # Mock data for demo
        farms = [
            {
                "farm_id": "UAE_Farm_001",
                "name": "Dubai Aquaculture Center",
                "location": "Dubai, UAE",
                "status": "active",
                "last_analysis": "2024-11-06T10:30:00Z"
            },
            {
                "farm_id": "UAE_Farm_002", 
                "name": "Abu Dhabi Marine Farm",
                "location": "Abu Dhabi, UAE",
                "status": "active",
                "last_analysis": "2024-11-06T09:15:00Z"
            }
        ]
        
        return {"farms": farms, "total": len(farms)}
        
    except Exception as e:
        logger.error(f"❌ Failed to list farms: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve farms")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )