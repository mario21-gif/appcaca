"""
EGM OS - Lecteur Multimedia
Formats : mp4, mp3, m4v, wav, vob, mov, mkv, avi, ogg
Utilise python-vlc s'il est installe (lecture encastree), sinon ouvre le
fichier avec le lecteur par defaut du systeme.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

BG = "#0f1420"
FG = "#e8ecf4"
ACCENT = "#1e88e5"
CARD = "#1a2233"

FORMATS = [
    ("Fichiers multimedia", "*.mp4 *.mp3 *.m4v *.wav *.vob *.mov *.mkv *.avi *.ogg *.mpg *.mpeg *.webm *.flac *.aac"),
    ("Tous les fichiers", "*.*"),
]

try:
    import vlc  # type: ignore
    HAS_VLC = True
except Exception:
    HAS_VLC = False


def open_with_system(path: str) -> None:
    """Ouvre le fichier avec le lecteur par defaut."""
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


class PlayerWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.vlc_player = None
        self.vlc_media = None

        root.title("EGM OS - Lecteur Multimedia")
        root.geometry("820x560")
        root.minsize(600, 420)
        root.configure(bg=BG)

        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", pady=(14, 8), padx=16)
        tk.Button(top, text="Ouvrir un fichier", command=self.pick_file,
                  bg=ACCENT, fg="white", relief="flat",
                  font=("Segoe UI", 11, "bold"), padx=14, pady=6).pack(side="left")

        status = ("Lecture encaastree (python-vlc)" if HAS_VLC
                  else "python-vlc non installe : ouverture avec le lecteur du systeme")
        tk.Label(top, text=status, bg=BG,
                 fg="#9aa5b8", font=("Segoe UI", 9)).pack(side="right")

        self.file_label = tk.Label(root, text="Aucun fichier charge", bg=CARD,
                                   fg=FG, font=("Segoe UI", 10), anchor="w")
        self.file_label.pack(fill="x", padx=16, ipady=8)

        self.video_area = tk.Frame(root, bg="#000000", height=320)
        self.video_area.pack(fill="both", expand=True, padx=16, pady=10)
        self.video_area.pack_propagate(False)

        controls = tk.Frame(root, bg=BG)
        controls.pack(fill="x", padx=16, pady=(0, 14))
        for label, cmd in (("Play", self.play), ("Pause", self.pause),
                           ("Stop", self.stop)):
            tk.Button(controls, text=label, command=cmd, bg=CARD, fg=FG,
                      relief="flat", font=("Segoe UI", 11, "bold"),
                      padx=18, pady=6).pack(side="left", padx=(0, 8))

        if HAS_VLC:
            self.vlc_player = vlc.Instance()
        self.current_path = None

    def pick_file(self) -> None:
        path = filedialog.askopenfilename(title="Choisir un fichier multimedia",
                                          filetypes=FORMATS)
        if not path:
            return
        self.current_path = path
        self.file_label.configure(text=os.path.basename(path))
        if HAS_VLC and self.vlc_player is not None:
            self.vlc_media = self.vlc_player.media_new(path)
            self.play()
        else:
            open_with_system(path)

    def play(self) -> None:
        if not HAS_VLC or self.vlc_player is None:
            if self.current_path:
                open_with_system(self.current_path)
            return
        if self.vlc_media is None:
            messagebox.showinfo("Lecteur", "Ouvrez d'abord un fichier.")
            return
        self.vlc_media.parse()
        player = self.vlc_player.media_player_new()
        player.set_media(self.vlc_media)
        self._player = player
        self.root.after(300, lambda: self._attach_and_play(player))

    def _attach_and_play(self, player) -> None:
        if sys.platform.startswith("win"):
            player.set_hwnd(self.video_area.winfo_id())
        else:
            player.set_xwindow(self.video_area.winfo_id())
        player.play()

    def pause(self) -> None:
        if getattr(self, "_player", None):
            self._player.pause()

    def stop(self) -> None:
        if getattr(self, "_player", None):
            self._player.stop()

    def close(self) -> None:
        self.stop()


def run() -> None:
    root = tk.Tk()
    win = PlayerWindow(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (win.close(), root.destroy()))
    root.mainloop()
