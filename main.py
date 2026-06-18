import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# 1. 환경 변수 로드
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("에러: GEMINI_API_KEY가 없습니다. .env 파일을 확인하세요.")
    sys.exit(1) # API 키 없으면 서버 시작 불가하게 설정

genai.configure(api_key=api_key)
# 모델명 확인: 현재 공식 지원되는 모델명을 사용하는 것이 안전해
model = genai.GenerativeModel("gemini-1.5-flash") 

app = FastAPI()

class TextRequest(BaseModel):
    content: str

# 2. 비동기(async) 호출 적용
@app.post("/generate")
async def generate_text(request: TextRequest):
    if not request.content:
        raise HTTPException(status_code=400, detail="내용이 비어있습니다.")
        
    try:
        # 모델 호출 (await 추가)
        response = await model.generate_content_async(
            f"다음 공지사항을 간단히 요약해줘.\n\n{request.content}"
        )
        return {"summary": response.text}

    except Exception as e:
        # 로그 기록 및 클라이언트에게 에러 전달
        print(f"에러 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))