import os
#Standard Library
import logging

#Other Imp Libraries
from twilio.rest import Client
from decouple import config


#Our account SID and Auth Token
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
twilio_number = os.environ['TWILIO_NUMBER']


#Lets Setup logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)



#Sending message using Twilio Api
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_= f"whatsapp:{twilio_number}",
            body = body_text,
            to = f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")