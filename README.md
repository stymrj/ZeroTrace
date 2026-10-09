<div align="center">

# ⚡ ZeroTrace

**Next-Gen All-in-One OSINT & Reconnaissance Framework**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Termux%20%7C%20Windows-blueviolet)](https://github.com/)
[![Stars](https://img.shields.io/github/stars/stymrj/ZeroTrace?style=social)](https://github.com/styrj/ZeroTrace)

An asynchronous, visually rich open-source intelligence suite designed for security researchers, ethical hackers, bug bounty hunters, and OSINT investigators.

[Key Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage) • [Modules](#-recon-modules) • [Contributing](#-contributing) • [Disclaimer](#-disclaimer)

</div>

---

## 🚀 Key Features

- ⚡ **Asynchronous Concurrency:** Scans 40+ platforms simultaneously in seconds using `asyncio` and `aiohttp`.
- 🌐 **Deep IP & ASN Intelligence:** Retrieves IP geolocation, ISP, ASN org, timezone, coordinates, and Google Maps direct links.
- 📱 **Global Phone Footprinting:** International E.164 parsing, carrier detection, line classification (mobile/fixed/VoIP), and direct WhatsApp chat links.
- 🕵️ **Username Reconnaissance:** Multi-platform footprinting with low false-positive heuristics and status verification.
- 🛡️ **DNS & Domain Intelligence:** Rapid resolution of A, AAAA, MX, NS, and TXT security records.
- ✉️ **Email Reconnaissance:** Syntax validation, MX mail exchanger check, disposable domain detection, and Gravatar profile identification.
- 🎨 **Modern Terminal UI:** Built with `Rich` for clean tables, live spinners, colorized status badges, and interactive navigation.
- 💾 **Automated Report Export:** Export investigation results to structured JSON and Markdown formats.
- 📱 **Full Termux / Android Support:** Runs natively on Termux without complex external dependencies.

---

## 📥 Installation

### On Linux & macOS
```bash
# Clone the repository
git clone https://github.com/stymrj/ZeroTrace.git
cd ZeroTrace

# Install required dependencies
pip3 install -r requirements.txt

# Launch ZeroTrace
python3 -m zerotrace.cli
```

### On Termux (Android)
```bash
# Update repositories and install Python & Git
pkg update -y && pkg install python git -y

# Clone and run
git clone https://github.com/stymrj/ZeroTrace.git
cd ZeroTrace
pip install -r requirements.txt
python -m zerotrace.cli
```

### Direct Pip Installation (Editable Mode)
```bash
pip install -e .
zerotrace
```

---

## 🎯 Recon Modules

| Module | Description | Output |
| :--- | :--- | :--- |
| **IP Intelligence** | Target IP/ASN lookup & local public IP resolution | Country, city, ISP, ASN, Google Maps link |
| **Phone Recon** | Global phone number parsing | Carrier, location, line type, WhatsApp link |
| **Username Recon** | Concurrent social platform footprinting | Found profile URLs across 40+ platforms |
| **Domain Recon** | DNS & nameserver inspection | A, AAAA, MX, NS, TXT verification records |
| **Email Recon** | Email validator & footprinting | MX records, disposable domain check, Gravatar |
| **Export Engine** | Session data serialization | Clean JSON and Markdown reports |

---

## 🤝 Contributing

Contributions are what make the open-source community an amazing place! Any contributions you make are **greatly appreciated**.

- **Want to add new platforms?** Adding a site to the username scanner takes less than 2 minutes in `zerotrace/core/config.py`.
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
- Look for issues tagged `good first issue` to make your first contribution!

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## ⚠️ Disclaimer

ZeroTrace is developed strictly for educational, security research, and authorized investigative purposes. The developers assume no liability for misuse or damage caused by this program. Always adhere to applicable laws and terms of service.
