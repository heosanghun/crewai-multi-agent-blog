import streamlit as st
import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
import time

# 페이지 설정
st.set_page_config(
    page_title="CrewAI 블로그 콘텐츠 생성기",
    page_icon="🤖",
    layout="wide"
)

# 제목 및 설명
st.title("🤖 CrewAI 블로그 콘텐츠 생성기")
st.markdown("주제에 맞는 블로그 콘텐츠를 생성하기 위해 CrewAI와 OpenAI를 사용합니다.")

# OpenAI API 키 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # OpenAI API 키 입력 (환경 변수에서 자동 로드)
    default_key = os.getenv("OPENAI_API_KEY", "")
    openai_api_key = st.text_input(
        "OpenAI API 키",
        value=default_key,
        type="password",
        help="OpenAI API 키를 입력하세요. 환경 변수에 설정되어 있으면 자동으로 로드됩니다."
    )
    
    # 모델 선택
    model_choice = st.selectbox(
        "사용할 모델",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        help="사용할 OpenAI 모델을 선택하세요."
    )
    
    st.markdown("---")
    st.markdown("### 📊 시스템 상태")
    
    if openai_api_key:
        st.success("✅ OpenAI API 키 설정됨")
    else:
        st.warning("⚠️ OpenAI API 키를 입력해주세요")

# AI 에이전트 생성 함수
@st.cache_resource
def create_agents(api_key, model):
    if not api_key:
        return None
    
    # OpenAI LLM 설정
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0.7
    )
    
    # 에이전트들 생성
    planner = Agent(
        role="콘텐츠 기획자",
        goal="{topic}에 대한 블로그 게시물 아웃라인과 콘텐츠 전략을 계획합니다.",
        backstory="당신은 상세하고 매력적인 콘텐츠 아웃라인을 만드는 데 능숙한 콘텐츠 전략가입니다.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    
    writer = Agent(
        role="콘텐츠 작가",
        goal="{topic}에 대한 블로그 게시물의 초안을 작성합니다.",
        backstory="당신은 주어진 아웃라인을 바탕으로 흥미롭고 유익한 기사를 작성하는 재능 있는 작가입니다.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    
    editor = Agent(
        role="콘텐츠 편집자",
        goal="작성된 블로그 게시물을 교정하고 편집하여 품질을 향상시킵니다.",
        backstory="당신은 문법, 스타일, 톤을 예리하게 파악하는 숙련된 편집자입니다.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    
    return planner, writer, editor

# 작업 생성 함수
def create_tasks(planner, writer, editor, topic):
    plan = Task(
        description=f"{topic}에 대한 블로그 게시물 아웃라인과 콘텐츠 전략을 개발합니다.",
        expected_output=f"{topic}에 대한 상세한 블로그 게시물 아웃라인으로, 주요 섹션, 핵심 포인트, SEO 키워드가 포함되어야 합니다.",
        agent=planner,
    )
    
    write = Task(
        description=f"{topic}에 대한 블로그 게시물을 작성합니다. 기획자가 제공한 아웃라인을 따릅니다.",
        expected_output="기획된 아웃라인을 기반으로 한 잘 작성된 블로그 게시물 초안입니다.",
        agent=writer,
        context=[plan]
    )
    
    edit = Task(
        description="작성된 블로그 게시물을 교정하고 편집하여 가독성과 문법적 정확성을 보장합니다.",
        expected_output="오류가 없고, 문체가 일관되며, 독자의 참여를 유도할 수 있도록 세련되게 편집된 최종 버전의 블로그 게시물입니다.",
        agent=editor,
        context=[write]
    )
    
    return [plan, write, edit]

# 메인 컨텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 콘텐츠 생성")
    
    # 주제 입력
    topic = st.text_input(
        "블로그 작성 주제를 입력해주세요.",
        placeholder="예: 인공지능의 미래",
        key="topic_input"
    )
    
    # 생성 버튼
    if st.button("🚀 콘텐츠 생성", type="primary", disabled=not topic or not openai_api_key):
        if topic and openai_api_key:
            # 에이전트 생성
            agents = create_agents(openai_api_key, model_choice)
            
            if agents:
                planner, writer, editor = agents
                
                # 진행 상황 표시
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # 작업 생성
                    tasks = create_tasks(planner, writer, editor, topic)
                    
                    # Crew 생성
                    crew = Crew(
                        agents=[planner, writer, editor],
                        tasks=tasks,
                        process=Process.sequential,
                        verbose=False
                    )
                    
                    # 진행 상황 업데이트
                    status_text.text("🤖 AI 에이전트들이 작업을 시작합니다...")
                    progress_bar.progress(20)
                    
                    # Crew 실행
                    result = crew.kickoff({"topic": topic})
                    
                    progress_bar.progress(100)
                    status_text.text("✅ 콘텐츠 생성 완료!")
                    
                    # 결과 저장
                    st.session_state['generated_content'] = str(result)
                    st.session_state['topic'] = topic
                    
                    st.success("✅ 콘텐츠가 성공적으로 생성되었습니다!")
                    
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
                    progress_bar.progress(0)
                    status_text.text("")
            else:
                st.error("❌ 에이전트 생성에 실패했습니다.")

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
            file_name=f"blog_content_{topic}_{time.strftime('%Y%m%d_%H%M%S')}.md",
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
        <p>🤖 CrewAI 블로그 콘텐츠 생성기 | Powered by Streamlit Cloud</p>
        <p><small>이 애플리케이션은 CrewAI, OpenAI API, Streamlit을 사용하여 구축되었습니다.</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
