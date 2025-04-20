import streamlit as st
import subprocess
import os
import json
from autosave import save_case

st.set_page_config(page_title="InfoHawk v3.1.1", page_icon="🦅", layout="wide")
st.title("🦅 InfoHawk – OSINT Intelligence Suite")
st.markdown("Built for cybersecurity professionals and investigators by **Zadwen**.")

st.sidebar.header("Choose OSINT Module")

module = st.sidebar.selectbox("Select a module", [
    "Email Breach Check (HIBP)",
    "Phone Lookup (PhoneInfoga)",
    "Domain Recon",
    "Username Discovery (Sherlock)",
    "Leak Dump Search",
    "Pastebin Monitor",
    "Export Sample Report"
])

if module == "Email Breach Check (HIBP)":
    email = st.text_input("Enter email address")
    if st.button("Check Breaches"):
        api_key = os.getenv("HIBP_API_KEY")
        if not api_key:
            st.error("HIBP API key not found. Please set HIBP_API_KEY environment variable.")
        else:
            headers = {
                "User-Agent": "InfoHawk OSINT Tool",
                "hibp-api-key": api_key
            }
            import requests
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                breaches = [b["Name"] for b in r.json()]
                for b in breaches:
                    st.success(f"🔓 Found in: {b}")
                save_case({"email": email, "breaches": breaches}, label=email)
            elif r.status_code == 404:
                st.info("✅ No breaches found.")
            else:
                st.error(f"API Error: {r.status_code}")

elif module == "Phone Lookup (PhoneInfoga)":
    number = st.text_input("Enter phone number (e.g. +14158586273)")
    if st.button("Lookup"):
        try:
            result = subprocess.getoutput(f"phoneinfoga scan -n {number}")
            st.code(result)
        except Exception as e:
            st.error(f"Error: {e}")

elif module == "Domain Recon":
    domain = st.text_input("Enter domain (e.g. example.com)")
    if st.button("Run Recon"):
        whois = subprocess.getoutput(f"whois {domain}")
        nslookup = subprocess.getoutput(f"nslookup {domain}")
        dig = subprocess.getoutput(f"dig +short {domain}")
        st.text("WHOIS:")
        st.code(whois)
        st.text("NSLOOKUP:")
        st.code(nslookup)
        st.text("DIG A Record:")
        st.code(dig)

elif module == "Username Discovery (Sherlock)":
    uname = st.text_input("Enter username")
    if st.button("Search Username"):
        try:
            result = subprocess.getoutput(f"python3 -m sherlock_project.sherlock {uname}")
            st.code(result)
        except Exception as e:
            st.error(f"Error: {e}")

elif module == "Leak Dump Search":
    term = st.text_input("Enter email/username/keyword to search in leaks")
    if st.button("Search Leaks"):
        leaks = []
        try:
            with open("modules/leaks.txt", "r") as f:
                lines = f.readlines()
            for line in lines:
                if term.lower() in line.lower():
                    leaks.append(line.strip())
            if leaks:
                for match in leaks:
                    st.success(f"Found: {match}")
                save_case({"search": term, "matches": leaks}, label=term)
            else:
                st.info("No matches found in local dumps.")
        except FileNotFoundError:
            st.error("Leak file not found!")

elif module == "Pastebin Monitor":
    keyword = st.text_input("Enter keyword (email/username) to simulate monitoring")
    if st.button("Simulate Pastebin Scan"):
        st.info(f"Found simulated match for '{keyword}' in pastebin.com/xyz123")
        st.info(f"Possible match: pastebin.com/abc789")

elif module == "Export Sample Report":
    st.download_button("📥 Download Markdown", data="## Report\n- Email: test@example.com", file_name="report.md")
    st.download_button("📥 Download JSON", data=json.dumps({"example": "data"}, indent=2), file_name="report.json")
