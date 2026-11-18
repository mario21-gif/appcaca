@echo off
REM ============================================
REM  EGM OS - Creer l'executable Windows (.exe)
REM  Double-cliquez sur ce fichier.
REM ============================================
echo.
echo Installation des outils de creation...
pip install pyinstaller yt-dlp

echo.
echo Creation de l'executable EGM-OS.exe ...
pyinstaller --onefile --windowed --name EGM-OS main.py

echo.
echo Termine ! Votre fichier se trouve dans le dossier "dist".
echo (EGM-OS.exe - vous pouvez le copier partout sur Windows)
pause
