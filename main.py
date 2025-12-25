from ledger.ledger_generator import generate_ledger_batch
from ledger.network_router import route_transaction
from ledger.ledger_graph import build_ledger_graph, visualize_graph

# 1️⃣ Generate huge batch
ledger_entries = generate_ledger_batch(500)

# 2️⃣ Normalize (for routing)
canonical_entries = [{"token":e["token"], "amount_usd":e["amount_usd"]} for e in ledger_entries]

# 3️⃣ Push to networks
network_outputs = []
for entry in canonical_entries:
    for net in ["ACH","SWIFT","STRIPE","PAYPAL"]:
        network_outputs.append(route_transaction(entry, net))

# 4️⃣ Generate ledger graph
G = build_ledger_graph(canonical_entries, network_outputs)
visualize_graph(G, "ledger_graph.png")

print("✅ Large batch simulation complete. Graph saved as ledger_graph.png")