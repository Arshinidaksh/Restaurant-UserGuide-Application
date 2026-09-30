import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('restaurant-app/app'))

from src.pos_data_builder import get_pos_full_data

data = get_pos_full_data()
chunks = data['chunks']
print(f"Total chunks in pos_data_builder: {len(chunks)}")
for c in chunks:
    print(f"{c['id']} | {c['part']} | {c['section']}")
