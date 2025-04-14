from app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.String, primary_key=True)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String, nullable=False)
    requested_features = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
