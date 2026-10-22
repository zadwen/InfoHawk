"""Optional CLI adapters: argv-only execution, deadline, bounded output, temp cwd."""
import os
import shutil
import signal
import subprocess
import tempfile
import threading
from modules.utils import email_address, username

TOOLS = {'sherlock': 'sherlock-project', 'holehe': 'holehe'}
MAX_OUTPUT = 128 * 1024


def availability():
    return {name: bool(shutil.which(name)) for name in TOOLS}


def run_tool(tool, target, timeout=120):
    if tool not in TOOLS:
        raise ValueError('Unsupported tool.')
    target = username(target) if tool == 'sherlock' else email_address(target)
    executable = shutil.which(tool)
    if not executable:
        return {'status': 'not_installed', 'message': f'Install {TOOLS[tool]} with pipx, then restart InfoHawk.'}
    args = [executable, target]
    if tool == 'sherlock':
        args += ['--timeout', '10', '--print-found', '--no-color']
    output = bytearray()
    truncated = [False]
    # Isolate generated tool files, and do not pass API secrets into optional CLIs.
    env = {k: v for k, v in os.environ.items() if k in (
        'PATH', 'HOME', 'USERPROFILE', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP',
        'LANG', 'LC_ALL', 'SSL_CERT_FILE', 'SSL_CERT_DIR')}
    env['NO_COLOR'] = '1'
    with tempfile.TemporaryDirectory(prefix='infohawk-') as cwd:
        try:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    stdin=subprocess.DEVNULL, cwd=cwd, env=env,
                                    start_new_session=(os.name == 'posix'))
        except OSError:
            return {'status': 'launch_failed', 'message': 'Installed executable could not start.'}
        def drain():
            while True:
                block = proc.stdout.read(4096)
                if not block:
                    break
                remaining = MAX_OUTPUT - len(output)
                output.extend(block[:max(0, remaining)])
                if len(block) > remaining:
                    truncated[0] = True
        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                if os.name == 'posix':
                    os.killpg(proc.pid, signal.SIGKILL)
                else:
                    proc.kill()
            except ProcessLookupError:
                pass
            proc.wait()
        reader.join(timeout=5)
        if not reader.is_alive():
            proc.stdout.close()
        return {'status': 'timeout' if timed_out else ('ok' if proc.returncode == 0 else 'failed'),
                'tool': tool, 'target': target, 'exit_code': proc.returncode,
                'output': output.decode('utf-8', errors='replace'), 'output_truncated': truncated[0],
                'note': 'External-tool observations are unverified leads, not proof of identity or account ownership.'}
