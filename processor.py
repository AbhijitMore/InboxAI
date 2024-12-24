from sender import EmailSender
from credentials import sender_email, sender_password
import logging


class EmailProcessor:
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.email_sender = EmailSender(self.smtp_server, self.port, sender_email, sender_password)

    def process_email(self, from_email: str, subject: str, body: str) -> None:
        """Processes and sends an email reply."""
        logging.info(f"Processing email from {from_email}")
        self.email_sender.send_email(from_email, subject, body)
