import logging

logger = logging.getLogger(__name__)

class QualityCheckAgent:
    def validate_brd(self, selected_key_points):
        logger.info("Validating BRD key points")
        if not selected_key_points:
            logger.error("No key points selected for BRD")
            return False, "No key points selected"
        return True, None

    def validate_ticket(self, ticket_data):
        logger.info("Validating ticket data")
        required = ["title", "description", "type"]
        missing = [field for field in required if not ticket_data.get(field)]
        if missing:
            logger.error(f"Missing ticket fields: {', '.join(missing)}")
            return False, f"Missing fields: {', '.join(missing)}"
        return True, None