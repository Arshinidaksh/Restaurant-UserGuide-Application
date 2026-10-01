import httpx

tabs = ["Catalog", "User", "Accounts", "Ingredients", "Inventory", "Database"]
for t in tabs:
    r = httpx.post("http://139.59.20.202:8000/capture", json={
        "route": "/settings",
        "actions": [
            {"type": "click", "selector": f"aside button:has-text('{t}'), nav button:has-text('{t}'), button:has-text('{t}')"},
            {"type": "wait", "ms": 2000}
        ]
    }, timeout=60)
    print(f"Captured {t}:", len(r.content))
    with open(f"scratch/tab_{t.lower()}.jpg", "wb") as f:
        f.write(r.content)
