#!/bin/bash
# Mac에서 실행: 코드 push 후 Windows에서 실행 + 출력 확인
git pull --rebase
git add -A
git commit -m "${1:-update}"
git push
ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no user@100.64.99.31 \
  "cd C:\\Users\\user\\board-game-ai && git pull && C:\\Users\\user\\anaconda3\\envs\\board-game-ai\\python.exe main.py"
