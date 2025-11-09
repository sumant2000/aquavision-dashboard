from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="API status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    database_connected: bool = Field(..., description="Database connection status")
    ai_model_loaded: bool = Field(..., description="AI model loading status")


class AnalysisResponse(BaseModel):
    """Fish activity analysis response"""
    farm_id: str = Field(..., description="Farm identifier")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    
    # Fish activity metrics
    fish_count: int = Field(..., description="Detected fish count")
    activity_level: str = Field(..., description="Fish activity level", example="High")
    feeding_behavior: str = Field(..., description="Observed feeding behavior")
    
    # Feed recommendations
    recommended_feed_amount: float = Field(..., description="Recommended feed amount in kg")
    confidence_score: float = Field(..., description="Model confidence (0-1)")
    
    # Economic metrics
    estimated_cost_savings: float = Field(..., description="Estimated cost savings in USD")
    efficiency_score: float = Field(..., description="Feeding efficiency score (0-10)")
    
    # Environmental metrics
    sustainability_score: float = Field(..., description="Sustainability score (0-10)")
    water_quality_impact: str = Field(..., description="Predicted water quality impact")
    
    # Additional insights
    insights: List[str] = Field(default=[], description="AI-generated insights")
    recommendations: List[str] = Field(default=[], description="Actionable recommendations")


class FeedRecommendation(BaseModel):
    """Feed recommendation response"""
    farm_id: str = Field(..., description="Farm identifier")
    timestamp: datetime = Field(..., description="Recommendation timestamp")
    
    current_feed_amount: float = Field(..., description="Current feed amount in kg")
    recommended_feed_amount: float = Field(..., description="Recommended feed amount in kg")
    adjustment_percentage: float = Field(..., description="Recommended adjustment percentage")
    
    reasoning: str = Field(..., description="Explanation for recommendation")
    confidence: float = Field(..., description="Recommendation confidence (0-1)")
    
    # Economic impact
    cost_per_kg: float = Field(default=4.50, description="Feed cost per kg in USD")
    daily_savings: float = Field(..., description="Estimated daily savings in USD")
    monthly_savings: float = Field(..., description="Estimated monthly savings in USD")
    
    # Performance metrics
    expected_growth_rate: float = Field(..., description="Expected growth rate improvement")
    feed_conversion_ratio: float = Field(..., description="Feed conversion ratio")
    
    # Next actions
    next_feeding_time: str = Field(..., description="Recommended next feeding time")
    monitoring_frequency: str = Field(..., description="Recommended monitoring frequency")


class FarmInfo(BaseModel):
    """Farm information model"""
    farm_id: str = Field(..., description="Unique farm identifier")
    name: str = Field(..., description="Farm name")
    location: str = Field(..., description="Farm location")
    contact_email: str = Field(..., description="Contact email")
    
    # Farm specifications
    pond_count: int = Field(..., description="Number of ponds")
    total_capacity: float = Field(..., description="Total capacity in cubic meters")
    fish_species: List[str] = Field(..., description="Fish species being farmed")
    
    # Current status
    status: str = Field(..., description="Farm operational status")
    last_analysis: Optional[datetime] = Field(None, description="Last analysis timestamp")
    total_analyses: int = Field(default=0, description="Total number of analyses")


class HistoricalData(BaseModel):
    """Historical analytics data"""
    farm_id: str = Field(..., description="Farm identifier")
    period_start: datetime = Field(..., description="Period start date")
    period_end: datetime = Field(..., description="Period end date")
    
    # Feed data
    total_feed_used: float = Field(..., description="Total feed used in kg")
    average_daily_feed: float = Field(..., description="Average daily feed in kg")
    feed_cost_total: float = Field(..., description="Total feed cost in USD")
    
    # Performance metrics
    total_growth: float = Field(..., description="Total fish growth in cm")
    average_growth_rate: float = Field(..., description="Average growth rate")
    feed_conversion_efficiency: float = Field(..., description="Feed conversion efficiency")
    
    # Sustainability metrics
    water_quality_score: float = Field(..., description="Average water quality score")
    environmental_impact_score: float = Field(..., description="Environmental impact score")
    
    # Daily breakdowns
    daily_data: List[Dict[str, Any]] = Field(default=[], description="Daily breakdown data")


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error detail message")
    timestamp: datetime = Field(..., description="Error timestamp")
    error_code: Optional[str] = Field(None, description="Error code")


class UploadResponse(BaseModel):
    """File upload response"""
    success: bool = Field(..., description="Upload success status")
    file_id: str = Field(..., description="Uploaded file identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="File content type")
    upload_timestamp: datetime = Field(..., description="Upload timestamp")