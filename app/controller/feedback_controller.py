from flask import jsonify
from app.config import config
from app.extensions import db
from app.model.feedback import FeedbackRequest
from app.model.feedback_db import Feedback
from app.service.feedback_service import FeedbackAnalyzer
from pydantic import ValidationError
import json

class FeedbackController:
    def __init__(self):
        self.analyzer = FeedbackAnalyzer(config.llm) 

    def classify_feedback(self, request):
        try:
            data = request.get_json()

            feedback_request = FeedbackRequest(**data)

            print(f"Analisando feedback: {feedback_request.feedback}")
            analysis = self.analyzer.analyze_feedback(feedback_request.feedback)

            if not isinstance(analysis, dict):
                try:
                    analysis = json.loads(analysis)
                except json.JSONDecodeError:
                    return jsonify({"error": "Resposta da LLM inválida."}), 500

            sentiment = analysis.get("sentiment")
            requested_features = analysis.get("requested_features", [])

            if sentiment not in ["POSITIVO", "NEGATIVO", "INCONCLUSIVO"]:
                return jsonify({"error": "Sentimento inválido retornado pela IA."}), 500

            feedback_entry = Feedback(
                id=feedback_request.id,
                feedback_text=feedback_request.feedback,
                sentiment=sentiment,
                requested_features=requested_features
            )
            db.session.add(feedback_entry)
            db.session.commit()

            return jsonify({
                "id": feedback_request.id,
                "sentiment": sentiment,
                "requested_features": requested_features
            })

        except ValidationError as e:
            return jsonify({"error": "Dados inválidos", "details": e.errors()}), 400

        except Exception as e:
            return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500
