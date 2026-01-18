import time

import requests
from django.conf import settings
from celery import shared_task


@shared_task
def send_telegram_notification(order_id, product_name, quantity, customer_username, phone_number):
    time.sleep(5)
    token = settings.TELEGRAM_BOT_TOKEN
    method = 'sendMessage'
    message_text = f"New order: {order_id}\nProduct: {product_name}\nQuantity: {quantity}\n" \
                   f"Client: @{customer_username}\nTel: {phone_number}"

    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/{method}",
        data={
            "chat_id": settings.ADMIN_CHAT_ID,
            "text": message_text
        }
    ).json()