import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class CommunicationAgent:
    def __init__(self):
        # Load email configuration from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.from_email = os.getenv("EMAIL_USER")
        self.to_email = os.getenv("EMAIL_TO")
        self.email_password = os.getenv("EMAIL_PASS")

        if not all([self.from_email, self.to_email, self.email_password]):
            logger.warning("Email configuration incomplete. Please check environment variables.")

    async def send_email(self, subject, body):
        if not all([self.from_email, self.to_email, self.email_password]):
            logger.error("Email configuration missing. Cannot send email.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.from_email, self.email_password)
            server.sendmail(self.from_email, self.to_email, msg.as_string())
            server.quit()
            logger.info(f"Email sent successfully to {self.to_email}")
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            raise