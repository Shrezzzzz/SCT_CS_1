import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# ─── Colour palette ───────────────────────────────────────────────────────────
BG        = "#12121a"
PANEL     = "#1a1a26"
BORDER    = "#2a2a3a"
ACCENT_R  = "#ff4d4d"   # encrypt / red
ACCENT_G  = "#00c896"   # decrypt / teal
FG_MAIN   = "#e8e8f0"
FG_DIM    = "#6a6a8a"
FG_MONO   = "#c8ffc8"   # green monospace
FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


# ─── Core cipher ──────────────────────────────────────────────────────────────
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result


# ─── Rotor matrix ─────────────────────────────────────────────────────────────
def update_rotor_matrix():
    shift = get_shift()
    if shift is None:
        return
    plain  = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    cipher = " ".join(
        chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    plain_var.set(f"PLAIN:   {plain}")
    cipher_var.set(f"CIPHER:  {cipher}")
    rotor_status_var.set(f"ROT+{shift} ACTIVE")


# ─── Shift helpers ────────────────────────────────────────────────────────────
def get_shift():
    try:
        return int(shift_var.get())
    except ValueError:
        return None


def increment_shift():
    s = get_shift()
    if s is not None:
        shift_var.set(str((s + 1) % 26))
    update_rotor_matrix()
    update_char_count()


def decrement_shift():
    s = get_shift()
    if s is not None:
        shift_var.set(str((s - 1) % 26))
    update_rotor_matrix()
    update_char_count()


# ─── Char counter ─────────────────────────────────────────────────────────────
def update_char_count(event=None):
    text = message_entry.get("1.0", tk.END).rstrip("\n")
    char_count_var.set(f"{len(text)} chars")
    update_rotor_matrix()


# ─── Encrypt / Decrypt ────────────────────────────────────────────────────────
def encrypt():
    text = message_entry.get("1.0", tk.END).rstrip("\n")
    shift = get_shift()

    if not text.strip():
        messagebox.showwarning("Input Required", "Please enter a message.", parent=root)
        return
    if shift is None:
        messagebox.showerror("Invalid Shift", "Shift must be an integer.", parent=root)
        return

    result = caesar_cipher(text, shift)
    set_result(result, f"Encrypted · Shift {shift}")


def decrypt():
    text = message_entry.get("1.0", tk.END).rstrip("\n")
    shift = get_shift()

    if not text.strip():
        messagebox.showwarning("Input Required", "Please enter a message.", parent=root)
        return
    if shift is None:
        messagebox.showerror("Invalid Shift", "Shift must be an integer.", parent=root)
        return

    result = caesar_cipher(text, -shift)
    set_result(result, f"Decrypted · Shift {shift}")


def set_result(text, label):
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, text)
    result_box.config(state="disabled")
    result_status_var.set(label)


def clear_all():
    message_entry.delete("1.0", tk.END)
    shift_var.set("0")
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.config(state="disabled")
    result_status_var.set("")
    char_count_var.set("0 chars")
    update_rotor_matrix()


def copy_result():
    text = result_box.get("1.0", tk.END).strip()
    if not text:
        return
    try:
        if sys.platform == "darwin":
            subprocess.run("pbcopy", input=text.encode(), check=True)
        elif sys.platform == "win32":
            subprocess.run("clip", input=text.encode(), check=True, shell=True)
        else:
            # Linux — try xclip, fall back to xsel
            try:
                subprocess.run(["xclip", "-selection", "clipboard"],
                               input=text.encode(), check=True)
            except FileNotFoundError:
                subprocess.run(["xsel", "--clipboard", "--input"],
                               input=text.encode(), check=True)
        copy_btn.config(text="  Copied!")
        root.after(1500, lambda: copy_btn.config(text="  Copy result"))
    except Exception:
        # Last resort: show text in a dialog so user can copy manually
        messagebox.showinfo("Copy Result", text, parent=root)


# ─── Reusable widget helpers ──────────────────────────────────────────────────
def make_panel(parent, **kwargs):
    return tk.Frame(parent, bg=PANEL, highlightbackground=BORDER,
                    highlightthickness=1, **kwargs)


def label(parent, text, font=None, fg=FG_MAIN, bg=PANEL, **kwargs):
    return tk.Label(parent, text=text, font=font or FONT_UI,
                    fg=fg, bg=bg, **kwargs)


# ══════════════════════════════════════════════════════════════════════════════
# ROOT WINDOW
# ══════════════════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("CIPHER//DECK HUD")
root.geometry("780x720")
root.resizable(False, False)
root.configure(bg=BG)

# ─── Top bar ──────────────────────────────────────────────────────────────────
topbar = tk.Frame(root, bg="#0d0d14", height=42)
topbar.pack(fill="x")
topbar.pack_propagate(False)

tk.Label(topbar, text="⬡  CIPHER//DECK HUD", font=("Courier New", 11, "bold"),
         fg=ACCENT_R, bg="#0d0d14").pack(side="left", padx=16, pady=10)

