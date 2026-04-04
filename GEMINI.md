# GEMINI.md - Gemini Study Project Mandates

이 파일은 **Gemini Study** 프로젝트 내에서 Gemini CLI가 준수해야 할 프로젝트 전용 지침입니다.

## 1. 문서화 표준 (Documentation Standards)
- **README.md 구조 유지**: `README.md`를 수정할 때는 항상 최상단의 목차(Table of Contents)와 섹션 번호를 최신 상태로 유지해야 합니다.
- **언어 및 톤**: 팀 발표 자료이므로 전문적이면서도 동료 개발자들에게 친근한 톤을 유지합니다.

## 2. 자산 관리 (Asset Management)
- **이미지 네이밍**: 한국어로 된 이미지 파일(예: `스크린샷...`, `요금제...`)은 반드시 의미 있는 영문 이름(예: `gemini_demo.png`, `gemini_pricing.png`)으로 변경한 뒤 프로젝트에 포함합니다.
- **이미지 참조**: `README.md`에 이미지를 삽입할 때는 상대 경로를 사용하며 적절한 대체 텍스트(alt text)를 포함합니다.

## 3. 커밋 가이드라인 (Commit Guidelines)
- **Conventional Commits 준수**: 모든 변경 사항은 아래의 프리픽스를 사용하여 커밋 메시지를 작성합니다.
  - `feat:`: 새로운 섹션이나 기능 추가
  - `docs:`: `README.md`나 `GEMINI.md` 등 문서 수정
  - `fix:`: 오타 수정이나 잘못된 링크 수정
- **자동 푸시**: 문서 작업이 완료되면 사용자에게 확인 후 또는 워크플로우에 따라 원격 저장소(`main` 브랜치)에 푸시합니다.

## 4. 발표 준비 최우선
- 모든 작업은 "팀원들에게 Gemini CLI를 효과적으로 소개한다"는 목적에 부합해야 합니다.
