import subprocess
import streamlit as st
import os
import requests

st.set_page_config(page_title="InfoHawk", layout="wide")
st.title("🦅 InfoHawk – OSINT Intelligence Suite")
st.markdown("Built for cybersecurity professionals and investigators by **Zadwen**.")

mode = st.sidebar.selectbox("Choose OSINT Module", [
    "Username Discovery (Sherlock)",
    "Phone Lookup (PhoneInfoga)",
    "Email Breach Check (HIBP)",
    "Leak Dump Search (Simulated)"
])

if mode == "Username Discovery (Sherlock)":
    username = st.text_input("Enter username")
    if st.button("Search Username"):
        try:
            result = subprocess.getoutput(f"python3 sherlock/sherlock.py {username}")
            if "No usernames found" in result or not result.strip():
                st.warning("No usernames found on target platforms.")
            else:
                st.success("✅ Username discovery complete:")
                st.code(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

elif mode == "Phone Lookup (PhoneInfoga)":
    number = st.text_input("Enter phone number")
    if st.button("Run PhoneInfoga"):
        try:
            result = subprocess.getoutput(f"phoneinfoga scan -n {number}")
            if not result.strip():
                st.warning("No phone information found.")
            else:
                st.success("✅ Phone number scan complete:")
                st.code(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

elif mode == "Email Breach Check (HIBP)":
    email = st.text_input("Enter target email:")
    if st.button("Check Breaches"):
        try:
            api_key = "7eb79f8cbaf84d768b553c389df93a65"
            headers = {
                "User-Agent": "InfoHawk",
                "hibp-api-key": api_key
            }
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                data = r.json()
                if data:
                    st.success(f"✅ {email} found in the following breaches:")
                    for b in data:
                        st.write(f"- {b['Name']} ({b['BreachDate']})")
                else:
                    st.info("✅ No breach data found.")
            elif r.status_code == 404:
                st.info("✅ No breaches found.")
            elif r.status_code == 401:
                st.error("❌ Invalid HIBP API Key.")
            else:
                st.error(f"❌ HIBP Error: {r.status_code}")
        except Exception as e:
            st.error(f"❌ Exception: {e}")

elif mode == "Leak Dump Search (Simulated)":
    term = st.text_input("Enter keyword to search in dumps")
    if st.button("Search Dumps"):
        matches = []
        try:
            with open("modules/leaks.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if term.lower() in line.lower():
                        matches.append(line.strip())
            if matches:
                st.success(f"✅ Found {len(matches)} matching records:")
                for m in matches:
                    st.code(m)
            else:
                st.warning("No matches found in leak database.")
        except FileNotFoundError:
            st.error("Leak file not found: modules/leaks.txt")
