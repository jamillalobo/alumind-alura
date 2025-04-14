from flask import Blueprint
from app.controller.report_controller import ReportController

report_bp = Blueprint('report', __name__)
controller = ReportController()

@report_bp.route('/report')
def get_report():
    return controller.get_report()

@report_bp.route('/feedback/<feedback_id>')
def get_feedback_detail(feedback_id):
    return controller.get_feedback_detail(feedback_id)
