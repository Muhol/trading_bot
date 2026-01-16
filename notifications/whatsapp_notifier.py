import os
from typing import Optional

try:
    from twilio.rest import Client
except ImportError:
    Client = None


class WhatsAppNotifier:
    """
    Safe WhatsApp notifier using Twilio.
    Will not crash the app if Twilio is not configured.
    """

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_FROM")

        self.enabled = all([
            self.account_sid,
            self.auth_token,
            self.from_number,
            Client is not None
        ])

        if self.enabled:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None

    def send_whatsapp_message(self, message: str, to_number: Optional[str] = None) -> bool:
        """
        Simple functional wrapper for SignalDispatcher.
        If to_number is not provided, uses ADMIN_WHATSAPP_NUMBER.
        """
        if to_number is None:
            to_number = os.getenv("ADMIN_WHATSAPP_NUMBER")

        if not to_number:
            print("[WhatsAppNotifier] No recipient number configured")
            return False

        if not self.enabled:
            print("[WhatsAppNotifier] WhatsApp notifications not configured")
            return False

        try:
            self.client.messages.create(
                from_="whatsapp:" + self.from_number,
                to="whatsapp:" + to_number,
                body=message
            )
            return True
        except Exception as e:
            print(f"[WhatsAppNotifier] Failed to send message: {e}")
            return False


# Global instance for functional use
_notifier = WhatsAppNotifier()


def send_whatsapp_message(message: str, to_number: Optional[str] = None) -> bool:
    """
    Functional wrapper to send WhatsApp messages.
    Uses the global notifier instance.
    """
    return _notifier.send_whatsapp_message(message, to_number)