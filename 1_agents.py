# 1_agents.py
import uuid
from ledger import log_agent_trade

class Agent:
    def __init__(self, task, parent_id=None, network="default"):
        self.id = str(uuid.uuid4())
        self.task = task
        self.parent_id = parent_id
        self.status = "running"
        self.result = None
        self.upgrades_applied = []
        self.children = []
        self.network = network

    def apply_upgrades(self, upgrades):
        """Apply upgrades: mirror, invert, negative, mobius, auto-replicate, multi-network"""
        self.upgrades_applied.extend(upgrades)

    def run_task(self, intent):
        """Execute task and log to multi-ledger using JBits"""
        self.result = f"Executed {self.task}"
        log_agent_trade(self.id, intent, self.upgrades_applied)

    def spawn_child(self, task, intent, upgrades=None, network="default"):
        child = Agent(task, parent_id=self.id, network=network)
        if upgrades:
            child.apply_upgrades(upgrades)
        child.run_task(intent)
        self.children.append(child)
        return child