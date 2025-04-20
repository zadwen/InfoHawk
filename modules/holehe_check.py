import subprocess

def run():
    print("[+] Holehe Email Intelligence Module")
    email = input("Enter email to analyze: ").strip()
    
    try:
        print(f"[~] Running holehe on {email}...")
        subprocess.run(["holehe", email])
    except FileNotFoundError:
        print("[!] Holehe is not installed. Run: pip install holehe")