tk.Label(topbar, text="CAESAR CIPHER  ·  ASCII STANDARD",
         font=FONT_MONO, fg=FG_DIM, bg="#0d0d14").pack(side="right", padx=16)

# ─── Main content area ────────────────────────────────────────────────────────
content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=24, pady=16)

# ─── Header card ──────────────────────────────────────────────────────────────
header = make_panel(content)
header.pack(fill="x", pady=(0, 10))

hinner = tk.Frame(header, bg=PANEL)
hinner.pack(fill="x", padx=14, pady=10)

icon_lbl = tk.Label(hinner, text="⬡", font=("Courier New", 20), fg=ACCENT_R, bg=PANEL)
icon_lbl.grid(row=0, column=0, rowspan=2, padx=(0, 12))

tk.Label(hinner, text="Caesar Cipher  ●", font=("Segoe UI", 14, "bold"),
         fg=FG_MAIN, bg=PANEL).grid(row=0, column=1, sticky="w")
tk.Label(hinner, text="Encrypt and decrypt text with a shift value",
         font=FONT_UI, fg=FG_DIM, bg=PANEL).grid(row=1, column=1, sticky="w")

algo_badge = tk.Label(hinner, text="● ALGORITHM: ROT-N // ASCII STANDARD",
                      font=("Courier New", 8, "bold"), fg=ACCENT_R, bg="#2a0a0a",
                      padx=8, pady=3)
algo_badge.grid(row=0, column=2, sticky="e", padx=(20, 0))
hinner.columnconfigure(2, weight=1)

# ─── Rotor matrix panel ───────────────────────────────────────────────────────
rotor_panel = make_panel(content)
rotor_panel.pack(fill="x", pady=(0, 10))

rotor_top = tk.Frame(rotor_panel, bg=PANEL)
rotor_top.pack(fill="x", padx=14, pady=(8, 2))

tk.Label(rotor_top, text="↻  ROTOR MAPPING MATRIX (A–Z)",
         font=("Courier New", 9, "bold"), fg=ACCENT_G, bg=PANEL).pack(side="left")

rotor_status_var = tk.StringVar(value="ROT+7 ACTIVE")
tk.Label(rotor_top, textvariable=rotor_status_var,
         font=("Courier New", 9, "bold"), fg=ACCENT_G, bg=PANEL).pack(side="right")

plain_var  = tk.StringVar()
cipher_var = tk.StringVar()

tk.Label(rotor_panel, textvariable=plain_var, font=("Courier New", 9),
         fg=FG_DIM, bg=PANEL, anchor="w").pack(fill="x", padx=14, pady=1)
tk.Label(rotor_panel, textvariable=cipher_var, font=("Courier New", 9),
         fg=ACCENT_R, bg=PANEL, anchor="w").pack(fill="x", padx=14, pady=(1, 8))

# ─── Message input panel ──────────────────────────────────────────────────────
msg_panel = make_panel(content)
msg_panel.pack(fill="x", pady=(0, 10))

msg_top = tk.Frame(msg_panel, bg=PANEL)
msg_top.pack(fill="x", padx=14, pady=(8, 4))

tk.Label(msg_top, text="⇄  MESSAGE [INPUT STREAM]",
         font=("Courier New", 9, "bold"), fg=ACCENT_G, bg=PANEL).pack(side="left")

char_count_var = tk.StringVar(value="0 chars")
tk.Label(msg_top, textvariable=char_count_var,
         font=FONT_MONO, fg=FG_DIM, bg=PANEL).pack(side="right")

message_entry = tk.Text(msg_panel, height=5, font=("Courier New", 11),
                        bg="#0f0f1a", fg=FG_MAIN, insertbackground=FG_MAIN,
                        relief="flat", padx=10, pady=8,
                        highlightbackground=BORDER, highlightthickness=1)
message_entry.pack(fill="x", padx=14, pady=(0, 10))
message_entry.bind("<KeyRelease>", update_char_count)

# ─── Shift value panel ────────────────────────────────────────────────────────
shift_panel = make_panel(content)
shift_panel.pack(fill="x", pady=(0, 10))

shift_inner = tk.Frame(shift_panel, bg=PANEL)
shift_inner.pack(fill="x", padx=14, pady=10)

tk.Label(shift_inner, text="⇌  SHIFT VALUE  (KEY: N)",
         font=("Courier New", 9, "bold"), fg=ACCENT_G, bg=PANEL).grid(row=0, column=0, sticky="w")
tk.Label(shift_inner, text="Each letter moves N positions in the alphabet (e.g. A → D).",
         font=("Courier New", 8), fg=FG_DIM, bg=PANEL).grid(row=1, column=0, sticky="w")

shift_ctrl = tk.Frame(shift_inner, bg=PANEL)
shift_ctrl.grid(row=0, column=1, rowspan=2, sticky="e")
shift_inner.columnconfigure(1, weight=1)

btn_minus = tk.Label(shift_ctrl, text=" − ", font=("Courier New", 14, "bold"),
                     fg="white", bg="#3a3a52", padx=10, pady=4)
