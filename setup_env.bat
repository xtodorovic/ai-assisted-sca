@echo off

:: Create virtual environment
python -m venv venv

:: Activate environment
call venv\Scripts\activate

:: Upgrade pip
pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt

echo ✅ Virtual environment is ready.
