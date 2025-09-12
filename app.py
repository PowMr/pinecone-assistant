from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

# 初始化 FastAPI
app = FastAPI(title="Powmr AI Assistant (Pinecone API)")

# 模板目录
templates = Jinja2Templates(directory="templates")

# 允许 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 环境变量
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "powmr-expert")

# 初始化 Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
assistant = pc.assistant.Assistant(assistant_name=ASSISTANT_NAME)

class Query(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask")
def ask_ai(query: Query):
    msg = Message(content=query.question, role="user")
    resp = assistant.chat(messages=[msg])
    return {"answer": resp["message"]["content"]}