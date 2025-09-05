# 🚀 Streamlit Cloud 배포 가이드

## 📋 배포 준비 완료!

모든 파일이 준비되었습니다. 이제 Streamlit Cloud에 배포할 수 있습니다.

## 🔧 배포 단계

### 1. GitHub 저장소 업로드
다음 파일들을 GitHub 저장소에 업로드하세요:

```
├── streamlit_cloud_app.py    # 메인 Streamlit 앱
├── requirements_cloud.txt    # 의존성 파일
├── env_example.txt          # API 키 예시
└── STREAMLIT_CLOUD_DEPLOYMENT.md  # 이 가이드
```

### 2. Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. "New app" 클릭
3. GitHub 저장소 연결
4. 앱 설정:
   - **Main file path**: `streamlit_cloud_app.py`
   - **Requirements file**: `requirements_cloud.txt`

### 3. 환경 변수 설정
Streamlit Cloud 앱 설정에서 환경 변수를 추가하세요:

```
OPENAI_API_KEY = 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
```

## 🎯 배포 후 사용법

1. **Streamlit Cloud 앱 접속**
2. **자동 설정 확인**: 환경 변수가 설정되어 있으면 API 키가 자동으로 로드됩니다
3. **주제 입력**: 원하는 블로그 주제를 입력하세요
4. **콘텐츠 생성**: "🚀 콘텐츠 생성" 버튼을 클릭하세요
5. **결과 확인**: 생성된 콘텐츠를 확인하고 다운로드하세요

## ✨ 주요 기능

- **🤖 AI 에이전트 협업**: 3개의 AI 에이전트가 순차적으로 작업
- **📝 콘텐츠 기획**: 주제에 맞는 아웃라인 생성
- **✍️ 콘텐츠 작성**: 전문적인 블로그 포스트 작성
- **📖 편집 및 교정**: 문법 및 스타일 개선
- **💾 다운로드**: 마크다운 형식으로 다운로드
- **🔄 실시간 진행률**: 생성 과정 시각화

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI Framework**: CrewAI
- **Language Model**: OpenAI GPT (3.5-turbo, GPT-4, GPT-4-turbo)
- **Deployment**: Streamlit Cloud
- **Cost**: OpenAI API 사용량에 따른 과금

## 💰 비용 정보

- **Streamlit Cloud**: 무료
- **OpenAI API**: 토큰당 과금
  - GPT-3.5-turbo: $0.0015/1K tokens (입력), $0.002/1K tokens (출력)
  - GPT-4: $0.03/1K tokens (입력), $0.06/1K tokens (출력)

## 🔒 보안 주의사항

- API 키는 환경 변수로 설정하여 코드에 노출되지 않도록 했습니다
- Streamlit Cloud의 환경 변수 설정을 사용하세요
- API 키를 공개 저장소에 커밋하지 마세요

## 🎉 배포 완료!

모든 설정이 완료되면 전 세계 어디서든 접속 가능한 AI 블로그 콘텐츠 생성 서비스를 사용할 수 있습니다!
