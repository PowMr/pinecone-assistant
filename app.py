from fastapi import FastAPI
from pydantic import BaseModel
import os
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

app = FastAPI(title="Powmr AI Assistant (Pinecone API)")

# 环境变量
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "powmr-expert")

# 初始化 Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# 创建或获取 Assistant
assistant = pc.assistant.Assistant().create_or_get(name=ASSISTANT_NAME)


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": f"Powmr AI Assistant `{ASSISTANT_NAME}` is running 🚀"}


@app.post("/ask")
def ask_ai(query: Query):
    msg = Message(content=query.question, role="user")
    resp = assistant.chat(messages=[msg])
    return {"answer": resp.message.content}