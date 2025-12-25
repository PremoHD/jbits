# 3_main.py
from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from agents import Agent
from ledger import log_agent_trade
import os, json
import networkx as nx
import plotly.graph_objects as go

os.makedirs("data", exist_ok=True)
AGENTS_FILE = "data/agents_snapshot.json"

app = FastAPI(title="JBits Agent Smith System")
agents_list = []

# Save/load agents
def save_agents(agent_list):
    data = [agent_to_dict(a) for a in agent_list]
    with open(AGENTS_FILE,"w") as f: json.dump(data,f,indent=2)

def load_agents():
    if not os.path.exists(AGENTS_FILE): return []
    with open(AGENTS_FILE,"r") as f: data = json.load(f)
    return [dict_to_agent(d) for d in data]

def agent_to_dict(agent):
    return {"id":agent.id,"task":agent.task,"parent_id":agent.parent_id,"status":agent.status,
            "result":agent.result,"network":agent.network,"upgrades_applied":agent.upgrades_applied,
            "children":[agent_to_dict(c) for c in agent.children]}

def dict_to_agent(d):
    agent = Agent(d["task"], parent_id=d["parent_id"], network=d.get("network","default"))
    agent.id=d["id"]; agent.status=d.get("status","running"); agent.result=d.get("result")
    agent.upgrades_applied=d.get("upgrades_applied",[]); agent.children=[dict_to_agent(c) for c in d.get("children",[])]
    return agent

# Agent DAG visualization
def build_graph(agent_list):
    G = nx.DiGraph()
    def add_node_recursive(agent):
        G.add_node(agent.id,label=agent.task, upgrades=", ".join(agent.upgrades_applied), network=agent.network)
        for c in agent.children:
            G.add_edge(agent.id,c.id)
            add_node_recursive(c)
    for a in agent_list: add_node_recursive(a)
    return G

def draw_dag_graph(G):
    pos = nx.spring_layout(G)
    edge_x,edge_y=[],[]
    for e in G.edges():
        x0,y0=pos[e[0]]; x1,y1=pos[e[1]]
        edge_x.extend([x0,x1,None]); edge_y.extend([y0,y1,None])
    edge_trace=go.Scatter(x=edge_x,y=edge_y,line=dict(width=1,color='#888'),hoverinfo='none',mode='lines')
    node_x,node_y,node_text=[],[],[]
    for n in G.nodes():
        x,y=pos[n]; node_x.append(x); node_y.append(y)
        node_text.append(f"{G.nodes[n]['label']} ({G.nodes[n]['upgrades']}) [{G.nodes[n]['network']}]")
    node_trace=go.Scatter(x=node_x,y=node_y,mode='markers+text',text=node_text,hoverinfo='text',
                          marker=dict(color='lightblue',size=20,line_width=2))
    fig=go.Figure(data=[edge_trace,node_trace])
    fig.update_layout(showlegend=False)
    return fig.to_html(full_html=False)

@app.get("/", response_class=HTMLResponse)
def dashboard():
    G = build_graph(agents_list)
    dag_html = draw_dag_graph(G)
    html_content = f"<html><head><title>JBits Dashboard</title></head><body><h1>Agent DAG</h1>{dag_html}</body></html>"
    return HTMLResponse(html_content)

@app.post("/spawn_agent")
async def spawn_agent(request: Request):
    data = await request.json()
    task = data.get("task","Default Task")
    upgrades = data.get("upgrades",[])
    intent = data.get("intent",{"side":"BUY","amountUSD":100,"price":0})
    agent = Agent(task)
    agent.apply_upgrades(upgrades)
    agent.run_task(intent)
    agents_list.append(agent)
    save_agents(agents_list)
    return {"message":"Agent spawned","id":agent.id}

@app.post("/log_agent_trade")
def log_agent_trade_endpoint(data: dict = Body(...)):
    agent_id = data.get("agent_id")
    intent = data.get("intent")
    upgrades = data.get("upgrades",[])
    entries = log_agent_trade(agent_id,intent,upgrades)
    return {"message":"Logged to ledgers","entries":entries}