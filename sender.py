import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from credentials import sender_email, sender_password
from typing import Optional
import logging


class EmailSender:
    def __init__(self, smtp_server: str, port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def create_attachment(self, attachment_path: str) -> MIMEBase:
        """Creates and returns a MIMEBase object for the attachment."""
        with open(attachment_path, 'rb') as attachment:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(attachment.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(attachment_path)}'
            )
        return mime_base

    def connect_to_server(self) -> smtplib.SMTP:
        """Establishes and returns a connection to the SMTP server."""
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()  # Upgrade the connection to secure
        server.login(self.sender_email, self.sender_password)  # Log in to the SMTP server
        return server

    def send_email(self, recipient_email: str, subject: str, body: str, attachment_path: Optional[str] = None) -> None:
        """Sends the email with the provided details."""
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            # Attach the email body
            message.attach(MIMEText(body, 'plain'))

            # Attach a file if provided
            if attachment_path and os.path.exists(attachment_path):
                attachment = self.create_attachment(attachment_path)
                message.attach(attachment)

            # Connect to the SMTP server
            with self.connect_to_server() as server:
                server.send_message(message)  # Send the email

            logging.info("Email sent successfully!")

        except Exception as e:
            logging.error(f"Failed to send email: {e}")