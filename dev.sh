#!/bin/bash
# Mac에서 실행: 코드 push 후 Windows 서버 재시작
git add -A
git commit -m "${1:-update}"
git push
ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no user@100.64.99.31 \
  "powershell -ExecutionPolicy Bypass -File C:\\Users\\user\\board-game-ai\\restart.ps1"
echo "Done. http://100.64.99.31:7860"
