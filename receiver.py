import imaplib
import email
from email.header import decode_header
from typing import List, Tuple
from credentials import sender_email, sender_password
import logging

class EmailReceiver:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
    
    def connect(self):
        """Establishes a connection to the mail server."""
        self.mail.login(self.username, self.password)
        self.mail.select("inbox")
    
    def disconnect(self):
        """Closes the connection to the mail server."""
        self.mail.close()
        self.mail.logout()
    
    def get_body(self, msg) -> str:
        """Extracts the body of the email."""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition and content_type == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            if msg.get_content_type() == "text/plain":
                return msg.get_payload(decode=True).decode()
        return ""
    
    def fetch_unread_emails(self) -> List[Tuple[str, str]]:
        """Fetches unread emails and returns the sender and body."""
        try:
            self.connect()
            status, messages = self.mail.search(None, ('UNSEEN'))
            email_ids = messages[0].split()
            email_details = []

            for email_id in email_ids:
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        from_email = self.extract_email(msg.get('From'))
                        body = self.get_body(msg)
                        if from_email == 'abhimore822@gmail.com':
                            email_details.append((from_email, body))
                
                # Mark the email as read
                self.mail.store(email_id, '-FLAGS', '\\Seen')
            
            return email_details
        
        except Exception as e:
            logging.error(f"Failed to fetch emails: {e}")
            return []
        
        finally:
            self.disconnect()
    
    def extract_email(self, from_string: str) -> str:
        """Extracts the email address from the 'From' field."""
        start_index = from_string.find('<')
        end_index = from_string.find('>', start_index)
        if start_index != -1 and end_index != -1:
            return from_string[start_index + 1:end_index]
        return from_string
