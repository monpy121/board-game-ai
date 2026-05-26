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

- **개발 머신**: 맥 (VS Code Remote SSH로 데스크탑에 접속해서 코딩)
- **실행 머신**: 데스크탑 (RTX 5080, VRAM 16GB, Windows)
- **원격 접속**: Tailscale VPN → SSH
- **Gradio 접속**: 맥 브라우저에서 `http://100.64.99.31:7860`

## 환경 정보 (설정 완료 — 재설치 불필요)

### 데스크탑
- OS: Windows, 사용자명: `user`
- Tailscale IP: `100.64.99.31`
- OpenSSH 서버: 실행 중 (자동시작 설정됨)
- SSH 인증: 키 방식 (맥 공개키 등록 완료)
  - 공개키 위치: `C:\ProgramData\ssh\administrators_authorized_keys`
  - `user` 계정이 관리자 그룹이라 이 경로 사용 (`~/.ssh/authorized_keys` 아님)
- conda 가상환경: `board-game-ai` (Python 3.11)
  - 위치: `C:\Users\user\anaconda3\envs\board-game-ai`
  - 설치된 패키지: torch 2.12.0, transformers 5.9.0, gradio 6.14.0, opencv-python 4.13.0, accelerate 1.13.0
- 프로젝트 경로: `C:\Users\user\board-game-ai`

### 맥
- Tailscale IP: `100.73.34.21`
- SSH 키: `~/.ssh/id_ed25519` (생성 완료)
- GitHub repo clone (최초 1회):
  ```bash
  git clone https://github.com/monpy121/board-game-ai.git
  ```

## Git 작업 흐름 (맥 ↔ 데스크탑 동기화)

> 맥과 데스크탑 양쪽에서 코드를 작업하므로 작업 전 pull, 작업 후 push 습관 필요.

### 맥에서 작업할 때
```bash
cd board-game-ai
git pull                          # 작업 시작 전 항상
# ... 코딩 ...
git add .
git commit -m "작업 내용"
git push
```

### 데스크탑에서 받을 때
```powershell
cd C:\Users\user\board-game-ai
git pull
```

### 데스크탑에서 작업 후 올릴 때
```powershell
cd C:\Users\user\board-game-ai
git add .
git commit -m "작업 내용"
git push
```

## "SSH 켜줘" 명령 시 체크리스트

> 유저가 "SSH 켜줘"라고 하면 아래 순서로 상태 확인 후 안내. 이미 설정된 것은 재설치하지 말 것.

1. **데스크탑 OpenSSH 서비스 상태 확인**
   ```powershell
   Get-Service sshd
   ```
   - Running이면 OK, 아니면 `Start-Service sshd` (관리자 PowerShell 필요)

2. **Tailscale 연결 상태 확인**
   ```powershell
   & "C:\Program Files\Tailscale\tailscale.exe" status
   ```
   - 맥 IP(`100.73.34.21`)가 보이면 OK

3. **맥에서 접속 안내**
   ```bash
   ssh user@100.64.99.31
   ```

4. **SSH 접속 후 개발 환경 활성화**
   ```powershell
   cd C:\Users\user\board-game-ai
   # python 실행 시 가상환경 직접 지정
   C:\Users\user\anaconda3\envs\board-game-ai\Scripts\python.exe <파일명>.py
   ```

## 프로젝트 구조

```
board-game-ai/
├── CLAUDE.md
├── requirements.txt
├── test_connection.py       # Gradio 연결 테스트용
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
- [x] 데스크탑 Tailscale + OpenSSH 설정
- [x] 맥 Tailscale 설치 및 연결
- [x] 맥 → 데스크탑 SSH 키 방식 접속 설정 완료
- [x] conda 가상환경 생성 및 패키지 설치 완료
- [ ] test_connection.py 실행 및 Gradio UI 동작 확인
- [ ] Qwen2-VL 모델 로드 및 테스트
- [ ] UNO 규칙 DB 작성
- [ ] 카메라 실시간 인식 구현
- [ ] 이벤트 감지 로직 구현
- [ ] Gradio UI 구현

## 데모 게임

**UNO** - 첫 번째 구현 대상
