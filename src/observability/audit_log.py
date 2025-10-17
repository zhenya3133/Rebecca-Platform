import datetime
import hashlib
import json


def audit(event_type: str, payload: dict, actor: str, blockchain_log: bool = False):
    ts = datetime.datetime.utcnow().isoformat()
    data = {
        "ts": ts,
        "actor": actor,
        "event_type": event_type,
        "payload": payload,
    }
    record = json.dumps(data, sort_keys=True)
    hash_val = hashlib.sha256(record.encode("utf-8")).hexdigest()
    data["hash"] = hash_val

    with open("audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, sort_keys=True) + "\n")

    if blockchain_log:
        with open("onchain_audit_hashes.txt", "a", encoding="utf-8") as f:
            f.write(hash_val + "\n")
    return hash_val
