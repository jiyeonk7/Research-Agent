import os
import ssl
import arxiv
from google import genai
from dotenv import load_dotenv

# 1. SSL 인증서 오류 우회
ssl._create_default_https_context = ssl._create_unverified_context

# 2. 설정 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ 에러: .env 파일에 GEMINI_API_KEY를 확인하세요.")
else:
    # 3. 최신 Google GenAI 클라이언트 설정
    client = genai.Client(api_key=api_key)

    # print("📋 사용 가능한 모델 목록을 가져오는 중...")
    # try:
    #     for m in client.models.list():
    #         print(f"사용 가능 모델명: {m.name}")
    # except Exception as e:
    #     print(f"모델 목록 조회 실패: {e}")
    # print("=" * 60)
    
    # 4. Arxiv 검색 설정
    print("🔍 Arxiv에서 최신 논문을 검색 중입니다...")
    arxiv_client = arxiv.Client()
    search = arxiv.Search(
        query = "Large Language Model optimization",
        max_results = 3,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    print("🚀 AI 연구 PM 에이전트 브리핑을 시작합니다.\n")
    print("=" * 60)

    # 5. 검색 및 요약 로직
    for result in arxiv_client.results(search):
        prompt = f"다음 논문의 제목과 초록을 3줄로 요약해줘.\n제목: {result.title}\n초록: {result.summary}"
        
        try:
            # 모델 이름을 'gemini-1.5-flash' 대신 'gemini-pro' 또는 'gemini-1.5-flash-latest' 사용
            response = client.models.generate_content(
                model="models/gemini-2.5-flash", # 만약 실패하면 "gemini-pro"로 수정
                contents=prompt
            )
            
            print(f"📌 [논문 제목]: {result.title}")
            print(f"📝 [요약]:\n{response.text.strip()}")
            print("-" * 60)
        except Exception as e:
            # 에러가 나면 모델을 바꿔서 한 번 더 시도하는 로직 (보험)
            try:
                response = client.models.generate_content(model="models/gemini-2.5-pro", contents=prompt)
                print(f"📌 [논문 제목]: {result.title}")
                print(f"📝 [요약(Pro)]: {response.text.strip()}")
            except:
                print(f"❌ 요약 실패: {e}")

    print("\n✅ 오늘자 브리핑이 완료되었습니다.")