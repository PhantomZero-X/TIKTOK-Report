<p align="center"> <img src="https://img.shields.io/badge/Version-0.1.0-blue.svg" alt="Version"> <img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python"> <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"> <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg" alt="Platform"> </p>

# ⚔️ XSS Scanner — Modern & Stylish

![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge) ![Build](https://img.shields.io/badge/status-ready-blue?style=for-the-badge) ![Language](https://img.shields.io/badge/Language-Python%20%7C%20CLI-orange?style=for-the-badge)

---

<p align="center">
  <img src="./assets/banner.png" alt="XSS Scanner Banner" width="900" />
</p>

> **XSS Scanner** — A fast, modern, and ethical Cross-Site Scripting (XSS) detection tool built for bug hunters, pentesters, and security students. Designed to be beautiful in the repo and powerful in the field.

---

## ✨ Highlights

* Modern, minimal CLI interface with readable results
* Supports **GET** and **POST** parameter fuzzing
* Custom payload lists and payload templating
* Output to JSON / CSV for easy ingestion into other tools
* Safe-by-default: rate limits, optional dry-run, and explicit consent reminder

---

## 🎨 Fancy ASCII Banner (terminal)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   ███╗   ██╗██╗  ██╗███████╗    ███████╗ █████╗ ███╗   ██╗███████╗ ██████╗   ┃
┃   ████╗  ██║██║  ██║██╔════╝    ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔═══██╗  ┃
┃   ██╔██╗ ██║███████║█████╗      ███████╗███████║██╔██╗ ██║█████╗  ██║   ██║  ┃
┃   ██║╚██╗██║██╔══██║██╔══╝      ╚════██║██╔══██║██║╚██╗██║██╔══╝  ██║   ██║  ┃
┃   ██║ ╚████║██║  ██║███████╗    ███████║██║  ██║██║ ╚████║███████╗╚██████╔╝  ┃
┃   ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

> Tip: Use `rich` (Python) or `colorama` to color this banner in the terminal.

---

## 🚀 Quick Start

```bash
# clone
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# install
python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt

# run basic scan
python xss_scanner.py --url "https://target.example/search?q=" --payloads payloads/common.txt
```

---

## 🧭 Usage (examples)

* Scan a single GET parameter:

```bash
python xss_scanner.py --url "https://target.example/page?name="
```

* Scan with a custom payload file and save results:

```bash
python xss_scanner.py --url "https://target.example/search?q=" --payloads payloads/custom.txt --output results.json
```

* POST scanning (body templating):

```bash
python xss_scanner.py --url "https://target.example/login" --method POST --template "username={payload}&password=pass"
```

---

## 🧾 Output Formats

* `--output results.json` (structured JSON)
* `--output results.csv` (spreadsheet-friendly)
* Terminal summary with pretty box (vulnerable param list)

---

## 🔒 Safety & Ethics

This tool is provided **only for authorized security testing and research**. Do **NOT** run it against systems you do not own or do not have explicit permission to test.

By running this tool you confirm you have permission to test the target.

---

## 🧩 Features & Roadmap

* ✅ Reflected XSS detection
* ✅ Payload templating and response heuristics
* ✅ Rate limiting and concurrency controls
* 🟧 Stored XSS detection (planned)
* 🟧 Browser-based DOM checks (via headless browser) (planned)
* 🟧 CI integration and GitHub Action for automated scanning in staging (planned)

---

## 📁 Recommended Repository Layout

```
├── README.md
├── LICENSE
├── xss_scanner.py
├── requirements.txt
├── payloads/
│   ├── common.txt
│   └── xss_payloads.txt
├── assets/
│   └── banner.png
└── examples/
    └── scan_example.json
```

---

## 🖼️ Creating a Modern Banner Image (assets/banner.png)

If you want a modern repo banner image (recommended for GitHub README):

1. Use Figma / Canva / Photopea to compose a sleek banner (900×300px). Include the project name, short tagline, and a subtle background pattern.
2. Export as `banner.png` and place it in `assets/banner.png`.
3. Reference it in the README as shown above.

If you'd like, I can generate multiple ASCII banners or a SVG banner template you can edit.

---

## 🛠️ Contributing

Contributions welcome — open an issue or a PR. Please follow the CONTRIBUTING.md guidelines (add tests, keep changes focused).

---

## 📜 License

MIT © Kilua Ahmad Al.A

---

## 💬 Contact

Kilua Ahmad Al.A — [kiluanostalgia@gmail.com](mailto:kiluanostalgia@gmail.com)

---

> *Made with 🔍 + ☕ for learning and ethical security research.*
