
![InfoHawk Project](project.png)

# 🦅 InfoHawk v3.2 – OSINT Intelligence Suite  
**Crafted with passion by Zadwen**

> A powerful and easy-to-use OSINT platform built for cybersecurity professionals, students, and law enforcement to investigate digital threats, fake accounts, breaches, and more.

---

### 🧰 Included Tools (Fully Integrated)

- ✅ **Sherlock** – Username lookup across 300+ platforms (subprocess-based, fast)
- ✅ **PhoneInfoga** – Phone number reconnaissance (CLI binary v2.11.0)
- ✅ **Holehe** – Detect email usage on websites
- ✅ **HIBP** – Breach check via HaveIBeenPwned API (live)
- ✅ **WHOIS / nslookup** – Domain and IP recon
- ✅ **Leak Search** – Look inside known credential dumps (LinkedIn combos etc.)
- ✅ **Pastebin Monitor** – Scrape paste dumps via dork-style search

---

### ⚙️ How to Use InfoHawk


```bash
cd InfoHawk
pip install -r requirements.txt --break-system-packages
chmod +x run.sh
./run.sh

api_key = "your_actual_api_key_here"
InfoHawk/
├── sherlock/                # Sherlock project (username scan)
├── assets/                  # Screenshots & logo
├── modules/                 # Functional logic per tool
├── app.py                   # Streamlit GUI
├── main.py                  # Core logic handler
├── autosave.py              # Save results automatically
├── requirements.txt         # Python dependencies
├── run.sh                   # Launcher
└── README.md                # You’re reading this

🧠 Author
Made with ❤️ by Zadwen
Cybersecurity Researcher | OSINT Enthusiast
Building tools to make investigations better 🚔🕵️‍♂️

For updates, features, and contributions – stay tuned on GitHub.com/zadwen



