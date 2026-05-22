  
@echo off
setlocal

REM Set PostgreSQL bin path - change if needed
set PGPATH=C:\Program Files\PostgreSQL\15\bin

REM Set backup directory
set BACKUP_DIR=C:\Users\JAYASH\Desktop\dinesh_gaikwad\backups

REM Create backup folder if not exists
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Get current date for filename
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set TIMESTAMP=%mydate%_%mytime%

REM Database credentials - match your .env
set DB_NAME=entreskill_db
set DB_USER=postgres

REM Run pg_dump
"%PGPATH%\pg_dump.exe" -U %DB_USER% -F c -b -v -f "%BACKUP_DIR%\entreskill_%TIMESTAMP%.backup" %DB_NAME%

echo Backup completed: %BACKUP_DIR%\entreskill_%TIMESTAMP%.backup
pause