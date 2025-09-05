import streamlit as st
import requests
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="AI 블로그 콘텐츠 생성기",
    page_icon="🤖",
    layout="wide"
)

# 제목
st.title("🤖 AI 블로그 콘텐츠 생성기")
st.markdown("OpenAI API를 사용하여 블로그 콘텐츠를 생성합니다.")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    
    # OpenAI API 키 자동 로드 (환경 변수에서)
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    # 모델 선택
    model = st.selectbox(
        "사용할 모델",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0
    )
    
    # API 키 상태 표시
    if api_key:
        st.success("🔑 API 키가 자동으로 설정되었습니다!")
        st.info("💡 API 키는 환경 변수에서 자동으로 로드됩니다.")
    else:
        st.error("❌ API 키가 설정되지 않았습니다!")
        st.warning("⚠️ Streamlit Cloud Secrets에서 OPENAI_API_KEY를 설정해주세요.")

# 메인 컨텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 콘텐츠 생성")
    
    # 주제 입력
    topic = st.text_input(
        "블로그 주제를 입력하세요",
        placeholder="예: 인공지능의 미래",
        key="topic_input"
    )
    
    # 생성 버튼
    if st.button("🚀 콘텐츠 생성", type="primary", disabled=not topic or not api_key):
        if topic and api_key:
            with st.spinner("콘텐츠를 생성하고 있습니다..."):
                try:
                    # OpenAI API 호출 (requests 사용)
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "당신은 전문적인 블로그 작가입니다. 매력적이고 유익한 콘텐츠를 작성하는 데 능숙합니다."
                            },
                            {
                                "role": "user",
                                "content": f"""
                                다음 주제에 대한 전문적이고 매력적인 블로그 포스트를 작성해주세요:
                                
                                주제: {topic}
                                
                                다음 구조로 작성해주세요:
                                1. 매력적인 제목
                                2. 흥미로운 소개
                                3. 주요 내용 (3-4개 섹션)
                                4. 실용적인 팁이나 조언
                                5. 강력한 결론
                                
                                마크다운 형식으로 작성하고, 한국어로 작성해주세요.
                                """
                            }
                        ],
                        "max_tokens": 2000,
                        "temperature": 0.7
                    }
                    
                    response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        
                        # 결과 저장
                        st.session_state['generated_content'] = content
                        st.session_state['topic'] = topic
                        
                        st.success("✅ 콘텐츠가 성공적으로 생성되었습니다!")
                    else:
                        st.error(f"❌ API 오류: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")

with col2:
    st.header("📄 생성된 콘텐츠")
    
    if 'generated_content' in st.session_state:
        # 콘텐츠 표시
        st.markdown("### 📋 미리보기")
        st.markdown(st.session_state['generated_content'])
        
        # 다운로드 버튼
        st.download_button(
            label="💾 다운로드",
            data=st.session_state['generated_content'],
            file_name=f"blog_content_{topic}.md",
            mime="text/markdown"
        )
        
        # 새로 생성 버튼
        if st.button("🔄 새 콘텐츠 생성"):
            for key in ['generated_content', 'topic']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.info("👈 왼쪽에서 주제를 입력하고 콘텐츠를 생성해보세요!")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🤖 AI 블로그 콘텐츠 생성기 | Powered by OpenAI & Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
