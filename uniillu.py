#!/usr/bin/env python3

import unicodedata
from urllib.parse import urlparse

TOOL_NAME = "UNiiLLU"
VERSION = "v0.3"


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
    print("Detects deceptive domains that look real but are not.\n")


# 🔍 Known brands for impersonation detection
COMMON_BRANDS = [
    "google",
    "microsoft",
    "apple",
    "amazon",
    "facebook",
    "paypal",
    "netflix"
]


# 🔍 Levenshtein distance (string similarity)
def levenshtein(a, b):
    if len(a) < len(b):
        return levenshtein(b, a)

    if len(b) == 0:
        return len(a)

    previous_row = range(len(b) + 1)

    for i, c1 in enumerate(a):
        current_row = [i + 1]
        for j, c2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# 🔍 Detect impersonation
def detect_impersonation(domain):
    name = domain.split('.')[0]

    for brand in COMMON_BRANDS:
        distance = levenshtein(name, brand)

        if distance <= 2 and name != brand:
            print(f"[!] Possible impersonation → {name} ≈ {brand}")


# 🔍 Detect script
def detect_script(char):
    try:
        name = unicodedata.name(char)

        if "LATIN" in name:
            if ord(char) < 128:
                return "Latin (ASCII)"
            else:
                return "Latin (Extended)"

        elif "CYRILLIC" in name:
            return "Cyrillic"

        elif "GREEK" in name:
            return "Greek"

        else:
            return "Other"

    except ValueError:
        return "Unknown"


# 🔍 Confusable Unicode chars
def is_confusable(char):
    confusables = {
        'ɑ', 'а', 'е', 'ο', 'і', 'ӏ', 'ѕ', 'ԁ', 'ԛ'
    }
    return char in confusables


# 🔍 ASCII illusion detection
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
    else:
        parsed = urlparse(input_text)
        return parsed.netloc if parsed.netloc else input_text


# 🔍 Main analysis
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

    # Show scripts
    for script, chars in scripts_used.items():
        print(f"{script}: {''.join(chars)}")

    print("\n[+] Analysis:")

    if len(scripts_used) > 1:
        print("[!] Mixed scripts detected → HIGH RISK")

    if "Latin (Extended)" in scripts_used:
        print("[!] Non-ASCII Latin detected → possible spoofing")

    if confusable_found:
        print(f"[!] Confusable characters found → {''.join(confusable_found)}")

    ascii_issues = detect_ascii_illusion(domain)
    if ascii_issues:
        print("[!] ASCII visual tricks detected:")
        for fake, real in ascii_issues:
            print(f"    '{fake}' may mimic '{real}'")

    # 🔥 New feature
    detect_impersonation(domain)

    if len(scripts_used) == 1 and not confusable_found and not ascii_issues:
        print("[+] Looks normal")


# 🚀 Main loop
if __name__ == "__main__":
    banner()
    description()

    while True:
        try:
            user_input = input("Enter URL/email (or 'exit' to quit): ").strip()

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
