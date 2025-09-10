from fastapi import FastAPI
from pydantic import BaseModel
import os
from pinecone import Pinecone
from pinecone_plugins.assistant import Assistant
from pinecone_plugins.assistant.models.chat import Message

# 初始化 FastAPI
app = FastAPI(title="Powmr AI Assistant (Pinecone API)")

# 环境变量
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "powmr-expert")  # 默认 assistant 名字

# 初始化 Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# 创建 Assistant
assistant = Assistant(pinecone=pc, assistant_name=ASSISTANT_NAME)


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": f"Powmr AI Assistant `{ASSISTANT_NAME}` is running 🚀"}


@app.post("/ask")
def ask_ai(query: Query):
    msg = Message(content=query.question, role="user")
    resp = assistant.chat(messages=[msg])
    return {"answer": resp["message"]["content"]}