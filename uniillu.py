#!/usr/bin/env python3

import unicodedata
from urllib.parse import urlparse

TOOL_NAME = "UNiiLLU"
VERSION = "v0.5"


def banner():
    print(r"""
        ██╗   ██╗███╗   ██╗██╗██╗     ██╗     ██╗   ██╗
        ██║   ██║████╗  ██║██║██║     ██║     ██║   ██║
        ██║   ██║██╔██╗ ██║██║██║     ██║     ██║   ██║
        ██║   ██║██║╚██╗██║██║██║     ██║     ██║   ██║
        ╚██████╔╝██║ ╚████║██║███████╗███████╗╚██████╔╝
         ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝ ╚═════╝ 

                U N i i L L U

[ Unicode Illusion Scanner ]
[ Author: TenzinNorden.T ]
----------------------------------------------------
""")


def description():
    print("Detects deceptive domains that visually imitate legitimate ones.\n")


# 🔧 Normalize visual tricks
def normalize_domain(name):
    replacements = {
        "rn": "m",
        "vv": "w",
        "cl": "d",
        "0": "o",
        "1": "l",
        "3": "e",
        "@": "a"
    }

    normalized = name
    for fake, real in replacements.items():
        normalized = normalized.replace(fake, real)

    return normalized


# 🔍 Script detection
def detect_script(char):
    try:
        name = unicodedata.name(char)

        if "LATIN" in name:
            return "Latin (ASCII)" if ord(char) < 128 else "Latin (Extended)"
        elif "CYRILLIC" in name:
            return "Cyrillic"
        elif "GREEK" in name:
            return "Greek"
        else:
            return "Other"

    except ValueError:
        return "Unknown"


# 🔍 Confusable Unicode characters
def is_confusable(char):
    confusables = {'ɑ', 'а', 'е', 'ο', 'і', 'ӏ', 'ѕ', 'ԁ', 'ԛ'}
    return char in confusables


# 🔍 ASCII illusions
def detect_ascii_illusion(domain):
    patterns = {
        "rn": "m",
        "vv": "w",
        "cl": "d",
        "0": "o",
        "1": "l",
        "l": "i"
    }

    found = []
    for fake, real in patterns.items():
        if fake in domain:
            found.append((fake, real))

    return found


# 🔍 Extract domain
def extract_domain(input_text):
    if "@" in input_text:
        return input_text.split("@")[-1]
    parsed = urlparse(input_text)
    return parsed.netloc if parsed.netloc else input_text


# 🔍 Core analysis
def analyze_domain(domain):
    print(f"\n[+] Target: {domain}\n")

    scripts_used = {}
    confusable_found = []

    for char in domain:
        if char.isalnum():
            script = detect_script(char)
            scripts_used.setdefault(script, []).append(char)

            if is_confusable(char):
                confusable_found.append(char)

    for script, chars in scripts_used.items():
        print(f"{script}: {''.join(chars)}")

    print("\n[+] Analysis:")

    if len(scripts_used) > 1:
        print("[!] Mixed scripts detected → HIGH RISK")

    if "Latin (Extended)" in scripts_used:
        print("[!] Non-ASCII Latin detected → possible spoofing")

    if confusable_found:
        print(f"[!] Confusable characters → {''.join(confusable_found)}")

    ascii_issues = detect_ascii_illusion(domain)
    if ascii_issues:
        print("[!] ASCII visual tricks:")
        for fake, real in ascii_issues:
            print(f"    '{fake}' → '{real}'")

    # 🔥 Core upgrade: normalization insight
    name = domain.split('.')[0]
    normalized = normalize_domain(name)

    if normalized != name:
        print(f"[!] Normalized form → {normalized}")

    if len(scripts_used) == 1 and not confusable_found and not ascii_issues:
        print("[+] Looks normal")


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
