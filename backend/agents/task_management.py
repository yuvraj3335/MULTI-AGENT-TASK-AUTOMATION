import datetime

class TaskManagementAgent:
    def create_ticket(self, brd_id, title, description, type):
        return {
            "id": str(datetime.datetime.now().timestamp()),
            "brd_id": brd_id,
            "title": title,
            "description": description,
            "type": type,
            "status": "open"
        }