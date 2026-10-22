"""In-memory reports: saving to disk is an explicit browser download."""
import json
from datetime import datetime, timezone
from uuid import uuid4


def make_report(module, target, result):
    return {'id': uuid4().hex, 'application': 'InfoHawk', 'version': '4.0.0',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'module': module, 'target': target, 'result': result}


def export_json(reports):
    return json.dumps(reports, indent=2, ensure_ascii=False)
