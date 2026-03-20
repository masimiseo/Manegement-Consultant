import streamlit as st
import google.generativeai as genai

# 🚨 [아주 중요] 다시 한번, 본인의 API 키를 꼭 아래 따옴표 안에 넣으세요!
API_KEY = st.secrets["GEMINI_API_KEY"]
model = genai.GenerativeModel('gemini-2.0-flash')

# AI 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')
# 앱 화면 전체 디자인 세팅
st.set_page_config(page_title="경영지도사 합격 루틴", page_icon="📈")
st.title("📈 경영지도사 2차 마케팅 완벽 루틴 앱")
st.write("스마트폰으로 언제 어디서나 학습하세요. 상단의 탭을 눌러 단계를 이동할 수 있습니다.")
st.markdown("---")

# 4개의 탭(메뉴) 만들기
tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ 1단계(평일)", "2️⃣ 2단계(평일)", "3️⃣ 3단계(주말)", "4️⃣ 4단계(주말)"])

# ---------------------------------------------------------
# [탭 1] 평일 출퇴근길 키워드 암기
# ---------------------------------------------------------
with tab1:
    st.header("📱 1단계: 출퇴근길 키워드 암기")
    st.write("버튼을 누르면 출제 빈도가 높은 핵심 논점 하나를 AI가 1분 요약해 줍니다.")
    
    subject = st.selectbox("오늘 공부할 과목을 선택하세요", ["마케팅관리론", "소비자행동론", "시장조사론"])
    
    if st.button("오늘의 핵심 1분 요약 뽑기"):
        with st.spinner("AI가 출퇴근길 맞춤형 핵심 노트를 작성 중입니다..."):
            prompt = f"너는 경영지도사 2차 마케팅 출제위원이야. '{subject}' 과목에서 매우 중요한 논점 1개를 무작위로 골라줘. 출퇴근길에 스마트폰으로 빠르게 읽고 외울 수 있도록, 1) 해당 논점의 '개념 요약'과 2) 무조건 답안지에 적어야 할 '필수 암기 키워드 5개'를 아주 간결하고 가독성 좋게 정리해 줘."
            response = model.generate_content(prompt)
            st.success("오늘의 학습 노트가 도착했습니다!")
            st.write(response.text)

# ---------------------------------------------------------
# [탭 2] 평일 뼈대(목차) 잡기 연습
# ---------------------------------------------------------
with tab2:
    st.header("📝 2단계: 답안 뼈대(목차) 잡기 연습")
    st.write("완벽한 문장을 쓰려 하지 마세요! 이면지에 끄적이듯 **목차**와 **핵심 키워드**만 툭툭 던져보세요.")
    
    topic_input = st.text_input("연습할 논점 (예: 시장침투가격과 초기고가전략)")
    skeleton_input = st.text_area("목차 및 키워드 메모 (자유롭게 끄적여보세요)", height=150)
    
    if st.button("뼈대 흐름 AI에게 검토받기"):
        if topic_input and skeleton_input:
            with st.spinner("AI가 논리 흐름과 누락된 키워드를 검토 중입니다..."):
                prompt = f"경영지도사 2차 마케팅 시험이야. 오늘 연습할 주제는 '{topic_input}'이고, 아래는 내가 머릿속으로 떠올려본 답안의 뼈대(목차와 키워드)야. \n내가 잡은 방향성이 맞는지, 그리고 반드시 들어가야 하는데 빠진 '핵심 키워드'가 있는지 짧고 굵게 피드백해 줘.\n\n[내 뼈대 메모]\n{skeleton_input}"
                response = model.generate_content(prompt)
                st.info("검토 결과입니다!")
                st.write(response.text)
        else:
            st.warning("논점과 메모를 모두 입력해 주세요!")

# ---------------------------------------------------------
# [탭 3] 주말 실전 모의고사 (기존과 동일)
# ---------------------------------------------------------
with tab3:
    st.header("🎲 3단계: 주말 실전 모의고사 출제")
    
    if 'questions' not in st.session_state:
        st.session_state.questions = ""
        
    if st.button("실전 모의고사 3문제 뽑기 (논술 1, 약술 2)"):
        with st.spinner("출제위원이 문제를 엄선 중입니다..."):
            prompt = "너는 경영지도사 2차 마케팅 분야 출제위원이야. [마케팅관리론, 소비자행동론, 시장조사론] 세 과목의 주요 논점 중에서 오늘 내가 풀 문제 3개를 랜덤으로 뽑아줘. (논술형 30점 1문제, 약술형 10점 2문제 형식으로)"
            response = model.generate_content(prompt)
            st.session_state.questions = response.text
            
    if st.session_state.questions:
        st.write(st.session_state.questions)

# ---------------------------------------------------------
# [탭 4] 주말 답안 AI 채점관 (기존과 동일)
# ---------------------------------------------------------
with tab4:
    st.header("💯 4단계: 실전 답안 AI 채점관")
    st.write("3단계에서 출제된 문제 중 하나를 골라, 실제 시험처럼 답안을 작성해 보세요.")
    
    user_answer = st.text_area("✍️ 작성한 실전 답안을 여기에 입력하세요.", height=300)
    
    if st.button("채점관에게 최종 제출하기"):
        if user_answer:
            with st.spinner("채점관이 답안을 꼼꼼히 평가 중입니다..."):
                grading_prompt = f"""
                너는 경영지도사 2차 마케팅 분야 채점관이야. 아래 내가 작성한 답안을 평가해 줘.
                1) 필수 키워드가 포함되었는지 
                2) 논리적 흐름이 매끄러운지 
                3) 감점 요소는 무엇인지 분석하고, 
                4) 더 높은 점수를 받기 위한 '한 줄 개선 포인트'를 알려줘.
                
                [내 답안]
                {user_answer}
                """
                grade_response = model.generate_content(grading_prompt)
                st.success("채점이 완료되었습니다!")
                st.write(grade_response.text)
        else:
            st.warning("먼저 답안을 입력해 주세요!")
