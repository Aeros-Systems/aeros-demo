
from flask import Flask, render_template, jsonify, request
from core.engine import Engine
from integration.event_bridge import generate_seed_events

app = Flask(__name__)
engine = Engine()

# seed nodes (platoon-like representatives)
engine.ingest_node("A", "suppression", (10, 10), priority=2)
engine.ingest_node("B", "suppression", (40, 25), priority=2)
engine.ingest_node("C", "suppression", (70, 15), priority=2)
engine.ingest_node("D", "corridor", (20, 70), priority=1)
engine.ingest_node("E", "forward", (75, 75), priority=3)

for e in generate_seed_events(18):
    engine.ingest_event(e)

cycle = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    result = engine.step()
    return jsonify(result)

@app.route("/add_event", methods=["POST"])
def add_event():
    payload = request.get_json(force=True)
    event = {
        "id": f"manual_{len(engine.tasks)+1}",
        "type": payload.get("type", "suppression"),
        "location": (float(payload["x"]), float(payload["y"])),
        "priority": 2 if payload.get("type") == "forward" else 1,
    }
    engine.ingest_event(event)
    return jsonify({"ok": True, "event": event})

if __name__ == "__main__":
    app.run(debug=True)
