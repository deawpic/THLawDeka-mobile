@echo off
setlocal
cd /d "%~dp0"
echo [THLawDeka-mobile] Starting FastAPI Gateway via uv...
uv run uvicorn main:app --host 127.0.0.1 --port 8000
if %errorlevel% neq 0 (
    echo [Fallback] uv failed, trying standard venv/python...
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    )
    python -m uvicorn main:app --host 127.0.0.1 --port 8000
)
endlocal
