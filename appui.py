import os, ssl, arxiv, time, json
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. 환경 설정
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


target_model = "gemini-2.5-flash" 

st.set_page_config(page_title="리서치 에이전트", page_icon="⚡", layout="wide")

st.title("⚡ 논문 추천 에이전트")
st.markdown("---")

# 사이드바 설정
with st.sidebar:
    st.header("🕵️ 지시사항")
    
    # placeholder로 예시를 보여주고, 기본값(value)은 비워둡니다.
    keyword = st.text_input(
        "검색 키워드", 
        placeholder="예: Multi-modal LLM, RAG Optimization..."
    )
    
    research_goal = st.text_area(
        "상세 연구 목적", 
        placeholder="예: 모바일 기기에서 동작 가능한 가벼운 멀티모달 모델의 구조와 효율적인 추론 기법에 대해 알고 싶어."
    )
    
    num_final = st.number_input("최종 추천받을 논문 수", value=3, min_value=1)
    
    st.markdown("---") # 시각적 구분선
    search_button = st.button("시작")

# 버튼을 눌렀을 때 입력 여부 체크
if search_button:
    if not keyword or not research_goal:
        st.warning("⚠️ 검색 키워드와 연구 목적을 모두 입력해 주세요!")
    else:
        # 이 아래부터 에이전트 가동 로직 시작...
        pass

    # 최종 결과가 들어갈 상단 컨테이너
    final_report_container = st.container()
    st.markdown("### 🔍 에이전트 실시간 검토 로그")
    log_container = st.container()

    try:
        # 1. Arxiv 검색 (10개 고정)
        arxiv_client = arxiv.Client()
        search = arxiv.Search(
            query=keyword,
            max_results=10, 
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        candidates = list(arxiv_client.results(search))
        passed_papers = []

        # 2. 실시간 검토 프로세스
        for i, paper in enumerate(candidates):
            with log_container:
                st.write(f"**[{i+1}/10]** `{paper.title}` 분석 중...")
                
                # Flash는 빨라서 대기 시간을 1초로 줄여도 충분합니다.
                time.sleep(1) 
                
                eval_prompt = f"""
                당신은 연구자입니다. 아래 논문을 분석하여 사용자의 목적에 부합하는지 평가하고 요약하세요.
                반드시 아래 JSON 형식으로만 답변하세요:
                {{
                    "score": 0~100,
                    "reason": "선별 또는 제외한 근거 (한 줄)",
                    "brief_summary": "논문의 핵심 내용을 연구자 관점에서 2~3줄로 요약"
                }}
                
                [사용자 목적]: {research_goal}
                [논문 제목]: {paper.title}
                [초록]: {paper.summary}
                """
                
                try:
                    res = client.models.generate_content(model=target_model, contents=eval_prompt)
                    
                    # JSON 데이터 추출
                    raw_text = res.text.strip()
                    clean_json = raw_text[raw_text.find("{"):raw_text.rfind("}")+1]
                    eval_data = json.loads(clean_json)
                    
                    # 실시간 로그 출력
                    st.caption(f"🎯 **판단 점수: {eval_data['score']}점**")
                    st.write(f"💬 **검토 근거:** {eval_data['reason']}")
                    st.info(f"📝 **요약:**\n{eval_data['brief_summary']}")
                    
                    passed_papers.append({
                        "paper": paper,
                        "score": eval_data['score'],
                        "reason": eval_data['reason'],
                        "summary": eval_data['brief_summary']
                    })
                except Exception as e:
                    st.error(f"⚠️ 분석 오류: {e}")
                
                st.write("---")

        # 3. 검토 완료 후 상단 리포트 배치
        sorted_papers = sorted(passed_papers, key=lambda x: x['score'], reverse=True)
        top_picks = sorted_papers[:num_final]

        with final_report_container:
            if not top_picks:
                st.error("❌ 분석 결과 적합한 논문을 찾지 못했습니다.")
            else:
                st.success(f"✅ 검토 완료! 상위 {len(top_picks)}개의 논문을 선정했습니다.")
                
                cols = st.columns(len(top_picks))
                for idx, item in enumerate(top_picks):
                    with cols[idx]:
                        st.markdown(f"### 🏆 Top {idx+1}")
                        st.metric(label="적합성 점수", value=f"{item['score']}점")
                        st.markdown(f"**제목:** {item['paper'].title}")
                        st.warning(f"**한줄평:**\n{item['reason']}")
                        st.markdown(f"**📝 심층 요약:**\n{item['summary']}")
                        st.link_button("논문 원문 보기", item['paper'].entry_id)
                
                st.markdown("---")
                st.balloons()

    except Exception as e:
        st.error(f"🔥 시스템 오류: {e}")