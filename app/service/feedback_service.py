from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.model.feedback import FeedbackRequest, FeedbackResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
import json
import re
from app.config import config
from langchain_core.output_parsers import PydanticOutputParser


PROMPT_INSTRUCTION = """
    Com base em um texto de feedback de um cliente que você irá receber, classifique o sentimento desse cliente como: POSITIVO, NEGATIVO, ou INCONCLUSIVO.
    Depois, para cada feedback, extraia uma lista de possíveis funcionalidades sugeridas. Cada funcionalidade sugerida tem um código em capslock que a identifica unicamente 
    e uma descrição breve do porquê a funcionalidade é importante.
    
    Raciocine sobre a justificativa da sua resposta, explicando por que você fez as escolhas que realmente fez.
    Pense nas etapas passo a passo.    

    O feedback do cliente é o seguinte: {feedback}
    
        Retorne apenas o JSON, nada além do JSON:
    {{
        "id": "",
        "sentiment": "",
        "requested_features": [
            {{"code": "", "reason": ""}}
        ]
    }}
    """

def analyze_sentiment(chat_model: BaseChatModel, feedback: str):
    prompt = PROMPT_INSTRUCTION.format(feedback=feedback)
    response = chat_model.invoke(prompt)
        
    if isinstance(response, AIMessage):
        response_content = response.content.strip()

        if response_content.startswith("```json") and response_content.endswith("```"):
            response_content = response_content[7:-3].strip()
        elif response_content.startswith("```") and response_content.endswith("```"):
            response_content = response_content[3:-3].strip()

        try:
            match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if match:
                json_only = match.group()
                analysis_dict = json.loads(json_only)
                return analysis_dict
            else:
                print(f"Nenhum JSON encontrado na resposta: {response_content}")
                return {"error": "Nenhum JSON encontrado na resposta da LLM"}, 500
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON da LLM: {e}, Conteúdo: {response_content}")
            return {"error": f"Resposta da LLM em formato JSON inválido: {e}"}, 500
    else:
        return {"error": "Resposta inesperada da LLM"}, 500

class FeedbackAnalyzer:
    def __init__(self, model: BaseChatModel):
        self.model = model

    def analyze_feedback(self, feedback: str):
        return analyze_sentiment(self.model, feedback)


