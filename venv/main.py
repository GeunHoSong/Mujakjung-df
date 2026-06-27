import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
# 1. 여기서 변경!
from google import genai 

load_dotenv(".env")

# 2. 클라이언트 초기화 방식 변경
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class TextRequest(BaseModel):
    content: str

@app.post("/generate")
async def generate_text(request: TextRequest):
    try:
        # 3. 모델 호출 방식 변경 (gemini-2.0-flash 권장)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"다음 공지사항을 간단히 요약해줘.\n\n{request.content}"
        )
        return {"summary": response.text}

    except Exception as e:
        print(f"에러 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))