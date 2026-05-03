#!/usr/bin/env python3

import unicodedata
from urllib.parse import urlparse

TOOL_NAME = "UNiiLLU"
VERSION = "v1.0"


def banner():
    print(rf"""
        ██╗   ██╗███╗   ██╗██╗██╗     ██╗     ██╗   ██╗
        ██║   ██║████╗  ██║██║██║     ██║     ██║   ██║
        ██║   ██║██╔██╗ ██║██║██║     ██║     ██║   ██║
        ██║   ██║██║╚██╗██║██║██║     ██║     ██║   ██║
        ╚██████╔╝██║ ╚████║██║███████╗███████╗╚██████╔╝
         ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝ ╚═════╝ 

                {TOOL_NAME}  {VERSION}

[ ASCII vs Unicode Analyzer ]
[ Author: TenzinNorden.T ]
----------------------------------------------------
""")


def description():
    print("Some domains look normal but are not.")
    print("They may use hidden characters or simple tricks that look like English.\n")

    print("Examples:")
    print("apple.com        → normal")
    print("аррӏе.com        → uses lookalike characters")
    print("rnicrosoft.com   → 'rn' looks like 'm'")
    print("g00gle.com       → '0' looks like 'o'")
    print("СNN.com          → first letter is not English 'C'\n")

    print("This tool shows what is actually being used.\n")


def extract_domain(input_text):
    if "@" in input_text:
        return input_text.split("@")[-1]
    parsed = urlparse(input_text)
    return parsed.netloc if parsed.netloc else input_text


LOOKALIKE_MAP = {
    'а':'a','е':'e','о':'o','р':'p','с':'c',
    'і':'i','ӏ':'l','ѕ':'s',
    'А':'A','В':'B','С':'C','Е':'E','Н':'H',
    'К':'K','М':'M','О':'O','Р':'P','Т':'T','Х':'X',
    'ο':'o','Ο':'O','α':'a',
    'ɑ':'a'
}


ASCII_MAP = {
    "rn": ("m", "'rn' is two letters that can look like 'm'"),
    "vv": ("w", "'vv' is two letters that can look like 'w'"),
    "cl": ("d", "'cl' can look like 'd'"),
    "0": ("o", "'0' is a number that looks like 'o'"),
    "1": ("l", "'1' is a number that can look like 'l' or 'i'"),
    "3": ("e", "'3' can look like 'e'"),
    "5": ("s", "'5' can look like 's'")
}


def normalize_unicode(text):
    return ''.join(LOOKALIKE_MAP.get(c, c) for c in text)


def normalize_ascii(text):
    result = text
    for fake, (real, _) in ASCII_MAP.items():
        result = result.replace(fake, real)
    return result


def detect_ascii(text):
    found = []
    for fake, (real, explanation) in ASCII_MAP.items():
        if fake in text:
            found.append(explanation)
    return found


def check_case(text):
    if text != text.lower():
        return "Capital letters used (does not affect domain)"
    else:
        return "All lowercase (clean)"


def analyze(domain):
    print(f"\n[+] Target: {domain}")

    name = domain.split('.')[0]

    unicode_found = False
    confusable_found = False

    print("\n[+] Inspection:")

    for char in name:
        if ord(char) > 127:
            unicode_found = True

            print(f"[!] '{char}' is not a normal English letter")

            if char in LOOKALIKE_MAP:
                confusable_found = True
                print(f"    It looks like '{LOOKALIKE_MAP[char]}'")

    if not unicode_found:
        print("[+] All characters are standard ASCII")

    ascii_issues = detect_ascii(name)
    if ascii_issues:
        print("\n[!] Tricks found:")
        for e in ascii_issues:
            print(f"    {e}")

    step1 = normalize_unicode(name)
    step2 = normalize_ascii(step1)

    if step2 != name:
        print(f"\n[!] Real form → {step2}")

    print("\n[+] Case:")
    print(f"    {check_case(name)}")

    print("\n[+] Result:")

    if confusable_found or ascii_issues:
        print("[!] This domain can trick people")
    elif unicode_found:
        print("[!] Unusual characters found")
    else:
        print("[+] Looks clean")


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
            analyze(domain)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting UNiiLLU...")
            break
