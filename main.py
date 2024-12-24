import logging
from receiver import EmailReceiver
from llm import LLMProcessor
from processor import EmailProcessor
from credentials import sender_email, sender_password

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize the components
    email_receiver = EmailReceiver(sender_email, sender_password)
    llm_processor = LLMProcessor()
    email_processor = EmailProcessor(sender_email, sender_password)
    
    # Fetch unread emails
    email_details = email_receiver.fetch_unread_emails()
    
    # Process each email
    for from_email, body in email_details:
        subject, body_reply = llm_processor.generate_reply(body)
        email_processor.process_email(from_email, subject, body_reply)

if __name__ == "__main__":
    main()