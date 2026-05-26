Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
cd C:\Users\user\board-game-ai
git pull
Start-Process -FilePath 'C:\Users\user\anaconda3\envs\board-game-ai\python.exe' -ArgumentList 'main.py' -WorkingDirectory 'C:\Users\user\board-game-ai' -WindowStyle Hidden
Write-Host 'Server restarted'
