from flask import current_app
from app.config import config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
import json
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.language_models.chat_models import BaseChatModel
import os
from langchain_core.messages import AIMessage

PROMPT_EMAIL = """
Seu trabalho é enviar e-mails personalizados com um breve resumo (até 200 palavras) dos principais feedbacks da semana para um cliente.

- Todos os feedbacks da semana: {feedbacks}
- % Feedbacks Positivos: {percent_positive}%
- % Feedbacks Negativos: {percent_negative}%
- Funcionalidades mais pedidas: {top_features}

Com esses dados, crie um email amigável, não precisa adicionar o assunto do email, nem mencionar o nome do cliente. Destaque pontos principais gerais dos feedbacks, mostrando as funcionalidades mais pedidas e agradeça no final.
"""

def send_email_chain(chat_model: BaseChatModel):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de IA que envia e-mails em nome da empresa Alumind."),
        ("user", PROMPT_EMAIL),
    ])

    return prompt_template

class EmailService:
    load_dotenv()

    def __init__(self, model: BaseChatModel):
        self.chat_model = model
        self.prompt_template = send_email_chain(self.chat_model)
    
    def generate_email_text(self, feedbacks, positive_percentage, negative_percentage, top_features):
        formatted_features = "\n".join(
            [f"- {feature[0]}: {feature[1]} pedidos" for feature in top_features]
        )

        prompt_values = {
            "feedbacks": feedbacks,
            "percent_positive": positive_percentage,
            "percent_negative": negative_percentage,
            "top_features": formatted_features
        }

        full_prompt = self.prompt_template.format_messages(**prompt_values)

        response = self.chat_model.invoke(full_prompt)

        if isinstance(response, AIMessage):
            return response.content.strip()
        
        return "Erro ao gerar o email."
    
    def send_email(self, subject, recipients, body):
        sender_email = os.getenv("GMAIL_SENDER")  
        sender_password = os.getenv("GMAIL_SENDER_PASSWORD")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", _charset="utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_bytes())

        print("Email enviado com sucesso!")