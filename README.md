# 🦅 InfoHawk 4.0

**Public-information research workbench · Crafted by Zadwen**

InfoHawk is a local Streamlit app with real DNS, email-domain and phone-number
checks, optional Sherlock/Holehe adapters, and JSON reports. Version 4 replaces
the former title-only app and placeholder modules.

## What works

| Workspace | Function | Requirements / limits |
| --- | --- | --- |
| Domain & DNS | A, AAAA, MX, NS, TXT and CAA records | Network; system DNS resolver |
| Email → Domain checks | Syntax, normalized domain, mail DNS, Null MX recognition | Does not verify mailbox existence |
| Email → HIBP breaches | Official breach metadata | Your HIBP API key and eligible subscription |
| Email → Holehe | Captured CLI output | Optional `holehe` executable on PATH |
| Phone | Formatting, validity pattern, region, original carrier, time zones | Offline metadata; no owner lookup or live tracking |
| Username | Captured Sherlock output | Optional `sherlock` executable on PATH |
| Reports | Individual/all JSON downloads, clear session | Latest 50 results, memory only |

External-tool matches are unverified leads. A failed lookup is not a clean result.
There is no bundled PhoneInfoga binary, WHOIS client, credential-dump search,
Pastebin monitor, or bundled Sherlock checkout. Previous claims of those fully
integrated features were inaccurate.

## Install — Linux / Zorin / Kali

Python 3.10+ recommended. Run as your regular user; no sudo is needed by the app.
If your distribution lacks venv, install its `python3-venv` package first.

```bash
git clone https://github.com/zadwen/InfoHawk.git
cd InfoHawk
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run.sh
```

Open **http://127.0.0.1:8501**. Press Ctrl+C in the terminal to stop.
Do not use `--break-system-packages`.

## Windows PowerShell

```powershell
git clone https://github.com/zadwen/InfoHawk.git
cd InfoHawk
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Optional integrations

Install these independently with [pipx](https://pipx.pypa.io/stable/installation/):

```bash
pipx install sherlock-project
pipx install holehe
pipx ensurepath
```

Restart your terminal and InfoHawk so PATH changes take effect. The sidebar
shows whether each command is available. Their services may impose rate limits,
CAPTCHAs or change behavior. Runs stop after 120 seconds; captured output is
limited to 128 KiB and generated files are confined to a temporary directory.
Linux terminates the process group on timeout; Windows terminates the direct
process only. External integrations need separate compatibility checks whenever
the installed tool versions change.

For HIBP, enter your key in the masked sidebar field or set `HIBP_API_KEY` in
the launching shell. Do not commit keys. Keys are not included in reports or
passed to optional CLI processes. An API subscription is separate from this app.
A 404 means HIBP returned no record, not that an account is secure; 429 means
wait before retrying. Requests are never automatically repeated.

## Privacy and operation

The app binds to loopback by default. It has no multi-user authentication; keep
it local. DNS questions go to your resolver; HIBP receives the queried email;
optional tools contact their upstream services. Phone analysis is offline.
Reports contain the input and findings. Download only when you want to retain
them. Clearing a session does not erase prior downloads or upstream logs.
Use your own accounts or an authorized research scope.

## Development and verification

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The suite tests input validation, DNS failure distinctions, Null MX, HIBP error
handling, secret exclusion, CLI argument construction, reports and Streamlit
navigation. Network responses are mocked: these tests do not establish live
provider availability or the accuracy of third-party account matches.

## Upstream documentation

- [Streamlit](https://docs.streamlit.io/)
- [dnspython resolver](https://dnspython.readthedocs.io/en/stable/resolver-class.html)
- [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers)
- [email-validator](https://github.com/JoshData/python-email-validator)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [Sherlock](https://github.com/sherlock-project/sherlock)
- [Holehe](https://github.com/megadose/holehe)

See the existing LICENSE file for the repository's license statement.
