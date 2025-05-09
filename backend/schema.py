from pydantic import BaseModel
from typing import List, Optional
import datetime

class FileSchema(BaseModel):
    id: str
    file_path: str
    status: str
    upload_time: datetime.datetime
    error: Optional[str] = None

class KeyPointSchema(BaseModel):
    text: str
    cluster_id: int
    embedding: List[float]

class TranscriptionSchema(BaseModel):
    id: str
    file_id: str
    text: str
    key_points: List[KeyPointSchema]
    timestamp: datetime.datetime

class BRDSchema(BaseModel):
    id: str
    transcription_id: str
    selected_key_points: List[str]
    content: str
    pdf_path: str
    embedding: List[float]

class TicketSchema(BaseModel):
    id: str
    brd_id: str
    title: str
    description: str
    type: str
    status: str

class FeedbackSchema(BaseModel):
    id: str
    brd_id: str
    rating: int
    comments: str
    timestamp: datetime.datetime

class CreateBRDRequest(BaseModel):
    file_id: str
    selected_key_points: List[str]

class CreateTicketRequest(BaseModel):
    brd_id: str
    title: str
    description: str
    type: str

class SimilarBRDsRequest(BaseModel):
    selected_key_points: List[str]

class FeedbackRequest(BaseModel):
    brd_id: str
    rating: int
    comments: str