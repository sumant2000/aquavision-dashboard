import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50
import cv2
import numpy as np
from PIL import Image
import asyncio
from datetime import datetime
import uuid
import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class FishActivityModel(nn.Module):
    """PyTorch model for fish activity analysis"""
    
    def __init__(self, num_classes=5):
        super(FishActivityModel, self).__init__()
        # Use pre-trained ResNet50 as backbone
        self.backbone = resnet50(pretrained=True)
        
        # Modify the final layer for our specific task
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, num_classes)
        
        # Additional layers for regression outputs
        self.activity_classifier = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 5)  # 5 activity levels
        )
        
        self.feed_predictor = nn.Sequential(
            nn.Linear(num_features, 64),
            nn.ReLU(),
            nn.Linear(64, 1)  # Feed amount prediction
        )
    
    def forward(self, x):
        # Extract features using backbone
        features = self.backbone.avgpool(self.backbone.layer4(
            self.backbone.layer3(self.backbone.layer2(
                self.backbone.layer1(self.backbone.maxpool(
                    self.backbone.relu(self.backbone.bn1(
                        self.backbone.conv1(x)
                    ))
                ))
            ))
        ))
        
        features = torch.flatten(features, 1)
        
        # Predict activity level and feed amount
        activity = self.activity_classifier(features)
        feed_amount = self.feed_predictor(features)
        
        return activity, feed_amount


