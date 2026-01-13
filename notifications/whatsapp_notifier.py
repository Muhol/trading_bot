from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class WhatsAppNotifier:
    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_WHATSAPP_FROM")
        self.to_number = os.getenv("WHATSAPP_TO")

    def send(self, message: str):
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=self.to_number
        )
