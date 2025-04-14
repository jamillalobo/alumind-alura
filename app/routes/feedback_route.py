from flask import Blueprint, request, jsonify
from app.controller.feedback_controller import FeedbackController

feedbacks_bp = Blueprint('feedbacks', __name__)
controller = FeedbackController()

@feedbacks_bp.route('/feedbacks', methods=['POST'])
def classify_feedback():
    return controller.classify_feedback(request)
