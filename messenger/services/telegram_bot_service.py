from django.conf import settings

from base.services.telegram_bot_service import BaseTelegramBotService
from messenger.models import Message


class MessageTelegramBotService(BaseTelegramBotService):
    def __init__(self, token=settings.MESSAGE_TELEGRAM_BOT_TOKEN):
        super().__init__(token)

    @staticmethod
    def _get_message_created_text(message: Message):
        return f"New message created: {message.text_preview}\nuser: {message.user.username}"

    def send_message_created(self, message: Message):
        text = self._get_message_created_text(message)

        if message.user.telegram_id:
            self.send_message(message.user.telegram_id, text)
