# FastAPI 웹 서버 프레임워크
from fastapi import FastAPI

# 요청 데이터 검증을 위한 Pydantic 모델
from pydantic import BaseModel

# Google Gemini API 클라이언트
from google import genai

# .env 파일에서 환경변수 로드
from dotenv import load_dotenv

# OS 환경변수 접근용
import os


# .env 파일 로드 (GOOGLE_API_KEY 등을 읽기 위해 필요)
load_dotenv()

# 환경변수에서 Google API 키 가져오기
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini API 클라이언트 생성 (API KEY 기반 인증)
client = genai.Client(api_key=api_key)

# FastAPI 앱 생성
app = FastAPI()


# 요청(Request) 데이터 구조 정의
# 클라이언트가 보내는 JSON 형태를 검증함
class TextRequest(BaseModel):
    content: str   # 사용자가 입력하는 텍스트 (필수 필드)


# POST /generate 엔드포인트 생성
# 클라이언트가 텍스트를 보내면 Gemini로 요약/생성 수행
@app.post("/generate")
def generate(request: TextRequest):

    # Gemini 모델 호출
    # model: 사용 모델 (gemini-2.0-flash → 빠른 응답용 모델)
    # contents: 사용자 입력 텍스트
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=request.content
    )

    # 결과를 JSON 형태로 반환
    # response.text → Gemini가 생성한 텍스트 결과
    return {
        "summary": response.text
    }