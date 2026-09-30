import re

with open('scripts/build_full_slides_and_export.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect where cards are defined
matches = [m.start() for m in re.finditer(r'"cards":\s*\[', content)]
print(f"Found {len(matches)} card arrays in build_full_slides_and_export.py")

for idx, pos in enumerate(matches):
    start = max(0, pos - 200)
    end = min(len(content), pos + 800)
    snippet = content[start:end]
    slide_m = re.findall(r'"(POS-[A-Z0-9]+)":', snippet)
    print(f"Slide: {slide_m[0] if slide_m else 'unknown'}")
