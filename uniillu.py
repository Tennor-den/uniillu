#!/usr/bin/env python3

import unicodedata
from urllib.parse import urlparse

TOOL_NAME = "UNiiLLU"
VERSION = "v0.7"


def banner():
    print(r"""
        ██╗   ██╗███╗   ██╗██╗██╗     ██╗     ██╗   ██╗
        ██║   ██║████╗  ██║██║██║     ██║     ██║   ██║
        ██║   ██║██╔██╗ ██║██║██║     ██║     ██║   ██║
        ██║   ██║██║╚██╗██║██║██║     ██║     ██║   ██║
        ╚██████╔╝██║ ╚████║██║███████╗███████╗╚██████╔╝
         ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝ ╚═════╝ 

                U N i i L L U

[ ASCII vs Unicode Analyzer ]
[ Author: TenzinNorden.T ]
----------------------------------------------------
""")


def description():
    print("Detects non-ASCII characters and highlights visually deceptive Unicode.\n")


# 🔍 Extract domain
def extract_domain(input_text):
    if "@" in input_text:
        return input_text.split("@")[-1]
    parsed = urlparse(input_text)
    return parsed.netloc if parsed.netloc else input_text


# 🔍 Confusable characters (visually deceptive)
def is_confusable(char):
    return char in {
        # Cyrillic lookalikes
        'а','е','о','р','с','і','ӏ','ѕ',
        'А','В','С','Е','Н','К','М','О','Р','Т','Х',

        # Greek lookalikes
        'ο','Ο','α',

        # Latin extended lookalikes
        'ɑ'
    }


# 🔧 Normalize Unicode → ASCII (reveal truth)
def normalize_unicode(text):
    mapping = {
        # Cyrillic
        'а': 'a','е': 'e','о': 'o','р': 'p','с': 'c',
        'у': 'y','х': 'x','і': 'i','ӏ': 'l','ѕ': 's',

        'А': 'A','В': 'B','С': 'C','Е': 'E','Н': 'H',
        'К': 'K','М': 'M','О': 'O','Р': 'P','Т': 'T','Х': 'X',

        # Greek
        'ο': 'o','Ο': 'O','α': 'a',

        # Latin extended
        'ɑ': 'a'
    }

    return ''.join(mapping.get(c, c) for c in text)


# 🔍 Core analysis
def analyze_domain(domain):
    print(f"\n[+] Target: {domain}")

    name = domain.split('.')[0]

    found_unicode = False
    found_confusable = False

    print("\n[+] Inspection:")

    for char in name:
        code = ord(char)

        if code < 128:
            continue

        found_unicode = True

        try:
            uname = unicodedata.name(char)
        except ValueError:
            uname = "UNKNOWN"

        print(f"[!] Unicode → '{char}' ({uname}, U+{code:04X})")

        if is_confusable(char):
            found_confusable = True
            print("    [!] Visually confusable with ASCII")

    if not found_unicode:
        print("[+] All characters are standard ASCII")

    # 🔥 Reveal true form
    normalized = normalize_unicode(name)

    if normalized != name:
        print(f"\n[!] Revealed ASCII form → {normalized}")

    # 🔥 Final judgement
    print("\n[+] Conclusion:")

    if found_confusable:
        print("[!] High risk → visually deceptive Unicode detected")
    elif found_unicode:
        print("[!] Non-ASCII present → review required")
    else:
        print("[+] Clean ASCII domain")


# 🚀 Main loop
if __name__ == "__main__":
    banner()
    description()

    while True:
        try:
            user_input = input("Enter URL/email (or 'exit'): ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("\nExiting UNiiLLU...")
                break

            if not user_input:
                continue

            domain = extract_domain(user_input)
            analyze_domain(domain)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting UNiiLLU...")
            break
