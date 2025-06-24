@echo off
REM Exit immediately if any command fails
setlocal enabledelayedexpansion

REM Activate virtual environment
call .venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Collect static files
python manage.py collectstatic --no-input

REM Apply migrations
python manage.py migrate