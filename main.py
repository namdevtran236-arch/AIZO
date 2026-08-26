import os
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

llm = Llama(
    model_path="/code/model.gguf",
    n_ctx=2048,
    n_threads=4
)

SYSTEM_PROMPT = """Bạn là AIZO - Trợ lý AI thông minh, linh hoạt và thân thiện.
Quy tắc trả lời:
1. Trả lời bằng tiếng Việt tự nhiên, ngắn gọn, đi thẳng vào trọng tâm.
2. Dùng định dạng rõ ràng (gạch đầu dòng, đánh số) khi giải thích vấn đề.
3. Duy trì phong cách thân thiện và ghi nhớ ngữ cảnh cuộc trò chuyện."""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: list[Message]

@app.get("/")
def home():
    return {"status": "AIZO Backend 24/7 đang hoạt động ngon lành!"}

@app.post("/v1/chat")
def chat(req: ChatRequest):
    formatted_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{SYSTEM_PROMPT}<|eot_id|>"
    
    for msg in req.history:
        formatted_prompt += f"<|start_header_id|>{msg.role}<|end_header_id|>\n\n{msg.content}<|eot_id|>"
    
    formatted_prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

    output = llm(
        formatted_prompt,
        max_tokens=512,
        stop=["<|eot_id|>"],
        temperature=0.7,
        echo=False
    )

    reply = output["choices"][0]["text"].strip()
    return {"reply": reply}
