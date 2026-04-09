
import random

def generate_seed_events(n=12):
    events = []
    for i in range(n):
        events.append({
            "id": f"event_{i}",
            "type": "suppression" if i < int(n * 0.7) else "forward",
            "location": (random.random() * 100, random.random() * 100),
            "priority": 1 if i < int(n * 0.7) else 2,
        })
    return events
  
