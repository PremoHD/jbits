import networkx as nx
import matplotlib.pyplot as plt

def build_ledger_graph(canonical_entries, network_outputs):
    G = nx.DiGraph()
    for entry in canonical_entries:
        G.add_node(entry["token"][:16], amount=int(entry["amount_usd"]*100), owner="Justus Ellis")
    for net_tx in network_outputs:
        source = net_tx.get("ledger_ref") or net_tx["metadata"]["ledger_id"]
        G.add_edge(source, f"{net_tx['network']}_OUT_{net_tx['status']}", amount=net_tx.get("amount_cents", net_tx.get("amount",0)))
    return G

def visualize_graph(G, filename="ledger_graph.png"):
    plt.figure(figsize=(20,10))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, arrowsize=15)
    plt.savefig(filename)
    plt.close()