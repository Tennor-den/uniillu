# UNiiLLU

Unicode Illusion Scanner

---

## Description

UNiiLLU is a focused tool designed to expose deceptive domain names that appear legitimate at first glance. Attackers often manipulate characters using Unicode or subtle ASCII tricks to create domains that visually mimic trusted ones.

This tool breaks down domain structure, highlights unusual character usage, and reveals normalized forms to help you understand what a domain is trying to resemble.

The goal is simple. Help you see what your eyes miss.

---

## Features

* Unicode script detection (Latin, Cyrillic, Greek)
* Detection of confusable characters
* ASCII visual trick detection (rn → m, 0 → o)
* Domain normalization insight
* Interactive CLI mode

---

## Example

Input:
rnicrosoft.com

Output:
[!] ASCII visual tricks:
'rn' → 'm'
[!] Normalized form → microsoft

---

## Why it matters

Modern phishing attacks rely on visual deception rather than obvious errors. Domains can look legitimate while being structurally different. UNiiLLU helps reveal those differences clearly.

---

## Usage

```bash
python uniillu.py
```

---

## Author

TenzinNorden.T

---

## License

MIT License
