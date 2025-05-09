import shutil
import logging
import asyncio
import datetime
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import PyPDF2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import traceback
from bson import ObjectId
import json

# Import agents
from agents.audio_to_text import AudioToTextAgent
from agents.key_point_extraction import KeyPointExtractionAgent
from agents.knowledge_base import KnowledgeBaseAgent
from agents.brd_author import BRDAuthorAgent
from agents.task_management import TaskManagementAgent
from agents.quality_check import QualityCheckAgent
from agents.communication import CommunicationAgent
from agents.feedback import FeedbackAgent

# Import schema
from schema import CreateBRDRequest, CreateTicketRequest, SimilarBRDsRequest, FeedbackRequest

from dotenv import load_dotenv

# Centralized logging setup
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/brds", exist_ok=True)

# In-memory queue for agent coordination
task_queue = asyncio.Queue()

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)

def mongo_serializer(obj):
    """Custom serializer for MongoDB objects"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj

class ReasoningPlanningAgent:
    def __init__(self):
        self.audio_agent = AudioToTextAgent()
        self.keypoint_agent = KeyPointExtractionAgent()
        self.kb_agent = KnowledgeBaseAgent()
        self.brd_agent = BRDAuthorAgent()
        self.task_agent = TaskManagementAgent()
        self.quality_agent = QualityCheckAgent()
        self.comm_agent = CommunicationAgent()
        self.feedback_agent = FeedbackAgent()
        self.logger = logging.getLogger(__name__)

    async def process_file(self, file_id, file_path, content_type):
        try:
            self.logger.info(f"Processing file {file_id}")
            self.kb_agent.update_file(file_id, {"status": "transcribing"})
            if content_type.startswith("video/") or content_type.startswith("audio/"):
                transcription = await self.audio_agent.transcribe(file_path)
            elif content_type == "application/pdf":
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    transcription = " ".join(page.extract_text() for page in reader.pages)
            else:
                raise ValueError("Unsupported file type")
            if not transcription:
                raise Exception("Transcription failed")
            transcription_id = str(datetime.datetime.now().timestamp())
            key_points = self.keypoint_agent.extract_key_points(transcription)
            transcription_data = {
                "id": transcription_id,
                "file_id": file_id,
                "text": transcription,
                "key_points": key_points,
                "timestamp": datetime.datetime.now()
            }
            self.kb_agent.store_transcription(transcription_data)
            self.kb_agent.update_file(file_id, {"status": "done"})
            await self.comm_agent.send_email("Transcription Completed", f"File {file_id} processed.")
            self.logger.info(f"File {file_id} processed successfully")
        except Exception as e:
            self.logger.error(f"File {file_id} processing failed: {str(e)}")
            self.kb_agent.update_file(file_id, {"status": "error", "error": str(e)})
            await self.comm_agent.send_email("Processing Failed", f"File {file_id} failed: {str(e)}")

    async def suggest_brd(self, key_points):
        embeddings = [kp["embedding"] for kp in key_points]
        avg_embedding = np.mean(embeddings, axis=0)
        brds = list(self.kb_agent.brds_col.find())
        for brd in brds:
            brd_embedding = np.mean([self.keypoint_agent.sentence_model.encode(p) for p in brd["selected_key_points"]], axis=0)
            similarity = cosine_similarity([avg_embedding], [brd_embedding])[0][0]
            if similarity > 0.85:
                self.logger.info(f"Suggested BRD {brd['id']} with similarity {similarity}")
                return True, brd["id"]
        return False, None

# Initialize the reasoning agent
reasoning_agent = ReasoningPlanningAgent()

@app.post("/api/agents/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.size > 100 * 1024 * 1024:
        logger.error("File size exceeds 100MB")
        return {"error": "File size exceeds 100MB"}
    file_path = f"data/uploads/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    file_id = str(datetime.datetime.now().timestamp())
    file_data = {
        "id": file_id,
        "file_path": file_path,
        "status": "uploading",
        "upload_time": datetime.datetime.now(),
        "error": None
    }
    reasoning_agent.kb_agent.store_file(file_data)
    background_tasks.add_task(reasoning_agent.process_file, file_id, file_path, file.content_type)
    logger.info(f"File {file_id} uploaded")
    return {"file_id": file_id}

@app.get("/api/agents/files/{file_id}")
def get_file(file_id: str):
    try:
        file_data = reasoning_agent.kb_agent.get_file(file_id)
        if file_data and file_data["status"] == "done":
            transcription = reasoning_agent.kb_agent.transcriptions_col.find_one({"file_id": file_id})
            if transcription:
                # Convert MongoDB objects to serializable format
                file_data = json.loads(json.dumps(file_data, cls=MongoJSONEncoder))
                transcription = json.loads(json.dumps(transcription, cls=MongoJSONEncoder))
                file_data["transcription"] = transcription
            logger.info(f"Retrieved file {file_id}")
            return JSONResponse(content=file_data)
        logger.error(f"File {file_id} not found")
        return JSONResponse(content={"error": "File not found"})
    except Exception as e:
        logger.error(f"Error retrieving file {file_id}: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(content={"error": f"Internal server error: {str(e)}"})

@app.post("/api/agents/brds")
async def create_brd(request: CreateBRDRequest):
    valid, error = reasoning_agent.quality_agent.validate_brd(request.selected_key_points)
    if not valid:
        logger.error(f"BRD creation failed: {error}")
        return {"error": error}
    transcription = reasoning_agent.kb_agent.transcriptions_col.find_one({"file_id": request.file_id})
    if not transcription:
        logger.error("Transcription not found")
        return {"error": "Transcription not found"}
    content = reasoning_agent.brd_agent.generate_brd(request.selected_key_points)
    brd_id = str(datetime.datetime.now().timestamp())
    pdf_path = f"data/brds/{brd_id}.pdf"
    reasoning_agent.brd_agent.generate_pdf(content, pdf_path)
    embeddings = reasoning_agent.keypoint_agent.sentence_model.encode(request.selected_key_points)
    brd_data = {
        "id": brd_id,
        "transcription_id": transcription["id"],
        "selected_key_points": request.selected_key_points,
        "content": content,
        "pdf_path": pdf_path,
        "embedding": np.mean(embeddings, axis=0).tolist()
    }
    reasoning_agent.kb_agent.store_brd(brd_data)
    await reasoning_agent.comm_agent.send_email("BRD Created", f"BRD {brd_id} created. Download: /api/agents/brds/{brd_id}/pdf")
    logger.info(f"BRD {brd_id} created")
    return {"brd_id": brd_id, "content": content, "pdf_path": pdf_path}

@app.get("/api/agents/brds/{brd_id}")
def get_brd(brd_id: str):
    brd = reasoning_agent.kb_agent.brds_col.find_one({"id": brd_id})
    if not brd:
        logger.error(f"BRD {brd_id} not found")
        return JSONResponse(content={"error": "BRD not found"})
    logger.info(f"Retrieved BRD {brd_id}")
    return JSONResponse(content=json.loads(json.dumps(brd, cls=MongoJSONEncoder)))

@app.get("/api/agents/brds/{brd_id}/pdf")
def get_brd_pdf(brd_id: str):
    brd = reasoning_agent.kb_agent.brds_col.find_one({"id": brd_id})
    if not brd or not os.path.exists(brd["pdf_path"]):
        logger.error(f"PDF for BRD {brd_id} not found")
        return {"error": "PDF not found"}
    logger.info(f"Serving PDF for BRD {brd_id}")
    return FileResponse(brd["pdf_path"], media_type="application/pdf", filename=f"brd_{brd_id}.pdf")

@app.post("/api/agents/tickets")
async def create_ticket(request: CreateTicketRequest):
    ticket_data = reasoning_agent.task_agent.create_ticket(
        request.brd_id, request.title, request.description, request.type
    )
    valid, error = reasoning_agent.quality_agent.validate_ticket(ticket_data)
    if not valid:
        logger.error(f"Ticket creation failed: {error}")
        return {"error": error}
    reasoning_agent.kb_agent.store_ticket(ticket_data)
    await reasoning_agent.comm_agent.send_email("Ticket Created", f"Ticket {ticket_data['id']} created.")
    logger.info(f"Ticket {ticket_data['id']} created")
    return {"ticket_id": ticket_data["id"]}

@app.get("/api/agents/tickets")
def get_tickets():
    try:
        tickets = list(reasoning_agent.kb_agent.tickets_col.find())
        return JSONResponse(content=json.loads(json.dumps(tickets, cls=MongoJSONEncoder)))
    except Exception as e:
        logger.error(f"Error retrieving tickets: {str(e)}")
        return JSONResponse(content={"error": f"Internal server error: {str(e)}"})

@app.post("/api/agents/similar_brds")
def get_similar_brds(request: SimilarBRDsRequest):
    try:
        similar_brds = list(reasoning_agent.kb_agent.brds_col.find())
        return JSONResponse(content=json.loads(json.dumps(similar_brds, cls=MongoJSONEncoder)))
    except Exception as e:
        logger.error(f"Error retrieving similar BRDs: {str(e)}")
        return JSONResponse(content={"error": f"Internal server error: {str(e)}"})

@app.post("/api/agents/feedback")
async def submit_feedback(request: FeedbackRequest):
    feedback_data = reasoning_agent.feedback_agent.store_feedback(
        request.brd_id, request.rating, request.comments
    )
    await reasoning_agent.communication_agent.send_email(
        "Feedback Received", f"Feedback for BRD {request.brd_id}: Rating {request.rating}"
    )
    logger.info(f"Feedback {feedback_data['id']} submitted")
    return {"feedback_id": feedback_data["id"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)