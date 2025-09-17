from celery import shared_task

from messenger.models import Message
from messenger.services.telegram_bot_service import MessageTelegramBotService


@shared_task
def send_new_message_notification(message_id):
    message = Message.objects.get(id=message_id)

    service = MessageTelegramBotService()
    service.send_message_created(message)
