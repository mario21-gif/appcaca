#!/bin/bash
# ============================================
#  EGM OS - Creer l'executable Linux
#  Lancer avec :  bash creer-exe-linux.sh
# ============================================
set -e

echo "Installation des outils de creation..."
pip install pyinstaller yt-dlp

echo "Creation de l'executable EGM-OS ..."
pyinstaller --onefile --windowed --name EGM-OS main.py

echo "Termine ! Votre fichier se trouve dans le dossier dist/."
echo "Rendez-le lancable avec :  chmod +x dist/EGM-OS"
