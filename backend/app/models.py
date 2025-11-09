from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from .database import Base
from datetime import datetime


class Farm(Base):
    """Farm model for storing farm information"""
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    contact_email = Column(String(100), nullable=True)
    
    # Farm specifications
    pond_count = Column(Integer, default=1)
    total_capacity = Column(Float, nullable=True)  # cubic meters
    fish_species = Column(JSON, nullable=True)  # List of species
    
    # Status and timestamps
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Analysis(Base):
    """Analysis model for storing video analysis results"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String(50), unique=True, index=True, nullable=False)
    farm_id = Column(String(50), index=True, nullable=False)
    
    # File information
    filename = Column(String(200), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(50), nullable=False)
    
    # Analysis results
    fish_count = Column(Integer, nullable=False)
    activity_level = Column(String(20), nullable=False)
    feeding_behavior = Column(String(50), nullable=False)
    
    # Feed recommendations
    recommended_feed_amount = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    
    # Economic metrics
    estimated_cost_savings = Column(Float, nullable=False)
    efficiency_score = Column(Float, nullable=False)
    
    # Environmental metrics
    sustainability_score = Column(Float, nullable=False)
    water_quality_impact = Column(String(50), nullable=False)
    
    # Additional data
    insights = Column(JSON, nullable=True)  # List of insights
    recommendations = Column(JSON, nullable=True)  # List of recommendations
    raw_analysis_data = Column(JSON, nullable=True)  # Raw ML output
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class FeedRecommendationRecord(Base):
    """Feed recommendation model for storing feed recommendations"""
    __tablename__ = "feed_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String(50), index=True, nullable=False)
    analysis_id = Column(String(50), index=True, nullable=True)
    
    # Feed amounts
    current_feed_amount = Column(Float, nullable=False)
    recommended_feed_amount = Column(Float, nullable=False)
    adjustment_percentage = Column(Float, nullable=False)
    
    # Recommendation details
    reasoning = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Economic data
    cost_per_kg = Column(Float, default=4.50)
    daily_savings = Column(Float, nullable=False)
    monthly_savings = Column(Float, nullable=False)
    
    # Performance metrics
    expected_growth_rate = Column(Float, nullable=False)
    feed_conversion_ratio = Column(Float, nullable=False)
    
    # Next actions
    next_feeding_time = Column(String(20), nullable=False)
    monitoring_frequency = Column(String(50), nullable=False)
    
    # Status
    status = Column(String(20), default="pending")  # pending, applied, ignored
    applied_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class HistoricalMetrics(Base):
    """Historical metrics model for storing daily farm performance data"""
    __tablename__ = "historical_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String(50), index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    
    # Daily feed data
    total_feed_used = Column(Float, nullable=False)
    number_of_feedings = Column(Integer, default=0)
    avg_feed_per_feeding = Column(Float, nullable=True)
    
    # Performance metrics
    fish_growth = Column(Float, nullable=True)  # daily growth in cm
    water_temperature = Column(Float, nullable=True)
    water_quality_score = Column(Float, nullable=True)
    
    # Economic data
    daily_feed_cost = Column(Float, nullable=False)
    estimated_savings = Column(Float, default=0.0)
    
    # Environmental metrics
    environmental_impact_score = Column(Float, nullable=True)
    feed_efficiency = Column(Float, nullable=True)
    
    # Additional data
    weather_conditions = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemLog(Base):
    """System log model for storing application logs"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(10), nullable=False)  # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    module = Column(String(50), nullable=True)
    farm_id = Column(String(50), nullable=True)
    analysis_id = Column(String(50), nullable=True)
    
    # Additional context
    context_data = Column(JSON, nullable=True)
    user_agent = Column(String(200), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)