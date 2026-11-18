# EGM OS

Un mini "OS" en Python avec 4 options au demarrage :

1. **EGM Download** - gestionnaire de telechargements integre
2. **Lecteur Multimedia** - mp4, mp3, m4v, wav, vob, mov, mkv, avi, ogg
3. **Navigateur Web** - navigation avec barre d'adresse
4. **Telechargeur Video** - capture des videos depuis le web (style downloadhelper.net)

## Installation (Windows / Linux)

```
pip install -r requirements.txt
python main.py
```

## Notes

- **Lecteur** : pour la lecture encaastree, installez aussi VLC
  (https://www.videolan.org) et `pip install python-vlc`.
  Sans VLC, le fichier s'ouvre avec le lecteur par defaut du systeme.
- **Navigateur** : pour un navigateur integre complet, `pip install pywebview`.
  Sinon les pages s'ouvrent dans votre navigateur systeme.
- **Telechargeur** : necessite `yt-dlp` (installe via requirements.txt).

## Android

Installez l'application **Pydroid 3** depuis le Play Store, copiez le dossier
`egm-os` sur le telephone, ouvrez `main.py` dans Pydroid 3 et lancez-le.
Le lanceur, le lecteur (mode systeme) et le telechargeur fonctionnent ;
le navigateur integre necessite pywebview (installable depuis Pydroid 3).
