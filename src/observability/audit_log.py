from datetime import datetime
from hashlib import sha256
from typing import Dict


def audit(event_type: str, payload: Dict, actor: str):
    record = {
        "ts": datetime.utcnow().isoformat(),
        "actor": actor,
        "event_type": event_type,
        "payload": payload,
    }
    digest = sha256(str(record).encode("utf-8")).hexdigest()
    record["hash"] = digest
    # TODO: append to durable storage (event log)
    return record
