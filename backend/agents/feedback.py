import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class FeedbackAgent:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client["multi_agent_system"]
        self.feedback_col = db["feedback"]

    def store_feedback(self, brd_id, rating, comments):
        logger.info(f"Storing feedback for BRD {brd_id}")
        feedback_data = {
            "id": str(datetime.datetime.now().timestamp()),
            "brd_id": brd_id,
            "rating": rating,
            "comments": comments,
            "timestamp": datetime.datetime.now()
        }
        self.feedback_col.insert_one(feedback_data)
        logger.info(f"Feedback {feedback_data['id']} stored")
        return feedback_data