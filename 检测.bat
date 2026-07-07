@echo off
chcp 65001 > nul
set "PYTHON_PROJECT=C:\Users\10717\PycharmProjects\卡邮件"

REM 检查虚拟环境
if not exist "%PYTHON_PROJECT%\.venv\Scripts\activate.bat" (
    echo 错误：虚拟环境不存在于以下路径：
    echo %PYTHON_PROJECT%\.venv
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call "%PYTHON_PROJECT%\.venv\Scripts\activate.bat"

REM 运行脚本（用 ow_main.exe 运行，任务管理器里显示为 ow_main）
echo 正在运行脚本...
cd /d "%PYTHON_PROJECT%"
.venv\Scripts\python.exe close_wegame.py start

echo 执行完成
pause