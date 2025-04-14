from app.service.email_service import EmailService
from app.service.weekly_summary_service import WeeklySummaryService
from langchain_core.language_models.chat_models import BaseChatModel
import os
from dotenv import load_dotenv

class EmailController:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.weekly_summary_service = WeeklySummaryService()

    def send_email(self):
        load_dotenv()
        summary = self.weekly_summary_service.generate_summary()

        email_text = self.email_service.generate_email_text(
            feedbacks=summary["feedbacks"],
            positive_percentage=summary["positive_percentage"],
            negative_percentage=summary["negative_percentage"],
            top_features=summary["top_features"]
        )

        recipients = ["email-receiver@gmail.com"]  
        subject = "Resumo Semanal de Feedbacks - AluMind"
        self.email_service.send_email(subject, recipients, email_text)

        return {"message": "Email enviado com sucesso!"}, 200
