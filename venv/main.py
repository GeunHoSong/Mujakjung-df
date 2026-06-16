import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv(dotenv_path=".env")

app = FastAPI()

# OpenAI 클라이언트 초기화 (API 키는 .env에 저장되어 있어야 함)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(f"DEBUG: 읽어온 키 확인 -> {api_key}")

class TextRequest(BaseModel):
    content: str

@app.post("/generate")
def generate_text(request: TextRequest):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 공지사항을 간결하게 요약해주는 친절한 AI야."},
            {"role": "user", "content": f"다음 내용을 요약해줘: {request.content}"}
        ]
    )
    return {"summary": response.choices[0].message.content}