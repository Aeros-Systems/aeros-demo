import math
from typing import Dict, Any

class Engine:
def **init**(self):
self.tasks: Dict[str, Dict[str, Any]] = {}
self.nodes: Dict[str, Dict[str, Any]] = {}
self.resources = 1.0
self.continuity = "NORMAL"

```
    # HiveMind placeholder (future expansion)
    self.hivemind = {
        "task_history": []
    }

# -----------------------------
# INGESTION
# -----------------------------
def ingest_node(self, node_id: str, role: str, position=(0.0, 0.0), priority: int = 1):
    self.nodes[node_id] = {
        "role": role,
        "position": tuple(position),
        "priority": priority,
        "active": True,
    }

def ingest_event(self, event: Dict[str, Any]):
    self.tasks[event["id"]] = {
        "type": event.get("type", "suppression"),
        "location": tuple(event["location"]),
        "priority": int(event.get("priority", 1)),
        "status": "PENDING",
        "assigned": None,
        "progress": 0.0,
    }

# -----------------------------
# CORE UTILS
# -----------------------------
def _distance(self, a, b) -> float:
    return math.dist(a, b)

def _update_continuity(self):
    active = sum(1 for n in self.nodes.values() if n["active"])
    if active < 2:
        self.continuity = "FRACTURED"
    elif active < 4:
        self.continuity = "DEGRADED"
    else:
        self.continuity = "NORMAL"

def _validation_score(self, task: Dict[str, Any]) -> float:
    if "location" not in task:
        return 0.0
    base = 0.8 if task["type"] == "forward" else 0.7
    return min(1.0, base)

def _reinforcement_request(self):
    pending = sum(1 for t in self.tasks.values() if t["status"] == "PENDING")
    if pending > 12 or self.resources < 0.3:
        return {"request": True, "type": "SUPPRESSION", "urgency": "HIGH"}
    return {"request": False}

# -----------------------------
# Hivemind Scoring Engine
# -----------------------------
def _score(self, node: Dict[str, Any], task: Dict[str, Any], distance: float) -> float:

    # ---- BENEFIT ----
    human_gain = 1.0 if task["type"] == "forward" else 0.7
    containment = 0.8
    continuity = 0.6

    benefit = (
        3.0 * human_gain +
        2.0 * containment +
        1.5 * continuity
    )

    # ---- RISK ----
    platform_loss = min(1.0, distance / 100)
    escalation = 0.2

    risk = (
        1.5 * platform_loss +
        1.0 * escalation
    )

    # ---- TIME COST ----
    time_cost = distance * 0.05

    # ---- CONFIDENCE ----
    confidence = 0.8  # placeholder (future Sentinel validation)

    # ---- FINAL SCORE ----
    score = (benefit * confidence) - risk - time_cost

    # ---- HUMAN PRIORITY OVERRIDE ----
    if task["type"] == "forward":
        score += 100  # enforce survivability-first doctrine

    return score

# -----------------------------
# MAIN STEP LOOP
# -----------------------------
def step(self) -> Dict[str, Any]:

    self._update_continuity()
    self.resources = max(0.0, self.resources - 0.01)

    active_nodes = [
        (nid, n) for nid, n in self.nodes.items()
        if n["active"]
    ]

    # -----------------------------
    # TASK ASSIGNMENT (UPGRADED)
    # -----------------------------
    for tid, t in sorted(self.tasks.items(), key=lambda kv: -kv[1]["priority"]):

        if t["status"] != "PENDING":
            continue

        if self._validation_score(t) < 0.5:
            continue

        best_id = None
        best_score = -10**9

        for nid, n in active_nodes:
            d = self._distance(n["position"], t["location"])
            score = self._score(n, t, d)

            if score > best_score:
                best_score = score
                best_id = nid

        if best_id is not None and self.resources > 0.05:
            t["assigned"] = best_id
            t["status"] = "ACTIVE"

    # -----------------------------
    # TASK PROGRESSION
    # -----------------------------
    for t in self.tasks.values():
        if t["status"] == "ACTIVE":
            inc = 0.28 if t["type"] == "forward" else 0.18
            t["progress"] += inc

            if t["progress"] >= 1.0:
                t["status"] = "DONE"

                # HiveMind memory capture (future learning layer)
                self.hivemind["task_history"].append({
                    "type": t["type"],
                    "assigned": t["assigned"],
                    "completion": t["progress"]
                })

    # -----------------------------
    # OUTPUT STATE
    # -----------------------------
    return {
        "cycle_state": {
            "done": sum(1 for t in self.tasks.values() if t["status"] == "DONE"),
            "active": sum(1 for t in self.tasks.values() if t["status"] == "ACTIVE"),
            "pending": sum(1 for t in self.tasks.values() if t["status"] == "PENDING"),
            "continuity": self.continuity,
            "resources": round(self.resources, 3),
            "reinforcement": self._reinforcement_request(),
        },
        "tasks": self.tasks,
        "nodes": self.nodes,
    }
```
