"""
EGM OS - Lanceur principal
Un mini bureau en Python avec 4 options :
  1. EGM Download (gestionnaire de telechargements integre)
  2. Lecteur multimedia (mp4, mp3, m4v, wav, vob, mov, mkv, avi, ogg)
  3. Navigateur web
  4. Telechargeur de videos (style downloadhelper.net)

Multiplateforme : Windows, Linux (et Android via Pydroid 3).
Lancez avec :  python main.py
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

BG = "#0f1420"
FG = "#e8ecf4"
ACCENT = "#1e88e5"
CARD = "#1a2233"
HOVER = "#243049"

TITLES = [
    ("1", "EGM Download", "Gestionnaire de telechargements integre", "download"),
    ("2", "Lecteur Multimedia", "mp4, mp3, m4v, wav, vob, mov, mkv, avi, ogg", "play"),
    ("3", "Navigateur Web", "Surfer sur Internet", "globe"),
    ("4", "Telechargeur Video", "Capturer des videos depuis le web", "capture"),
]


def open_module(choice: str) -> None:
    try:
        if choice == "download":
            import downloader
            downloader.run()
        elif choice == "play":
            import player
            player.run()
        elif choice == "globe":
            import browser
            browser.run()
        elif choice == "capture":
            import downloader
            downloader.run(capture_mode=True)
    except Exception as exc:  # Surface les erreurs dans l'UI
        messagebox.showerror("EGM OS", f"Impossible d'ouvrir ce module :\n{exc}")


def make_card(root: tk.Widget, num: str, title: str, subtitle: str, key: str) -> tk.Frame:
    card = tk.Frame(root, bg=CARD, highlightbackground=ACCENT, highlightthickness=0)
    card.pack(fill="x", padx=30, pady=9, ipady=6)

    num_lbl = tk.Label(card, text=num, bg=CARD, fg=ACCENT,
                       font=("Segoe UI", 20, "bold"), width=3)
    num_lbl.pack(side="left", padx=(18, 6))

    txt = tk.Frame(card, bg=CARD)
    txt.pack(side="left", fill="x", expand=True)
    tk.Label(txt, text=title, bg=CARD, fg=FG,
             font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x")
    tk.Label(txt, text=subtitle, bg=CARD, fg="#9aa5b8",
             font=("Segoe UI", 10), anchor="w").pack(fill="x")

    def on_enter(_event):
        card.configure(bg=HOVER, highlightthickness=1)
        for w in card.winfo_children():
            if isinstance(w, tk.Frame):
                for c in w.winfo_children():
                    c.configure(bg=HOVER)
            else:
                w.configure(bg=HOVER)

    def on_leave(_event):
        card.configure(bg=CARD, highlightthickness=0)
        for w in card.winfo_children():
            if isinstance(w, tk.Frame):
                for c in w.winfo_children():
                    c.configure(bg=CARD)
            else:
                w.configure(bg=CARD)

    def on_click(_event):
        open_module(key)

    for widget in (card, num_lbl, txt):
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)
    for w in txt.winfo_children():
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)

    return card


def run() -> None:
    root = tk.Tk()
    root.title("EGM OS")
    root.geometry("640x560")
    root.minsize(520, 480)
    root.configure(bg=BG)

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", pady=(28, 6))
    tk.Label(header, text="EGM OS", bg=BG, fg=FG,
             font=("Segoe UI", 26, "bold")).pack()
    tk.Label(header, text="Choisissez une option pour demarrer", bg=BG,
             fg="#9aa5b8", font=("Segoe UI", 11)).pack(pady=(4, 14))

    for num, title, subtitle, key in TITLES:
        make_card(root, num, title, subtitle, key)

    footer = tk.Frame(root, bg=BG)
    footer.pack(side="bottom", fill="x", pady=10)
    tk.Label(footer, text="EGM OS  -  Windows / Linux / Android (Pydroid 3)",
             bg=BG, fg="#5d6a80", font=("Segoe UI", 9)).pack()

    root.mainloop()


if __name__ == "__main__":
    run()
