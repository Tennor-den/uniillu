# UNiiLLU

Unicode illusion scanner

---

## Description

UNiiLLU helps you spot domain names that look normal but are not. Some domains use Unicode characters that look the same as English letters. People see one thing but the computer reads something else.

This tool shows those hidden characters and reveals what the domain actually says.

---

## What it does

* Checks if a domain uses only standard ASCII characters
* Detects non ASCII characters inside the domain
* Highlights characters that look like English letters
* Shows the real Unicode identity of each suspicious character
* Reveals a clean ASCII version of the domain

---

## Why it matters

A domain can look safe but still be fake. Attackers use characters from other languages that look identical to English letters.

Example
apple.com is safe
аррӏе.com looks the same but is not

UNiiLLU helps you see that difference clearly.

---

## Example

Input
аррӏе.com

Output
Unicode detected
Characters are not standard ASCII
Revealed ASCII form → apple
High risk

---

## Usage

Run the tool

```bash
python uniillu.py
```

Enter a domain or email when asked.

---

## Notes

This tool focuses on Unicode deception. It does not depend on brand names or wordlists. It works on any domain.

---

## Author

TenzinNorden.T

---

## License

MIT License
