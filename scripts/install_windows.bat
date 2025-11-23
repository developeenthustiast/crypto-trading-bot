@echo off
REM ============================================
REM Crypto Trading Bot - Windows Installation Script
REM ============================================
REM This script will:
REM   1. Check Python version
REM   2. Create virtual environment
REM   3. Install Freqtrade and dependencies
REM   4. Set up configuration files
REM   5. Verify installation
REM ============================================

echo.
echo ========================================
echo  Crypto Trading Bot Setup
echo ========================================
echo.

REM Check if Python is installed
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Extract major.minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if not "%PYTHON_MAJOR%"=="3" (
    echo ERROR: Python 3.x required. You have Python %PYTHON_VERSION%
    pause
    exit /b 1
)

if %PYTHON_MINOR% LSS 10 (
    echo WARNING: Python 3.10 or higher recommended. You have Python %PYTHON_VERSION%
    echo Installation will continue but may have issues.
    timeout /t 5
)

echo [OK] Python %PYTHON_VERSION% detected
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Create virtual environment
echo [2/7] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo [5/7] Installing Freqtrade and dependencies...
echo This may take 5-10 minutes. Please be patient...
pip install -r freqtrade_setup\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo [OK] All dependencies installed
echo.

REM Set up .env file
echo [6/7] Setting up environment variables...
if not exist "freqtrade_setup\.env" (
    copy freqtrade_setup\.env.template freqtrade_setup\.env >nul
    echo [OK] Created .env file from template
    echo.
    echo IMPORTANT: You need to edit freqtrade_setup\.env and add your API keys!
    echo.
    echo To get Binance Testnet API keys:
    echo   1. Visit https://testnet.binance.vision/
    echo   2. Click "Generate HMAC_SHA256 Key"
    echo   3. Copy the API Key and Secret Key
    echo   4. Paste them into freqtrade_setup\.env
    echo.
) else (
    echo .env file already exists. Skipping creation.
    echo If you need a fresh template, delete freqtrade_setup\.env and run this script again.
)
echo.

REM Verify Freqtrade installation
echo [7/7] Verifying Freqtrade installation...
freqtrade --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Freqtrade not properly installed.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('freqtrade --version 2^>^&1') do set FREQTRADE_VERSION=%%i
echo [OK] %FREQTRADE_VERSION%
echo.

REM Success message
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Edit freqtrade_setup\.env with your Binance Testnet API keys
echo    Get keys from: https://testnet.binance.vision/
echo.
echo 2. Download historical data (15-20 minutes):
echo    python scripts\download_data.py
echo.
echo 3. Train the ML model (30-60 minutes):
echo    python scripts\train_model.py
echo.
echo 4. Run a backtest to verify (5 minutes):
echo    python scripts\backtest.py --period 3m
echo.
echo 5. Start the bot in dry-run mode:
echo    cd freqtrade_setup
echo    freqtrade trade --config config.json
echo.
echo 6. Open web dashboard (in another terminal):
echo    cd dashboard
echo    npm install
echo    npm run dev
echo.
echo For detailed instructions, see docs\SETUP_GUIDE.md
echo.
echo Virtual environment is still active.
echo To deactivate, type: deactivate
echo.
pause
