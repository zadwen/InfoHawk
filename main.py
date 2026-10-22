"""Compatibility launcher: python main.py."""
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    raise SystemExit(subprocess.call([sys.executable, '-m', 'streamlit', 'run',
                                     str(Path(__file__).with_name('app.py')),
                                     '--server.address=127.0.0.1']))
