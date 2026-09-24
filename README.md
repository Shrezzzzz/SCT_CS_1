# SCT_CS_1 — Caesar Cipher

A GUI-based Caesar Cipher encryption and decryption tool built with Python and Tkinter, developed as **Task 01** of the SkillCraft Technology Cyber Security Internship.

---

## Features

- Encrypt and decrypt text using the Caesar Cipher algorithm
- User-defined shift value (1–25) with + / − controls
- Live rotor mapping matrix showing the plain → cipher alphabet for the current shift
- Real-time character counter
- Copy result to clipboard
- Dark hacker-style UI (terminal aesthetic)
- Input validation with error messages
- Preserves spaces, numbers, and special characters
- Supports both uppercase and lowercase letters

---

## How Caesar Cipher Works

The Caesar Cipher is a substitution cipher where each letter is shifted by a fixed number of positions in the alphabet.

**Encryption:**
```
C = (P + K) mod 26
```

**Decryption:**
```
P = (C - K) mod 26
```

Where:
- `P` = plaintext character position
- `C` = ciphertext character position
- `K` = shift value (key)

---

## Technologies Used

- Python 3
- Tkinter (GUI)
- subprocess + pbcopy (macOS built-in clipboard support)

---

## Requirements

No external dependencies required. Everything used is part of Python's standard library or macOS built-ins.

> Tkinter comes bundled with Python 3 — no separate install needed.

---

## How to Run

```bash
python3 main.py
```

---

## Usage

1. Type your message in the **MESSAGE** input box.
2. Set your **SHIFT VALUE** using the `+` / `−` buttons.
3. Click **Encrypt** to encode, or **Decrypt** to decode.
4. The result appears in the **RESULT** panel — click **Copy result** to copy it.
5. Click **Clear** to reset everything.

---

## Project Structure

```
SCT_CS_1/
├── main.py          # Main application
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## Internship

**Organisation:** SkillCraft Technology  
**Domain:** Cyber Security  
**Task:** 01 — Caesar Cipher Encryption Tool
