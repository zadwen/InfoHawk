![InfoHawk Project](assets/project.png)



# 🦅 InfoHawk v3.2 – OSINT Intelligence Suite



> A powerful and easy-to-use OSINT platform for cybersecurity professionals and law enforcement.

**Fully working OSINT toolkit for cyber investigations**  
**Crafted by Zadwen**

---

### 🧰 Tools Included (Pre-installed)

- ✅ Sherlock (fast subprocess-based call)
- ✅ PhoneInfoga (precompiled CLI v2.11.0)
- ✅ HIBP Breach Check (live via your API key)
- ✅ Leak Search (combo/LinkedIn dumps)
- ✅ Pastebin Monitor (basic Google dork emulation)
- ✅ Holehe (check email usage on services)

---

### ⚙️ How to Run

```bash
cd InfoHawk
pip install -r requirements.txt --break-system-packages
chmod +x run.sh
./run.sh
```

Then open: `http://localhost:8501`

---

### 🔐 Add Your HIBP API Key

In `main.py`, edit this line:

```python
api_key = "your_actual_api_key_here"
```

You can get one from: [https://haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key)

---

### 📁 Folder Structure

```
InfoHawk/
├── sherlock/                # Sherlock project
├── assets/                  # Image, screenshots
├── modules/                 # Extra tool functions
├── app.py                   # Streamlit dashboard
├── main.py                  # Tool logic
├── autosave.py              # Save search history
├── requirements.txt
├── run.sh
└── README.md
```

---

### 🧠 Author

**Made with ❤️ by Zadwen**  
Cybersecurity Researcher | OSINT Enthusiast

---
