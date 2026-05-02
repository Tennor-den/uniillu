# UNiiLLU

Unicode Illusion Scanner

---

## Description

UNiiLLU is a simple tool built to catch something most people miss: fake domains that look real. Attackers replace normal letters with similar Unicode characters and create URLs or email domains that appear legitimate at first glance.

This tool scans those domains, breaks down each character, and points out anything unusual or deceptive. The goal is simple. Help you see what your eyes miss so you don’t get fooled by something that only pretends to be trustworthy.

---

## Features

* Detect Unicode script mixing
* Identify confusable characters
* Detect ASCII visual tricks (rn → m, vv → w)
* Works with URLs and email domains
* Interactive CLI mode

---

## Installation

```bash
git clone https://github.com/your-username/uniillu.git
cd uniillu
```

---

## Usage

```bash
python uniillu.py
```

or

```bash
python uniillu.py example.com
```

---

## Example

Input:
rnicrosoft.com

Output:
[!] ASCII visual tricks detected:
'rn' may mimic 'm'

---

## Author

TenzinNorden.T

---

## License

MIT License
