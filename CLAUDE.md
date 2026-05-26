# Board Game AI Assistant

보드 게임 규칙을 실시간으로 도와주는 AI. 게임을 이기는 법이 아닌 규칙에 맞게 진행할 수 있도록 돕는 것이 목적.

## 핵심 기능

1. **규칙 학습** - 유명 게임은 사전 입력, 기타 게임은 설명서 이미지 OCR로 규칙 추출
2. **실시간 인식** - 카메라로 게임판/카드/말을 실시간 인식
3. **이벤트 감지** - 게임 중 발생하는 이벤트 및 영향 안내
4. **다음 진행 안내** - 현재 상황에서 가능한 선택지 안내
5. **규칙 위반 감지** - 규칙에 어긋나는 진행 시 알림
6. **카드/말 설명** - 플레이어가 보고 있는 카드/말의 능력 및 역할 설명

## 기술 스택

- **모델**: Qwen2-VL-7B-Instruct (HuggingFace, 로컬 실행)
- **OCR**: microsoft/trocr-large-printed
- **UI**: Gradio
- **비디오**: OpenCV
- **언어**: Python

## 실행 환경

- **개발**: MacBook
- **실행**: Windows Desktop (RTX 5080, VRAM 16GB)
- **원격 접속**: Tailscale VPN → 맥 브라우저에서 `http://<tailscale-ip>:7860` 접속

## 프로젝트 구조

```
board-game-ai/
├── CLAUDE.md
├── requirements.txt
├── test_connection.py       # Tailscale 연결 테스트용
├── main.py                  # 앱 진입점
├── models/
│   ├── vision.py            # Qwen2-VL 실시간 인식
│   └── ocr.py               # TrOCR 설명서 파싱
├── rules/
│   ├── preloaded/           # 사전 입력 게임 규칙 (UNO 등)
│   │   └── uno.py
│   └── parser.py            # OCR 결과 → 규칙 구조화
├── game/
│   ├── state.py             # 현재 게임 상태 추적
│   └── events.py            # 이벤트 감지 및 규칙 위반 체크
└── ui/
    └── app.py               # Gradio UI
```

## 현재 진행 상황

- [x] 기획 및 아키텍처 확정
- [x] 연결 테스트 코드 작성 (test_connection.py)
- [ ] Tailscale 설치 및 연결 테스트
- [ ] Qwen2-VL 모델 로드 및 테스트
- [ ] UNO 규칙 DB 작성
- [ ] 카메라 실시간 인식 구현
- [ ] 이벤트 감지 로직 구현
- [ ] Gradio UI 구현

## 데모 게임

**UNO** - 첫 번째 구현 대상

## 개발 워크플로우

1. Mac에서 코드 작성 → `git push`
2. Windows에서 `git pull` → `python main.py` 실행
3. Mac 브라우저에서 Tailscale IP로 접속하여 테스트

## 경로

- **Mac**: `/Users/chaeseunghun/board-game-ai`
- **Windows**: `C:\Projects\board-game-ai`
