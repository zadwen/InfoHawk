#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ ! -x .venv/bin/python ]]; then
  echo 'First run: python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt' >&2
  exit 1
fi
exec .venv/bin/python -m streamlit run app.py --server.address=127.0.0.1 "$@"
