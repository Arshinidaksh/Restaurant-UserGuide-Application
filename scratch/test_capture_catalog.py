import httpx

client = httpx.Client(timeout=60.0)
resp = client.post("http://139.59.20.202:8000/capture", json={
    "route": "/settings",
    "actions": [
        {"type": "click", "selector": "text=Catalog"},
        {"type": "wait", "ms": 1500}
    ]
})

print("Catalog captured:", resp.status_code, len(resp.content))
with open("scratch/tab_catalog_fresh.jpg", "wb") as f:
    f.write(resp.content)
