import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

class Config:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        assert self.api_key, "Google API key is required"
        self.project_id = os.getenv("PROJECT_ID")
        assert self.project_id, "Project ID is required"
        self.gemini_model = os.getenv("GEMINI_MODEL")
        assert self.gemini_model, "Gemini model is required"
        self.location = "us-central1"

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        assert self.openai_api_key, "OpenAI API key is required"
        self.openai_model = os.getenv("OPENAI_MODEL")
        assert self.openai_model, "OpenAI model is required"

        self.llm_provider = os.getenv("LLM_PROVIDER")
        assert self.llm_provider in ["GEMINI", "OPENAI"], "LLM_PROVIDER must be either 'GEMINI' or 'OPENAI'"

    @property
    def gemini(self):
        if self.project_id:
            return ChatGoogleGenerativeAI(
                api_key=self.api_key,
                project_id=self.project_id,
                location=self.location,
                model=self.gemini_model,
                temperature=0.2,
            )
        
    @property
    def openai(self):
        return ChatOpenAI(model=self.openai_model, api_key=self.openai_api_key, temperature=0.2)    
    
    @property
    def llm(self):
        if self.llm_provider == "GEMINI":
            return self.gemini
        elif self.llm_provider == "OPENAI":
            return self.openai
        else:
            raise ValueError(f"LLM_PROVIDER inválido: {self.llm_provider}")
    
config = Config()

    

    