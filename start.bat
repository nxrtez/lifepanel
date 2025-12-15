\
@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ============================================================
REM Life Dashboard - start script (single-user / Tailscale)
REM - Creates venv if missing
REM - Installs requirements
REM - Runs migrations
REM - Starts Django dev server bound to all interfaces
REM
REM Notes:
REM - For private Tailscale use, runserver is acceptable.
REM - For a public internet deployment, use a proper WSGI server.
REM ============================================================

cd /d "%~dp0"

if not exist venv (
  echo [*] Creating virtual environment...
  py -m venv venv
)

echo [*] Activating virtual environment...
call venv\Scripts\activate

echo [*] Upgrading pip...
py -m pip install --upgrade pip

echo [*] Installing requirements...
pip install -r requirements.txt

echo [*] Applying migrations...
py manage.py migrate

REM Optional: create admin user if none exists
REM py manage.py createsuperuser

echo [*] Starting server on http://0.0.0.0:8000
echo     (Use your Tailscale IP to access remotely)
py manage.py runserver 0.0.0.0:8000

endlocal
