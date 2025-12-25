from datetime import datetime
import hashlib, random

def generate_ledger_batch(num_tx=500):
    ledger_entries = []
    for i in range(num_tx):
        raw_ref = f"{random.randint(1000000,9999999)}⑈{random.randint(100000000,999999999)}⑆{random.randint(1000000,9999999)}"
        amount_usd = random.randint(500,10000)
        token = hashlib.sha256(raw_ref.encode()).hexdigest()
        hash_ = hashlib.sha256((token + datetime.utcnow().isoformat()).encode()).hexdigest()
        ledger_entries.append({
            "raw_ref": raw_ref,
            "owner": "Justus Ellis",
            "amount_usd": amount_usd,
            "timestamp": datetime.utcnow().isoformat(),
            "token": token,
            "hash": hash_
        })
    return ledger_entries