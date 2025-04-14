from flask import render_template, request
from app.extensions import db
from app.model.feedback_db import Feedback
from collections import Counter

class ReportController:
    def get_report(self):
        feedbacks = Feedback.query.all()

        total_feedbacks = len(feedbacks)
        positive_feedbacks = len([f for f in feedbacks if f.sentiment == "POSITIVO"])
        positive_percentage = (positive_feedbacks / total_feedbacks * 100) if total_feedbacks > 0 else 0

        all_features = []
        for f in feedbacks:
            if f.requested_features:
                all_features.extend([feature['code'] for feature in f.requested_features])

        feature_counter = Counter(all_features)
        top_features = feature_counter.most_common(5)

        return render_template('report.html', positive_percentage=round(positive_percentage, 2), top_features=top_features, feedbacks=feedbacks)

    def get_feedback_detail(self, feedback_id):
        feedback = Feedback.query.get_or_404(feedback_id)
        return render_template('feedback_details.html', feedback=feedback)
