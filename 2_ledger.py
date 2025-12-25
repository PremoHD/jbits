# 2_ledger.py
import csv, os, uuid, hashlib
from datetime import datetime

LEDGER_FILES = {
    "original": "data/ledger_original.csv",
    "mirror": "data/ledger_mirror.csv",
    "invert": "data/ledger_invert.csv",
    "branches": "data/ledger_branches.csv"
}

os.makedirs("data", exist_ok=True)

def log_ledger(entry: dict):
    branch_type = entry.get("branch_type","original")
    file_path = LEDGER_FILES.get(branch_type, LEDGER_FILES["original"])

    if not os.path.exists(file_path):
        with open(file_path,"w",newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp","type","source","destination","asset","amount","fee","net",
                "tx_id","hash","network","notes"
            ])
            writer.writeheader()

    now = datetime.utcnow().isoformat()
    tx_id = str(uuid.uuid4())
    amount = float(entry.get("amount",0))
    fee = float(entry.get("fee",0))
    net = amount - fee
    if entry.get("type")=="expense" and net>0:
        net = -net

    row = {
        "timestamp": now,
        "type": entry.get("type","income"),
        "source": entry.get("source",""),
        "destination": entry.get("destination",""),
        "asset": entry.get("asset","USD"),
        "amount": amount,
        "fee": fee,
        "net": net,
        "tx_id": tx_id,
        "network": entry.get("network","default"),
        "notes": entry.get("notes","")
    }

    hash_input = f"{tx_id}-{row['source']}-{net}-{now}".encode()
    row["hash"] = hashlib.sha256(hash_input).hexdigest()

    with open(file_path,"a",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)

    return row

def log_agent_trade(agent_id, intent, upgrades=[]):
    """Log a trade across Original, Mirror, Invert, Branches ledgers"""
    entries = []

    # Original
    entries.append(log_ledger({
        "type": "income" if intent["side"]=="BUY" else "expense",
        "amount": intent["amountUSD"],
        "source": agent_id,
        "notes": ", ".join(upgrades),
        "branch_type": "original",
        "network": "default"
    }))

    # Mirror
    if "mirror" in upgrades:
        entries.append(log_ledger({
            "type": "income" if intent["side"]=="BUY" else "expense",
            "amount": intent["amountUSD"],
            "source": agent_id,
            "notes": "mirror",
            "branch_type": "mirror",
            "network": "default"
        }))

    # Invert
    if "invert" in upgrades:
        amount = -intent["amountUSD"]
        entries.append(log_ledger({
            "type": "income" if amount>0 else "expense",
            "amount": abs(amount),
            "source": agent_id,
            "notes": "invert",
            "branch_type": "invert",
            "network": "default"
        }))

    # Branches
    if any(u in upgrades for u in ["mobius","negative","multi-network"]):
        net = intent["amountUSD"]
        if "negative" in upgrades: net = -net
        if "mobius" in upgrades: net = 0
        entries.append(log_ledger({
            "type": "income" if net>0 else "expense",
            "amount": abs(net),
            "source": agent_id,
            "notes": ", ".join([u for u in upgrades if u in ["mobius","negative","multi-network"]]),
            "branch_type": "branches",
            "network": "A" if "multi-network" in upgrades else "default"
        }))

    return entries