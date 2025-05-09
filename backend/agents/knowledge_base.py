from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class KnowledgeBaseAgent:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client["multi_agent_system"]
        self.files_col = db["files"]
        self.transcriptions_col = db["transcriptions"]
        self.brds_col = db["brds"]
        self.tickets_col = db["tickets"]
        logger.info("MongoDB connection established")

    def store_file(self, file_data):
        logger.info(f"Storing file {file_data['id']}")
        self.files_col.insert_one(file_data)

    def update_file(self, file_id, update_data):
        logger.info(f"Updating file {file_id}")
        self.files_col.update_one({"id": file_id}, {"$set": update_data})

    def get_file(self, file_id):
        logger.info(f"Retrieving file {file_id}")
        return self.files_col.find_one({"id": file_id})

    def store_transcription(self, transcription_data):
        logger.info(f"Storing transcription {transcription_data['id']}")
        self.transcriptions_col.insert_one(transcription_data)

    def store_brd(self, brd_data):
        logger.info(f"Storing BRD {brd_data['id']}")
        self.brds_col.insert_one(brd_data)

    def store_ticket(self, ticket_data):
        logger.info(f"Storing ticket {ticket_data['id']}")
        self.tickets_col.insert_one(ticket_data)