from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
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

# 请求模型
class Query(BaseModel):
    question: str

# 首页
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# /ask 接口
@app.post("/ask")
async def ask_ai(query: Query):
    """
    调用 Pinecone Assistant，返回 Markdown 格式文本
    前端使用 marked.js 渲染
    """
    msg = Message(content=query.question, role="user")
    resp = assistant.chat(messages=[msg])
    answer = resp["message"]["content"]

    # 这里可以根据需要，确保回答是 Markdown 格式
    # 如果想让 Assistant 输出 Markdown，可在 prompt 中要求：
    # "Answer in Markdown format: use headings, bullet points, line breaks"
    
    return JSONResponse({"answer": answer})