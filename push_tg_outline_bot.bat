chcp 65001
set /p c=请输入commit:
git add .
git commit -m "%c%"
git push https://hxse:%hxse_github_token%@github.com/hxse/tg_outline_bot.git
pause