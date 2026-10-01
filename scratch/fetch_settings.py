import httpx

r = httpx.post("http://139.59.20.202:8000/capture", json={"route": "/settings"}, timeout=60)
print("Settings captured:", len(r.content))
with open("scratch/settings_main.jpg", "wb") as f:
    f.write(r.content)
