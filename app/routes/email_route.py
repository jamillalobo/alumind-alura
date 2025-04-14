from flask import Blueprint
from app.controller.email_controller import EmailController
from app.service.email_service import EmailService
from app.config import config 

email_bp = Blueprint('email', __name__)
controller = EmailController(EmailService(config.llm))  

@email_bp.route("/send_mail", methods=["POST"])
def send_email():
    return controller.send_email()