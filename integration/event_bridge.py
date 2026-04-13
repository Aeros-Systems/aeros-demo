import random

def generate_seed_events(n=12):

```
events = []

# Create 1–2 hotspot clusters (more realistic fire behavior)
clusters = [
    (random.uniform(20, 40), random.uniform(20, 40)),
    (random.uniform(60, 80), random.uniform(60, 80))
]

for i in range(n):

    # Assign cluster or random spread
    if random.random() < 0.7:
        cx, cy = random.choice(clusters)
        x = cx + random.uniform(-10, 10)
        y = cy + random.uniform(-10, 10)
    else:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)

    # Clamp to map bounds
    x = max(0, min(100, x))
    y = max(0, min(100, y))

    is_forward = i >= int(n * 0.7)

    events.append({
        "id": f"event_{i}",
        "type": "forward" if is_forward else "suppression",
        "location": (x, y),
        "priority": 2 if is_forward else 1,
    })

return events
```

  
