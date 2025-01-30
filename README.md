# LangGraph Projects

LangGraph를 활용한 다양한 프로젝트 모음입니다. 각 프로젝트는 LangGraph의 다양한 활용 사례를 보여줍니다.

## 프로젝트 목록

### 1. [Meta Prompt Generator](projects/meta_prompt)
- 🤖 대화형 메타 프롬프트 생성 시스템
- LangGraph를 활용한 프롬프트 최적화 파이프라인
- Streamlit + FastAPI 기반의 웹 인터페이스

### 2. [프로젝트 2] (예정)
- 프로젝트 설명
- 주요 기능
- 기술 스택

### 3. [프로젝트 3] (예정)
- 프로젝트 설명
- 주요 기능
- 기술 스택

## 프로젝트 구조

```
langgraph/
├── projects/                    # 실제 구현 프로젝트
    ├── meta_prompt/            # 메타 프롬프트 생성기
    │   ├── app/               # 웹 애플리케이션
    │   ├── graph/            # LangGraph 구현
    │   └── README.md        # 프로젝트 문서
    └── project2/            # 다음 프로젝트
```

## 시작하기

각 프로젝트는 독립적으로 실행할 수 있으며, 자세한 설정과 실행 방법은 각 프로젝트의 README를 참조하세요.

### 환경 설정
```bash
# 저장소 클론
git clone https://github.com/yourusername/langgraph.git
cd langgraph

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## 기여하기

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다: `git checkout -b feature/amazing-feature`
3. 변경사항을 커밋합니다: `git commit -m 'Add some amazing feature'`
4. 원격 저장소에 푸시합니다: `git push origin feature/amazing-feature`
5. Pull Request를 생성합니다.

## 프로젝트 제안

새로운 프로젝트를 제안하고 싶으시다면:
1. Issues 탭에서 새로운 이슈를 생성합니다.
2. 프로젝트 제안 템플릿을 사용하여 상세 내용을 작성합니다.
3. 'project-proposal' 레이블을 추가합니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 