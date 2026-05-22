  
@echo off
echo ========================================
echo EntreSkill Hub - Test Runner
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate

REM Check if Redis is running
redis-cli ping >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Redis is not running. Start Redis first.
    pause
    exit /b 1
)

REM Run migrations check
echo Checking migrations...
python manage.py makemigrations --check --dry-run
if %errorlevel% neq 0 (
    echo ERROR: Unapplied migrations found
    pause
    exit /b 1
)

REM Run Django tests
echo Running Django tests...
python manage.py test --verbosity=2

REM Check static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Check Celery connection
echo Checking Celery...
celery -A config inspect ping >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Celery worker not running
) else (
    echo Celery worker is running
)

REM Security check
echo Running security checks...
python manage.py check --deploy

echo ========================================
echo All tests completed
echo ========================================
pause