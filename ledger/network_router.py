import random

def route_transaction(entry, network):
    if network == "ACH":
        return {"network": "ACH", "batch_id": f"BATCH-{entry['token'][:16]}", "amount_cents": int(entry["amount_usd"]*100),
                "reference": entry["token"], "status": random.choice(["PENDING","SETTLED"])}
    if network == "SWIFT":
        return {"network": "SWIFT", "amount": entry["amount_usd"], "reference": entry["token"][:16],
                "status": random.choice(["QUEUED","SETTLED"])}
    if network == "STRIPE":
        return {"network": "STRIPE", "amount": int(entry["amount_usd"]*100), "metadata":{"ledger_id":entry["token"][:16]},
                "status": random.choice(["CREATED","SETTLED"])}
    if network == "PAYPAL":
        return {"network": "PAYPAL", "amount": entry["amount_usd"], "ledger_ref": entry["token"][:16],
                "instant": True, "status": random.choice(["INSTANT","SETTLED"])}