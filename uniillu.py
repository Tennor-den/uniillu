#!/usr/bin/env python3

import unicodedata
from urllib.parse import urlparse

TOOL_NAME = "UNiiLLU"
VERSION = "v0.9"


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
    print("Some domains look normal but are not.")
    print("They use characters from other languages or tricks that look like English.\n")

    print("Examples:")
    print("apple.com        → normal")
    print("аррӏе.com        → uses lookalike characters")
    print("rnicrosoft.com   → 'rn' looks like 'm'")
    print("g00gle.com       → '0' looks like 'o'")
    print("СNN.com          → first letter is not English 'C'\n")

    print("This tool reveals what is actually being used.\n")


# 🔍 Extract domain
def extract_domain(input_text):
    if "@" in input_text:
        return input_text.split("@")[-1]
    parsed = urlparse(input_text)
    return parsed.netloc if parsed.netloc else input_text


# 🔍 Unicode confusable detection
def is_confusable(char):
    return char in {
        'а','е','о','р','с','і','ӏ','ѕ',
        'А','В','С','Е','Н','К','М','О','Р','Т','Х',
        'ο','Ο','α',
        'ɑ'
    }


# 🔧 Normalize Unicode → ASCII
def normalize_unicode(text):
    mapping = {
        'а':'a','е':'e','о':'o','р':'p','с':'c',
        'у':'y','х':'x','і':'i','ӏ':'l','ѕ':'s',
        'А':'A','В':'B','С':'C','Е':'E','Н':'H',
        'К':'K','М':'M','О':'O','Р':'P','Т':'T','Х':'X',
        'ο':'o','Ο':'O','α':'a',
        'ɑ':'a'
    }
    return ''.join(mapping.get(c, c) for c in text)


# 🔧 Normalize ASCII tricks
def normalize_ascii(text):
    replacements = {
        "rn": "m",
        "vv": "w",
        "cl": "d",
        "0": "o",
        "1": "l",
        "3": "e",
        "5": "s"
    }

    result = text
    for fake, real in replacements.items():
        result = result.replace(fake, real)

    return result


# 🔍 Human-readable ASCII trick detection
def detect_ascii_tricks(text):
    patterns = {
        "rn": ("m", "'rn' is two letters that can look like 'm'"),
        "vv": ("w", "'vv' is two letters that can look like 'w'"),
        "cl": ("d", "'cl' can look like 'd'"),
        "0":  ("o", "'0' is a number that looks like 'o'"),
        "1":  ("l", "'1' is a number that can look like 'l' or 'i'"),
        "3":  ("e", "'3' can look like 'e'"),
        "5":  ("s", "'5' can look like 's'")
    }

    found = []
    for fake, (real, explanation) in patterns.items():
        if fake in text:
            found.append((fake, real, explanation))

    return found


# 🔍 Main analysis
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

    # 🔍 ASCII tricks
    ascii_issues = detect_ascii_tricks(name)
    if ascii_issues:
        print("\n[!] ASCII visual tricks:")
        for _, _, explanation in ascii_issues:
            print(f"    {explanation}")

    # 🔥 Normalize
    unicode_norm = normalize_unicode(name)
    ascii_norm = normalize_ascii(unicode_norm)

    if unicode_norm != name:
        print(f"\n[!] Unicode normalized → {unicode_norm}")

    if ascii_norm != unicode_norm:
        print(f"[!] ASCII normalized → {ascii_norm}")

    # 🔍 Conclusion
    print("\n[+] Conclusion:")

    if found_confusable or ascii_issues:
        print("[!] High risk → deceptive characters detected")
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
