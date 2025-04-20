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
        subprocess.run(["python3", "sherlock/sherlock.py", username])
        st.success("✅ Sherlock run complete.")

elif mode == "Phone Lookup (PhoneInfoga)":
    number = st.text_input("Enter phone number")
    if st.button("Run PhoneInfoga"):
        subprocess.run(["phoneinfoga", "scan", "-n", number])
        st.success("✅ PhoneInfoga run complete.")

elif mode == "Email Breach Check (HIBP)":
    email = st.text_input("Enter target email:")
    if st.button("Check Breaches"):
        api_key = "7eb79f8cbaf84d768b553c389df93a65"  # <- Your provided key
        headers = {
            "User-Agent": "InfoHawk",
            "hibp-api-key": api_key
        }
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            st.success(f"✅ Found breaches: {[b['Name'] for b in r.json()]}")
        elif r.status_code == 404:
            st.info("✅ No breach found.")
        else:
            st.error(f"Error {r.status_code}: Check API key or email format.")

elif mode == "Leak Dump Search (Simulated)":
    email = st.text_input("Enter term to search in dumps:")
    if st.button("Search Dumps"):
        found = []
        for leak_file in ["combo-list.txt", "linkedin_leak.txt"]:
            if email in leak_file:
                found.append(leak_file)
        for match in found:
            st.success(f"Found in {match}")
        if not found:
            st.warning("No results found in local dumps.")
