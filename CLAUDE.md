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

## "맥 Git 설정해줘" 명령 시 체크리스트

> 맥에서 처음 GitHub 연동할 때 아래 순서로 진행. 이미 된 항목은 건너뜀.

1. **GitHub SSH 연결 확인**
   ```bash
   ssh -T git@github.com
   ```
   - `Hi monpy121!` 메시지 나오면 OK → 3번으로
   - 실패하면 2번으로

2. **GitHub SSH 키 등록** (미연결 시)
   ```bash
   # 기존 SSH 공개키 확인
   cat ~/.ssh/id_ed25519.pub
   ```
   - 출력된 공개키를 GitHub → Settings → SSH and GPG keys → New SSH key에 등록
   - 등록 후 1번 다시 확인

3. **git 사용자 정보 설정 확인**
   ```bash
   git config --global user.name
   git config --global user.email
   ```
   - 비어있으면:
     ```bash
     git config --global user.name "monpy121"
     git config --global user.email "seunghun1480@gmail.com"
     ```

4. **repo clone (최초 1회)**
   ```bash
   git clone git@github.com:monpy121/board-game-ai.git
   ```
   - 이미 clone 되어 있으면 생략

## Git 작업 흐름 (맥 ↔ 데스크탑 동기화)

> GitHub가 중간 저장소 역할. 맥 → GitHub → 데스크탑 순으로 전달됨.
> SSH는 dev.sh 실행 시에만 잠깐 연결되고 바로 끊김 (상시 연결 아님).

### 스크립트 정리

| 상황 | 명령 | 실행 위치 |
|------|------|-----------|
| 맥에서 작업 후 데스크탑에 배포 | `./dev.sh "메시지"` | 맥 |
| 데스크탑 작업 내용을 맥으로 받기 | `git pull --rebase` | 맥 |
| 데스크탑에서 작업 후 GitHub에 올리기 | `.\push.ps1 "메시지"` | 데스크탑 |

### dev.sh 동작 순서 (맥 → 데스크탑)
```
1. git pull --rebase  (GitHub에서 데스크탑 작업 내용 먼저 받음)
2. git add -A + commit + push  (맥 작업 내용 GitHub에 올림)
3. SSH로 데스크탑 접속 → git pull → main.py 실행 → SSH 끊김
```

### 데스크탑에서 작업 후 맥으로 보내기
```powershell
# 데스크탑에서
.\push.ps1 "작업 내용"   # GitHub에 올림
```
```bash
# 맥에서
git pull --rebase        # GitHub에서 받아옴
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
├── dev.sh                   # 맥 → 데스크탑 배포 (push + SSH pull + 실행)
├── push.ps1                 # 데스크탑 → GitHub push
├── restart.ps1              # 데스크탑 서버 재시작
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

---

## 설계 확정 내용 (2026-05-27)

### 1. 규칙 데이터 시스템

| 게임 유형 | 규칙 입력 방식 |
|-----------|---------------|
| 유명 게임 (UNO 등) | 직접 텍스트 작성 → `rules/preloaded/` |
| 기타 게임 | 설명서 이미지 업로드 → TrOCR OCR → 텍스트 추출 |

- 게임 선택 시 preloaded 여부 자동 판단 (`game_registry.py`에서 관리)

### 2. RAG 구성

- **벡터 DB**: ChromaDB (로컬 파일 저장, 간단한 API)
- **임베딩 모델**: `BAAI/bge-m3` (다국어 최고 성능, 한국어 지원, 로컬 실행)
- 게임별 ChromaDB 컬렉션으로 분리 저장
- 질의 → 관련 규칙 청크 검색 → Qwen2-VL에 컨텍스트로 전달 → 답변

### 3. 카드 인식 시스템

**인식 파이프라인:**
```
카메라 프레임
    ↓ (2초 간격 캡처)
OpenCV 전처리 (카드 영역 crop, 밝기/대비 보정, 원근 보정)
    ↓
Qwen2-VL → 카드 식별
    ↓
RAG에서 해당 카드 기능 설명 반환
```

**게임별 카드 인식 방식:**

| 게임 유형 | 방식 |
|-----------|------|
| 유명 게임 (UNO 등) | Qwen2-VL 사전 파인튜닝 (장시간, 고품질) |
| 기타 게임 | Reference 이미지 방식 (카드당 10장 내외 등록 → 프롬프트에 직접 첨부) |

> **파인튜닝 10장은 인식률 낮아서 채택 안 함.** 대신 등록한 이미지를 프롬프트 reference로 활용하는 방식이 더 robust함.

### 4. 확정 파일 구조

```
board-game-ai/
├── models/
│   ├── vision.py        # Qwen2-VL 카드 인식 (OpenCV 전처리 포함)
│   └── ocr.py           # TrOCR 설명서 파싱
├── rules/
│   ├── preloaded/
│   │   └── uno.py       # UNO 규칙 텍스트 (한국어)
│   ├── parser.py        # 이미지 → TrOCR → 텍스트
│   ├── rag.py           # ChromaDB + bge-m3 임베딩/검색
│   └── game_registry.py # 유명 게임 목록 (preloaded 여부 판단)
├── game/
│   ├── state.py         # 현재 게임 상태 추적
│   └── events.py        # 이벤트 감지 및 규칙 위반 체크
└── ui/
    └── app.py           # Gradio UI
```

### 5. 다음 코딩 순서

1. `rules/preloaded/uno.py` — UNO 규칙 텍스트 작성
2. `rules/game_registry.py` — 게임 목록 관리
3. `rules/rag.py` — ChromaDB + bge-m3 구성
4. `rules/parser.py` — TrOCR 설명서 파싱
5. `models/vision.py` — OpenCV 전처리 + Qwen2-VL 카드 인식
6. `game/state.py`, `game/events.py` — 게임 상태 및 이벤트
7. `ui/app.py` — Gradio UI 통합
