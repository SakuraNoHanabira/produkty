@echo off
echo ===============================
echo Instalator bibliotek Python
echo ===============================

:: Sprawdź, czy Python jest zainstalowany
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  Python nie jest zainstalowany lub nie dodano go do PATH.
    echo    Pobierz go ze strony: https://www.python.org/downloads/
    pause
    exit /b
)

:: Instaluj potrzebne biblioteki
echo  Instalowanie bibliotek: selenium, requests, webdriver-manager...
pip install selenium requests webdriver-manager

echo.
echo  Gotowe! Wszystkie biblioteki zostały zainstalowane.
pause