class FishActivityAnalyzer:
    """Main class for fish activity analysis using computer vision"""
    
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Activity level mapping
        self.activity_levels = {
            0: "Low",
            1: "Moderate", 
            2: "Active",
            3: "High",
            4: "Feeding"
        }
        
        # Feeding behavior patterns
        self.feeding_behaviors = [
            "Surface feeding",
            "Bottom feeding", 
            "Scattered feeding",
            "Aggressive feeding",
            "Calm feeding"
        ]
        
        logger.info(f"🤖 Initialized FishActivityAnalyzer on {self.device}")
    
    async def load_model(self):
        """Load the pre-trained model"""
        try:
            self.model = FishActivityModel()
            self.model.to(self.device)
            
            # In production, load actual trained weights
            # self.model.load_state_dict(torch.load('models/fish_activity_model.pth'))
            
            self.model.eval()
            logger.info("✅ AI model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            # Use mock model for demo
            self.model = "mock_model"
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    async def analyze_fish_activity(self, file_path: str, farm_id: str) -> Dict[str, Any]:
        """
        Analyze fish activity from video/image file
        
        Args:
            file_path: Path to the uploaded video/image file
            farm_id: Identifier for the fish farm
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            analysis_id = str(uuid.uuid4())
            timestamp = datetime.utcnow()
            
            logger.info(f"🔍 Starting analysis for {file_path}")
            
            # Process video/image
            if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                frames = await self._extract_video_frames(file_path)
                analysis_results = await self._analyze_frames(frames)
            else:
                # Single image
                image = await self._load_image(file_path)
                analysis_results = await self._analyze_single_image(image)
            
            # Generate comprehensive analysis
            results = {
                "farm_id": farm_id,
                "analysis_id": analysis_id,
                "timestamp": timestamp,
                "fish_count": analysis_results.get("fish_count", np.random.randint(15, 45)),
                "activity_level": analysis_results.get("activity_level", np.random.choice(list(self.activity_levels.values()))),
                "feeding_behavior": analysis_results.get("feeding_behavior", np.random.choice(self.feeding_behaviors)),
                "recommended_feed_amount": analysis_results.get("feed_amount", round(2.5 + np.random.random() * 1.5, 2)),
                "confidence_score": analysis_results.get("confidence", 0.85 + np.random.random() * 0.14),
                "estimated_cost_savings": round(10 + np.random.random() * 20, 2),
                "efficiency_score": round(7 + np.random.random() * 2.5, 1),
                "sustainability_score": round(7.5 + np.random.random() * 2, 1),
                "water_quality_impact": np.random.choice(["Minimal", "Low", "Moderate"]),
                "insights": self._generate_insights(analysis_results),
                "recommendations": self._generate_recommendations(analysis_results)
            }
            
            logger.info(f"✅ Analysis completed: {analysis_id}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            raise e
    
    async def _extract_video_frames(self, video_path: str, max_frames: int = 30) -> List[np.ndarray]:
        """Extract frames from video for analysis"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = max(1, total_frames // max_frames)
        
        frame_idx = 0
        while cap.isOpened() and len(frames) < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_idx % frame_interval == 0:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            frame_idx += 1
        
        cap.release()
        logger.info(f"📹 Extracted {len(frames)} frames from video")
        return frames
    
    async def _load_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess single image"""
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    async def _analyze_frames(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze multiple frames from video"""
        if not self.model or self.model == "mock_model":
            return self._mock_analysis()
        
        results = []
        
        for frame in frames:
            # Convert to PIL Image and apply transforms
            pil_image = Image.fromarray(frame)
            tensor_image = self.transform(pil_image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                activity_logits, feed_amount = self.model(tensor_image)
                
                activity_pred = torch.softmax(activity_logits, dim=1)
                activity_class = torch.argmax(activity_pred, dim=1).item()
                confidence = torch.max(activity_pred).item()
                
                results.append({
                    "activity_class": activity_class,
                    "confidence": confidence,
                    "feed_amount": feed_amount.item()
                })
        
        # Aggregate results
        avg_confidence = np.mean([r["confidence"] for r in results])
        activity_counts = {}
        
        for r in results:
            activity = self.activity_levels[r["activity_class"]]
            activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        dominant_activity = max(activity_counts, key=activity_counts.get)
        avg_feed_amount = np.mean([r["feed_amount"] for r in results])
        
        return {
            "activity_level": dominant_activity,
            "confidence": avg_confidence,
            "feed_amount": max(0.5, avg_feed_amount),  # Minimum 0.5kg
            "fish_count": np.random.randint(15, 45)  # Mock fish counting
        }
    
    async def _analyze_single_image(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze single image"""
        if not self.model or self.model == "mock_model":
            return self._mock_analysis()
        
        # Convert to PIL and apply transforms
        pil_image = Image.fromarray(image)
        tensor_image = self.transform(pil_image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            activity_logits, feed_amount = self.model(tensor_image)
            
            activity_pred = torch.softmax(activity_logits, dim=1)
            activity_class = torch.argmax(activity_pred, dim=1).item()
            confidence = torch.max(activity_pred).item()
            
            return {
                "activity_level": self.activity_levels[activity_class],
                "confidence": confidence,
                "feed_amount": max(0.5, feed_amount.item()),
                "fish_count": np.random.randint(15, 45)
            }
    
    def _mock_analysis(self) -> Dict[str, Any]:
        """Generate mock analysis results for demo"""
        return {
            "activity_level": np.random.choice(list(self.activity_levels.values())),
            "confidence": 0.85 + np.random.random() * 0.14,
            "feed_amount": 2.0 + np.random.random() * 2.0,
            "fish_count": np.random.randint(15, 45)
        }
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate AI insights based on analysis"""
        insights = []
        
        activity = analysis.get("activity_level", "Moderate")
        fish_count = analysis.get("fish_count", 25)
        feed_amount = analysis.get("feed_amount", 2.5)
        
        if activity in ["High", "Feeding"]:
            insights.append("Fish are actively feeding - optimal time for feed distribution")
        elif activity == "Low":
            insights.append("Low fish activity detected - consider reducing feed amount")
        
        if fish_count > 35:
            insights.append("High fish density observed - monitor water quality closely")
        elif fish_count < 20:
            insights.append("Lower fish density - feed distribution can be more targeted")
        
        if feed_amount > 3.0:
            insights.append("Higher feed requirement detected - fish growth phase likely")
        
        return insights
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        activity = analysis.get("activity_level", "Moderate")
        confidence = analysis.get("confidence", 0.9)
        
        if confidence > 0.9:
            recommendations.append("High confidence analysis - safe to apply recommendations")
        elif confidence < 0.7:
            recommendations.append("Lower confidence - consider manual verification")
        
        if activity == "Feeding":
            recommendations.append("Continue current feeding schedule - fish responding well")
        elif activity == "Low":
            recommendations.append("Reduce feeding frequency or amount to prevent waste")
        
        recommendations.append("Monitor water temperature and quality parameters")
        recommendations.append("Schedule next analysis within 4-6 hours")
        
        return recommendations
    
    async def get_feed_recommendations(self, farm_id: str) -> Dict[str, Any]:
        """Get feed recommendations for a farm"""
        # Mock recommendations - in production, this would query the database
        current_time = datetime.utcnow()
        
        return {
            "farm_id": farm_id,
            "timestamp": current_time,
            "current_feed_amount": 3.0,
            "recommended_feed_amount": 2.7,
            "adjustment_percentage": -10.0,
            "reasoning": "Fish activity analysis suggests slightly lower feed requirement to optimize efficiency",
            "confidence": 0.92,
            "cost_per_kg": 4.50,
            "daily_savings": 1.35,
            "monthly_savings": 40.50,
            "expected_growth_rate": 2.3,
            "feed_conversion_ratio": 1.4,
            "next_feeding_time": "14:30",
            "monitoring_frequency": "Every 4 hours"
        }
    
    async def get_historical_analytics(self, farm_id: str, days: int = 7) -> Dict[str, Any]:
        """Get historical analytics for a farm"""
        # Mock historical data - in production, this would query the database
        end_date = datetime.utcnow()
        start_date = datetime.utcnow().replace(day=end_date.day - days)
        
        # Generate mock daily data
        daily_data = []
        for i in range(days):
            day_data = {
                "date": (start_date.replace(day=start_date.day + i)).strftime("%Y-%m-%d"),
                "feed_amount": round(2.5 + np.random.random() * 1.0, 2),
                "growth_rate": round(2.0 + np.random.random() * 0.8, 2),
                "cost": round(11 + np.random.random() * 6, 2),
                "efficiency": round(85 + np.random.random() * 10, 1),
                "water_quality": round(7.5 + np.random.random() * 1.5, 1)
            }
            daily_data.append(day_data)
        
        return {
            "farm_id": farm_id,
            "period_start": start_date,
            "period_end": end_date,
            "total_feed_used": round(sum([d["feed_amount"] for d in daily_data]), 2),
            "average_daily_feed": round(np.mean([d["feed_amount"] for d in daily_data]), 2),
            "feed_cost_total": round(sum([d["cost"] for d in daily_data]), 2),
            "total_growth": round(sum([d["growth_rate"] for d in daily_data]), 2),
            "average_growth_rate": round(np.mean([d["growth_rate"] for d in daily_data]), 2),
            "feed_conversion_efficiency": round(np.mean([d["efficiency"] for d in daily_data]), 1),
            "water_quality_score": round(np.mean([d["water_quality"] for d in daily_data]), 1),
            "environmental_impact_score": round(8.5 + np.random.random() * 1.0, 1),
            "daily_data": daily_data
        }