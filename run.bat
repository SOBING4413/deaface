@echo off
title Deface Tool Suite v3.0 - NO ADMIN NEEDED
color 0A
chcp 65001 >nul

echo ========================================
echo DEFACE TOOL v3.0 - AUTHORIZED PENTEST
echo NO ADMIN REQUIRED - READY TO DEPLOY!
echo ========================================
echo.

REM Quick structure check
if not exist "main.py" (
    echo [ERROR] Run from PROJECT FOLDER!
    echo [FIX] Put all files in one folder first
    pause
    exit /b
)

REM Install dependencies (silent)
echo [1/3] Installing modules...
pip install -r requirements.txt --quiet --upgrade >nul 2>&1

REM Create folders
if not exist "modules" mkdir modules
if not exist "assets" mkdir assets

REM Quick payload prep
echo [2/3] Preparing payloads...
echo ^<?php echo "READY"; ?^> > assets\shell.php 2>nul
echo HACKED > assets\banner.jpg 2>nul

echo [3/3] Launching attack...
echo.
echo ++++++++++++++++++++++++++++++++++++++++++++++++
python main.py
echo ++++++++++++++++++++++++++++++++++++++++++++++++
echo.
echo [TOOLS READY]:
echo 1. verify_deface.py  - Check live shells
echo 2. persist.py       - Root persistence  
echo 3. Run again? Type: python main.py
echo.
pause