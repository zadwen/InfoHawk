
import streamlit as st
import subprocess\nimport json\nfrom autosave import save_case

st.set_page_config(page_title="InfoHawk OSINT Suite", page_icon="🦅", layout="wide")

st.title("🦅 InfoHawk v3 - OSINT Suite for Cyber Investigations")
st.markdown("A powerful and easy-to-use OSINT platform for cybersecurity professionals and law enforcement.")

st.sidebar.header("Choose Module")

module = st.sidebar.selectbox("Select OSINT Tool", [
    "Email Breach Check (HIBP)",
    "Phone Lookup (PhoneInfoga)",
    "Domain Recon",
    "Username Discovery (Sherlock)",
    "Leak Dump Search (Simulated)",
    "Pastebin Monitor (Simulated)",
    "Export Sample Report"
])

if module == "Email Breach Check (HIBP)":
    email = st.text_input("Enter target email:")
    if st.button("Check Breaches"):
        if email:
            st.write(f"🔎 Searching breaches for: {email}")
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {"User-Agent": "InfoHawk OSINT Tool"}
            import requests
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                for b in r.json():
                    st.success(f"Found in {b['Name']} on {b['BreachDate']}")
            elif r.status_code == 404:
                st.info("No breaches found.")
            else:
                st.error(f"Error: {r.status_code}")


    if email:
        case = {
            "target": email,
            "breaches": [b['Name'] for b in r.json()] if r.status_code == 200 else []
        }
        case_id = save_case(case, label=email)
        st.success(f"Case saved: {case_id}")

elif module == "Phone Lookup (PhoneInfoga)":

    number = st.text_input("Enter phone number (e.g., +14158586273):")
    if st.button("Run PhoneInfoga"):
        st.write("Running PhoneInfoga (requires PhoneInfoga installed)...")
        subprocess.run(["phoneinfoga", "scan", "-n", number])

elif module == "Domain Recon":
    domain = st.text_input("Enter domain (e.g., example.com):")
    if st.button("Run Domain Recon"):
        st.write("🔍 WHOIS")
        st.code(subprocess.getoutput(f"whois {domain}"))
        st.write("📡 NSLOOKUP")
        st.code(subprocess.getoutput(f"nslookup {domain}"))
        st.write("📬 DIG A record")
        st.code(subprocess.getoutput(f"dig +short {domain}"))

elif module == "Username Discovery (Sherlock)":
    uname = st.text_input("Enter username:")
    if st.button("Run Sherlock"):
        st.write(f"🔍 Searching username: {uname}")
        subprocess.run(["python3", "-m", "sherlock_project.sherlock", uname])

elif module == "Leak Dump Search (Simulated)":
    term = st.text_input("Enter term to search in dumps:")
    if st.button("Search Dumps"):
        st.success("Found in combo-list.txt (2021)")
        st.success("Found in linkedin_leak.txt (2012)")

elif module == "Pastebin Monitor (Simulated)":
    term = st.text_input("Enter keyword for pastebin monitoring:")
    if st.button("Monitor"):
        st.info("Matched: https://pastebin.com/abc123")
        st.info("Possible Match: https://pastebin.com/xyz789")

elif module == "Export Sample Report":
    st.download_button("📥 Download Sample Markdown", "## Report for: target\n\nBreached in LinkedIn\nFound on GitHub", file_name="report.md")
    st.download_button("📥 Download Sample JSON", '{"target":"target","breaches":["LinkedIn"],"profiles":["GitHub"]}', file_name="report.json")