btn_minus.bind("<Button-1>", lambda e: decrement_shift())
btn_minus.bind("<Enter>",    lambda e: btn_minus.config(bg=ACCENT_R))
btn_minus.bind("<Leave>",    lambda e: btn_minus.config(bg="#3a3a52"))
btn_minus.pack(side="left", padx=(0, 4))

shift_var = tk.StringVar(value="0")
shift_display = tk.Label(shift_ctrl, textvariable=shift_var,
                         font=("Courier New", 18, "bold"), fg=ACCENT_R,
                         bg=PANEL, width=3, anchor="center")
shift_display.pack(side="left")

btn_plus = tk.Label(shift_ctrl, text=" + ", font=("Courier New", 14, "bold"),
                    fg="white", bg="#3a3a52", padx=10, pady=4)
btn_plus.bind("<Button-1>", lambda e: increment_shift())
btn_plus.bind("<Enter>",    lambda e: btn_plus.config(bg=ACCENT_G))
btn_plus.bind("<Leave>",    lambda e: btn_plus.config(bg="#3a3a52"))
btn_plus.pack(side="left", padx=(4, 0))

# ─── Action buttons (Label-based for full macOS color control) ────────────────
btn_row = tk.Frame(content, bg=BG)
btn_row.pack(fill="x", pady=(0, 10))

def make_btn(parent, text, color, hover_color, cmd, expand=True):
    lbl = tk.Label(parent, text=text,
                   font=("Courier New", 13, "bold"),
                   fg="white", bg=color,
                   padx=20, pady=14, anchor="center")
    lbl.bind("<Button-1>", lambda e: cmd())
    lbl.bind("<Enter>",    lambda e: lbl.config(bg=hover_color))
    lbl.bind("<Leave>",    lambda e: lbl.config(bg=color))
    if expand:
        lbl.pack(side="left", fill="x", expand=True, padx=(0, 6))
    else:
        lbl.pack(side="left", padx=(0, 0))
    return lbl

enc_btn = make_btn(btn_row, "Encrypt",  ACCENT_R,  "#cc3333", encrypt)
dec_btn = make_btn(btn_row, "Decrypt",  ACCENT_G,  "#009e78", decrypt)
clr_btn = make_btn(btn_row, "Clear",    "#3a3a52",  "#4a4a62", clear_all, expand=False)

# ─── Result panel ─────────────────────────────────────────────────────────────
res_panel = make_panel(content)
res_panel.pack(fill="x", pady=(0, 10))

res_top = tk.Frame(res_panel, bg=PANEL)
res_top.pack(fill="x", padx=14, pady=(8, 4))

result_status_var = tk.StringVar(value="")
res_label_left = tk.Label(res_top, text=">_  RESULT",
                           font=("Courier New", 9, "bold"), fg=ACCENT_G, bg=PANEL)
res_label_left.pack(side="left")

res_badge = tk.Label(res_top, textvariable=result_status_var,
                     font=("Courier New", 8), fg=ACCENT_R,
                     bg="#2a0a0a", padx=6, pady=2)
res_badge.pack(side="left", padx=8)

copy_btn = tk.Label(res_top, text="  Copy result",
                    font=("Courier New", 8), fg=FG_DIM, bg=BORDER,
                    padx=8, pady=2)
copy_btn.bind("<Button-1>", lambda e: copy_result())
copy_btn.bind("<Enter>",    lambda e: copy_btn.config(bg="#3a3a4a"))
copy_btn.bind("<Leave>",    lambda e: copy_btn.config(bg=BORDER))
copy_btn.pack(side="right")

result_box = tk.Text(res_panel, height=4, font=("Courier New", 11),
                     bg="#0f0f1a", fg=FG_MONO, relief="flat",
                     padx=10, pady=8, state="disabled",
                     highlightbackground=BORDER, highlightthickness=1)
result_box.pack(fill="x", padx=14, pady=(0, 6))

tk.Label(res_panel, text="UTF-8 // STREAM LOCK",
         font=("Courier New", 7), fg=FG_DIM, bg=PANEL, anchor="e"
         ).pack(fill="x", padx=14, pady=(0, 6))

# ─── Footer ───────────────────────────────────────────────────────────────────
footer = tk.Frame(root, bg="#0d0d14", height=30)
footer.pack(fill="x", side="bottom")
footer.pack_propagate(False)

tk.Label(footer,
         text="CIPHER//DECK V1.0 — CAESAR PIPELINE  ·  SkillCraft Technology Internship",
         font=("Courier New", 7), fg=FG_DIM, bg="#0d0d14").pack(side="left", padx=16, pady=8)

tk.Label(footer, text="ASCII SPECIFICATION  ·  ROT-N ENGINE",
         font=("Courier New", 7), fg=FG_DIM, bg="#0d0d14").pack(side="right", padx=16)

# ─── Init ─────────────────────────────────────────────────────────────────────
update_rotor_matrix()
root.mainloop()
