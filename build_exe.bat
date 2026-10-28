@echo off
REM Builds dist\HeroScore\HeroScore.exe. Zip the whole dist\HeroScore folder to share it.
cd /d "%~dp0"
python -m PyInstaller --noconfirm --windowed --name HeroScore --icon logo_ico.ico --collect-all customtkinter system.py
if errorlevel 1 exit /b 1
xcopy "match" "dist\HeroScore\match\" /E /I /Y >nul
xcopy "rules" "dist\HeroScore\rules\" /E /I /Y >nul
copy /Y "logo_ico.ico" "dist\HeroScore\" >nul
copy /Y "football pitch.jpg" "dist\HeroScore\" >nul
echo Build finished: dist\HeroScore\HeroScore.exe
