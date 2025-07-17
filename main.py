#Imports
import os
import uvicorn
import openai
from fastapi import FastAPI, Form, Request
from decouple import config


# Internal imports
from utils import send_message
from models import ChatMessage
from db import init_db, get_session
from sqlmodel import Session

init_db()
app = FastAPI()
# Set up the OpenAI API client
openai.api_key = os.environ['OPENAI_API_KEY']


@app.get("/")
async def index():
    return {"msg": "working"}

@app.get("/messages/{phone}")
def get_user_messages(phone: str):
    with Session(engine) as session:
        return session.query(ChatMessage).filter(ChatMessage.user_number == phone).all()


@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    print(f"Sending ChatGPT response to this number: {whatsapp_number}")

    # Call OpenAI API
    messages = [{"role": "user", "content": Body}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5
    )
    chatgpt_response = response.choices[0].message.content

    # Save to DB
    with Session(engine) as session:
        chat_record = ChatMessage(
            user_number=whatsapp_number,
            user_input=Body,
            ai_response=chatgpt_response
        )
        session.add(chat_record)
        session.commit()

    send_message(whatsapp_number, chatgpt_response)
    return ""


uvicorn.run(app,host="0.0.0.0",port="8080")