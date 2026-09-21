@echo off
chcp 65001 >nul
title Vault Web - 手动启动
echo ========================================
echo   Vault Web 手动启动器
echo ========================================
echo.

set VAULT_ROOT=C:\WorkBuddy\EveryDayPaper
set PORT=4177
set VAULT_WEB_HOST=0.0.0.0
set VAULT_WEB_TOKEN=78366bbaff9a7461e2013a7e26a48e4eb879c2e4a2a9cc82a1fe1f83b077f7d8
set VAULT_WEB_THEME_FILE=C:\WorkBuddy\EveryDayPaper\.obsidian\plugins\vault-web-launcher\vault-web\theme.json

cd /d "C:\WorkBuddy\EveryDayPaper\.obsidian\plugins\vault-web-launcher\vault-web"

echo [1/2] 检查 node.exe ...
if not exist "C:\Program Files\nodejs\node.exe" (
  echo   [错误] 未找到 C:\Program Files\nodejs\node.exe
  echo   请先安装 Node.js 后再运行本脚本。
  pause
  exit /b 1
)
echo   已找到 node.exe
echo.
echo [2/2] 启动 Vault Web 服务器 (监听 0.0.0.0:%PORT%) ...
echo.
echo   本机访问   : http://127.0.0.1:%PORT%/?token=%VAULT_WEB_TOKEN%
echo   远程访问   : http://100.77.158.38:%PORT%/?token=%VAULT_WEB_TOKEN%
echo.
echo   关闭此窗口 = 停止服务器
echo ========================================
echo.

"C:\Program Files\nodejs\node.exe" server.js

echo.
echo 服务器已退出。
pause
