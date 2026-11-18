#!/bin/bash
# ============================================
#  EGM OS - Creer l'application Android (.apk)
#  A lancer sur Linux (ou WSL sur Windows) :
#  bash creer-apk.sh
# ============================================
set -e

echo "1/4 - Installation des outils systeme (plusieurs minutes)..."
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake

echo "2/4 - Installation de Buildozer..."
pip install buildozer cython==0.29.33

echo "3/4 - Preparation du dossier de build Android..."
buildozer init 2>/dev/null || true

echo "4/4 - Creation de l'APK (tres long la premiere fois : 30 min a 1 h)..."
buildozer android debug

echo ""
echo "Termine ! Votre application se trouve ici :"
echo "  bin/egmos-1.0-arm64-v8a_armeabi-v7a-debug.apk"
echo "Copiez ce fichier sur votre telephone et ouvrez-le pour l'installer."
echo "(Pensez a autoriser 'Installer des applications inconnues' sur Android.)"
