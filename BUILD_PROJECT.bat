@echo off
echo ============================================================
echo   FINANCIAL COMPLAINT INTELLIGENCE SYSTEM - ANDROID APP
echo   Full Project Builder
echo ============================================================
echo.

:: ─────────────────────────────────────────────
:: STEP 1: CHECK PREREQUISITES
:: ─────────────────────────────────────────────
echo [STEP 1/8] Checking prerequisites...

where java >nul 2>&1
if errorlevel 1 (
    echo ERROR: Java JDK not found. Install JDK 17+ from https://adoptium.net/
    pause & exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.9+ from https://python.org/
    pause & exit /b 1
)

where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Install from https://git-scm.com/
    pause & exit /b 1
)

echo [OK] Java, Python, Git found.

:: ─────────────────────────────────────────────
:: STEP 2: CREATE DIRECTORY STRUCTURE
:: ─────────────────────────────────────────────
echo.
echo [STEP 2/8] Creating project directory structure...

set ROOT=FinancialComplaintAI
mkdir %ROOT%
mkdir %ROOT%\backend
mkdir %ROOT%\backend\app
mkdir %ROOT%\backend\app\api
mkdir %ROOT%\backend\app\core
mkdir %ROOT%\backend\app\models
mkdir %ROOT%\backend\app\services
mkdir %ROOT%\backend\data
mkdir %ROOT%\android
mkdir %ROOT%\android\app
mkdir %ROOT%\android\app\src
mkdir %ROOT%\android\app\src\main
mkdir %ROOT%\android\app\src\main\java\com\fcis\app
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\ui\screens
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\ui\theme
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\viewmodel
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\data\model
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\data\repository
mkdir %ROOT%\android\app\src\main\java\com\fcis\app\data\network
mkdir %ROOT%\android\app\src\main\res\layout
mkdir %ROOT%\android\app\src\main\res\values
mkdir %ROOT%\android\app\src\main\res\drawable

echo [OK] Directory structure created.

:: ─────────────────────────────────────────────
:: STEP 3: GENERATE BACKEND FILES
:: ─────────────────────────────────────────────
echo.
echo [STEP 3/8] Generating backend (FastAPI + RAG) files...

python generate_backend.py %ROOT%\backend
if errorlevel 1 (
    echo ERROR: Backend generation failed.
    pause & exit /b 1
)

echo [OK] Backend files generated.

:: ─────────────────────────────────────────────
:: STEP 4: GENERATE ANDROID FILES
:: ─────────────────────────────────────────────
echo.
echo [STEP 4/8] Generating Android (Kotlin + Jetpack Compose) files...

python generate_android.py %ROOT%\android
if errorlevel 1 (
    echo ERROR: Android generation failed.
    pause & exit /b 1
)

echo [OK] Android files generated.

:: ─────────────────────────────────────────────
:: STEP 5: SETUP PYTHON VIRTUAL ENV
:: ─────────────────────────────────────────────
echo.
echo [STEP 5/8] Setting up Python virtual environment...

cd %ROOT%\backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..\..

echo [OK] Python environment ready.

:: ─────────────────────────────────────────────
:: STEP 6: DOWNLOAD SAMPLE DATA
:: ─────────────────────────────────────────────
echo.
echo [STEP 6/8] Setting up sample complaint data...

python setup_sample_data.py %ROOT%\backend\data
echo [OK] Sample data ready.

:: ─────────────────────────────────────────────
:: STEP 7: BUILD FAISS INDEX
:: ─────────────────────────────────────────────
echo.
echo [STEP 7/8] Building FAISS vector index...

cd %ROOT%\backend
call venv\Scripts\activate
python -m app.services.index_builder
cd ..\..

echo [OK] FAISS index built.

:: ─────────────────────────────────────────────
:: STEP 8: INSTRUCTIONS
:: ─────────────────────────────────────────────
echo.
echo [STEP 8/8] Final setup complete!
echo.
echo ============================================================
echo   NEXT STEPS:
echo ============================================================
echo.
echo   1. START BACKEND SERVER:
echo      cd %ROOT%\backend
echo      venv\Scripts\activate
echo      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo   2. OPEN ANDROID PROJECT:
echo      Open Android Studio → %ROOT%\android
echo      Wait for Gradle sync → Run on emulator/device
echo.
echo   3. API DOCS (when server is running):
echo      http://localhost:8000/docs
echo.
echo ============================================================
pause
