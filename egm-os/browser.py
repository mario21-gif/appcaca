"""
EGM OS - Navigateur Web
Utilise pywebview s'il est installe (vraie fenetre de navigation avec barre
d'adresse), sinon ouvre l'adresse dans le navigateur par defaut du systeme.
"""

import sys
import threading
import tkinter as tk
from tkinter import messagebox
import webbrowser

BG = "#0f1420"
FG = "#e8ecf4"
ACCENT = "#1e88e5"
CARD = "#1a2233"

try:
    import webview  # type: ignore
    HAS_WEBVIEW = True
except Exception:
    HAS_WEBVIEW = False

HOME_URL = "https://www.google.com"


def normalize_url(text: str) -> str:
    text = text.strip()
    if not text:
        return HOME_URL
    if text.startswith("http://") or text.startswith("https://"):
        return text
    if " " not in text and "." in text:
        return "https://" + text
    return "https://duckduckgo.com/?q=" + text.replace(" ", "+")


def launch_webview(url: str) -> None:
    window = webview.create_window("EGM OS - Navigateur", url, width=1100, height=700)
    webview.start(window)


class TkBrowser:
    """Navigateur de secours en pur Tkinter : barre d'adresse + navigation
    dans le navigateur systeme (aucune dependance requise)."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.history: list[str] = []
        root.title("EGM OS - Navigateur Web")
        root.geometry("640x300")
        root.minsize(520, 240)
        root.configure(bg=BG)

        tk.Label(root, text="Adresse ou recherche", bg=BG, fg=FG,
                 font=("Segoe UI", 12, "bold")).pack(pady=(18, 6))

        bar = tk.Frame(root, bg=BG)
        bar.pack(fill="x", padx=24)
        self.entry = tk.Entry(bar, bg=CARD, fg=FG, insertbackground=FG,
                              relief="flat", font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entry.insert(0, HOME_URL)
        self.entry.bind("<Return>", lambda _e: self.go())

        tk.Button(bar, text="Aller", command=self.go, bg=ACCENT, fg="white",
                  relief="flat", font=("Segoe UI", 11, "bold"),
                  padx=16).pack(side="right")

        self.status = tk.Label(root, text="", bg=BG, fg="#9aa5b8",
                               font=("Segoe UI", 9))
        self.status.pack(side="bottom", pady=10)

        note = ("pywebview non installe : les pages s'ouvrent dans votre "
                "navigateur systeme.\nInstallez pywebview pour un navigateur "
                "integre complet.")
        tk.Label(root, text=note, bg=BG, fg="#5d6a80",
                 font=("Segoe UI", 9), justify="center").pack(pady=16)

    def go(self) -> None:
        url = normalize_url(self.entry.get())
        self.history.append(url)
        webbrowser.open_new_tab(url)
        self.status.configure(text="Ouvert : " + url)


def run() -> None:
    if HAS_WEBVIEW:
        launch_webview(HOME_URL)
        return
    root = tk.Tk()
    TkBrowser(root)
    root.mainloop()
