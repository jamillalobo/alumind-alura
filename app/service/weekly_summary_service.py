from app.extensions import db
from app.model.feedback_db import Feedback
from datetime import datetime, timedelta
from collections import Counter
from app.config import config

class WeeklySummaryService:
    def __init__(self):
        self.llm = config.gemini

    def get_weekly_feedbacks(self):
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        return Feedback.query.filter(Feedback.created_at >= week_ago).all()
    
    def percentage_positive_feedbacks(self, feedbacks):
        total_feedbacks = len(feedbacks)
        positive_feedbacks = len([f for f in feedbacks if f.sentiment == "POSITIVO"])
        return (positive_feedbacks / total_feedbacks * 100) if total_feedbacks > 0 else 0
    
    def percentage_negative_feedbacks(self, feedbacks):
        total_feedbacks = len(feedbacks)
        negative_feedbacks = len([f for f in feedbacks if f.sentiment == "NEGATIVO"])
        return (negative_feedbacks / total_feedbacks * 100) if total_feedbacks > 0 else 0
    
    def get_top_requested_features(self, feedbacks):
        all_features = []
        for f in feedbacks:
            if f.requested_features:
                all_features.extend([feature['code'] for feature in f.requested_features])
        
        feature_counter = Counter(all_features)
        return feature_counter.most_common(5)
    
    def generate_summary(self):
        feedbacks = self.get_weekly_feedbacks()
        positive_percentage = self.percentage_positive_feedbacks(feedbacks)
        negative_percentage = self.percentage_negative_feedbacks(feedbacks)
        top_features = self.get_top_requested_features(feedbacks)

        summary = {
            "feedbacks": feedbacks,
            "positive_percentage": round(positive_percentage, 2),
            "negative_percentage": round(negative_percentage, 2),
            "top_features": top_features
        }

        return summary
