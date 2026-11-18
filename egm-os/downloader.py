"""
EGM OS - EGM Download / Telechargeur Video
Telecharge des videos depuis n'importe quel site (YouTube, Twitter, etc.)
en style "downloadhelper.net" :
  - collez l'URL de la page video
  - choisissez le format (MP4 video ou MP3 audio)
  - choisissez le dossier de destination
  - la progression s'affiche en direct

Necessite : pip install yt-dlp
"""

import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

BG = "#0f1420"
FG = "#e8ecf4"
ACCENT = "#1e88e5"
CARD = "#1a2233"
GREEN = "#2e9e5b"
RED = "#d64545"


def yt_dlp_available() -> bool:
    return shutil.which("yt-dlp") is not None or _importable("yt_dlp")


def _importable(module: str) -> bool:
    try:
        __import__(module)
        return True
    except Exception:
        return False


class DownloaderWindow:
    def __init__(self, root: tk.Tk, capture_mode: bool = False) -> None:
        self.root = root
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.downloading = False

        title = ("EGM Download" if not capture_mode
                 else "Telechargeur Video (style downloadhelper.net)")
        root.title("EGM OS - " + title)
        root.geometry("680x480")
        root.minsize(560, 420)
        root.configure(bg=BG)

        tk.Label(root, text=title, bg=BG, fg=FG,
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 4))
        tk.Label(root, text="Collez l'adresse de la page qui contient la video",
                 bg=BG, fg="#9aa5b8", font=("Segoe UI", 10)).pack()

        url_frame = tk.Frame(root, bg=BG)
        url_frame.pack(fill="x", padx=24, pady=(16, 6))
        tk.Label(url_frame, text="URL de la video", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.url_entry = tk.Entry(url_frame, bg=CARD, fg=FG, relief="flat",
                                  font=("Segoe UI", 11), insertbackground=FG)
        self.url_entry.pack(fill="x", ipady=9, pady=(4, 0))

        fmt_frame = tk.Frame(root, bg=BG)
        fmt_frame.pack(fill="x", padx=24, pady=6)
        self.format_var = tk.StringVar(value="mp4")
        tk.Label(fmt_frame, text="Format", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        row = tk.Frame(fmt_frame, bg=BG)
        row.pack(anchor="w", pady=(4, 0))
        for value, label in (("mp4", "MP4 (video)"), ("mp3", "MP3 (audio)"),
                             ("best", "Meilleure qualite")):
            tk.Radiobutton(row, text=label, variable=self.format_var,
                           value=value, bg=BG, fg=FG, selectcolor=CARD,
                           activebackground=BG, activeforeground=FG,
                           font=("Segoe UI", 10)).pack(side="left", padx=(0, 16))

        dir_frame = tk.Frame(root, bg=BG)
        dir_frame.pack(fill="x", padx=24, pady=6)
        tk.Label(dir_frame, text="Dossier de destination", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        dir_row = tk.Frame(dir_frame, bg=BG)
        dir_row.pack(fill="x", pady=(4, 0))
        self.dir_label = tk.Label(dir_row, text=self.folder, bg=CARD, fg=FG,
                                  anchor="w", relief="flat")
        self.dir_label.pack(side="left", fill="x", expand=True, ipady=7)
        tk.Button(dir_row, text="Parcourir", command=self.pick_folder,
                  bg=CARD, fg=FG, relief="flat", padx=12).pack(side="right",
                                                               padx=(8, 0))

        tk.Button(root, text="Telecharger", command=self.start_download,
                  bg=ACCENT, fg="white", relief="flat",
                  font=("Segoe UI", 13, "bold"), pady=8).pack(pady=14,
                                                              ipadx=30)

        self.progress = tk.DoubleVar(value=0.0)
        bar = tk.Frame(root, bg=BG)
        bar.pack(fill="x", padx=24)
        tk.Label(bar, text="Progression", bg=BG, fg=FG,
                 font=("Segoe UI", 9)).pack(anchor="w")
        tk.Scale(bar, variable=self.progress, from_=0, to=100, orient="horizontal",
                 bg=BG, fg=FG, highlightthickness=0, state="disabled",
                 troughcolor=CARD, sliderrelief="flat").pack(fill="x")

        self.status_label = tk.Label(root, text="", bg=BG, fg="#9aa5b8",
                                     font=("Segoe UI", 10), wraplength=600)
        self.status_label.pack(pady=(6, 12), padx=24)

        if not yt_dlp_available():
            self.status_label.configure(
                text="Outil de telechargement absent. Installez-le avec : "
                     "pip install yt-dlp",
                fg="#e0a63a")

    def pick_folder(self) -> None:
        folder = filedialog.askdirectory(title="Dossier de destination")
        if folder:
            self.folder = folder
            self.dir_label.configure(text=folder)

    def start_download(self) -> None:
        if self.downloading:
            return
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("EGM Download", "Collez d'abord une URL.")
            return
        if not yt_dlp_available():
            messagebox.showerror(
                "EGM Download",
                "L'outil yt-dlp n'est pas installe.\n"
                "Ouvrez un terminal et lancez :  pip install yt-dlp")
            return

        self.downloading = True
        self.progress.set(0)
        self.status_label.configure(text="Telechargement en cours...", fg="#9aa5b8")
        fmt = self.format_var.get()
        args = ["yt-dlp", "--newline", "--no-playlist", "-o",
                os.path.join(self.folder, "%(title)s.%(ext)s")]
        if fmt == "mp3":
            args += ["-x", "--audio-format", "mp3"]
        elif fmt == "mp4":
            args += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"]
        args.append(url)

        self._proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace")
        threading.Thread(target=self._read_output, daemon=True).start()

    def _read_output(self) -> None:
        assert self._proc.stdout is not None
        for line in self._proc.stdout:
            line = line.strip()
            if "[download]" in line and "%" in line:
                try:
                    pct = float(line.split("%")[0].split()[-1])
                    self.root.after(0, self.progress.set, pct)
                except ValueError:
                    pass
            elif line.startswith("ERROR"):
                self.root.after(0, lambda l=line: self.status_label.configure(
                    text=l, fg=RED))
        code = self._proc.wait()
        self.downloading = False

        def done() -> None:
            if code == 0:
                self.progress.set(100)
                self.status_label.configure(
                    text="Termine ! Fichier enregistre dans " + self.folder,
                    fg=GREEN)
            else:
                self.status_label.configure(
                    text="Echec du telechargement. Verifiez l'URL et votre "
                         "connexion.", fg=RED)
        self.root.after(0, done)


def run(capture_mode: bool = False) -> None:
    root = tk.Tk()
    DownloaderWindow(root, capture_mode=capture_mode)
    root.mainloop()
