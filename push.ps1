param([string]$msg = "update")
cd C:\Users\user\board-game-ai
git pull --rebase
git add -A
git commit -m $msg
git push
Write-Host "Pushed to GitHub"
