from typing import List
from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    id: str = Field(..., description="id of feedback")
    feedback: str = Field(..., description="feedback of user", serialization_alias='feedback_text')

class RequestFeatures(BaseModel):
    code: str = Field(description="code requested by user")
    reason: str = Field(description="reason requested by user")

class FeedbackResponse(BaseModel):
    id: str = Field(description="id of feedback")
    sentiment: str = Field(description="sentiment of user")
    requested_features: List[RequestFeatures] = Field(description="requested features of user")
