# Contributing to ZeroTrace

Thank you for your interest in contributing to **ZeroTrace**! 

ZeroTrace thrives on community contributions. Whether you are fixing bugs, improving documentation, or adding new OSINT sources, your help is welcome.

---

## 🚀 Quick Ways to Contribute

1. **Add Social Media Sites:**
   Open `zerotrace/core/config.py` and add new platform URLs to `SOCIAL_TARGETS`.
2. **Improve Error Handling:**
   Submit enhancements to module parsers to handle rate-limiting and API updates.
3. **Enhance Termux UX:**
   Report or optimize terminal layout compatibility on mobile screens.

---

## 🛠️ Development Workflow

1. **Fork the repo** and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/ZeroTrace.git
   cd ZeroTrace
   ```
2. **Create a new branch**:
   ```bash
   git checkout -b feature/add-new-module
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Test your changes**:
   ```bash
   python -m zerotrace.cli
   ```
5. **Commit and push**:
   ```bash
   git commit -m "feat: add TikTok and Threads to username scanner"
   git push origin feature/add-new-module
   ```
6. **Open a Pull Request** with a descriptive summary of your changes.
