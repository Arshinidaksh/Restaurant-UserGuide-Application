import httpx

r = httpx.post("http://139.59.20.202:8000/capture", json={
    "route": "/settings",
    "actions": [
        {"type": "click", "selector": "button:has-text('Catalog'), div:has-text('Catalog'), a:has-text('Catalog')"},
        {"type": "wait", "ms": 2000}
    ]
}, timeout=60)
print("Catalog captured:", len(r.content))
with open("scratch/catalog_main.jpg", "wb") as f:
    f.write(r.content)
