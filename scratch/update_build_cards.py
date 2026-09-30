import re

file_path = 'scripts/build_full_slides_and_export.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

icon_map = {
    'POS-A01': ['monitor', 'key', 'doc_tax', 'shield_lock'],
    'POS-C01': ['power', 'storefront', 'wifi', 'cash_money'],
    'POS-D03': ['save_disk', 'kds_screen', 'kitchen_printer', 'bill_preview'],
    'POS-D04': ['table_move', 'table_merge', 'bill_split', 'floor_zones'],
    'POS-E03': ['coupon_percent', 'gift_card', 'loyalty_star', 'pos_terminal'],
    'POS-M01': ['receipt_printer', 'kitchen_printer', 'network_routing', 'slip_template'],
    'POS-S01': ['export_arrow', 'import_arrow', 'cloud_sync', 'db_clean'],
    'POS-V01': ['tax_gov', 'team_roles', 'menu_book', 'test_checklist']
}

for s_id, icons in icon_map.items():
    # Find the section in content
    pattern = rf'("{s_id}":\s*\{{.*?"cards":\s*\[)(.*?)(\]\s*\}})'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        cards_block = match.group(2)
        # Find all individual card dicts: {"step": ..., "title": ..., "description": ...}
        card_pattern = r'(\{\s*"step":\s*"[^"]+",\s*"title":\s*"[^"]+",\s*"description":\s*"[^"]+")(\s*\})'
        card_matches = list(re.finditer(card_pattern, cards_block))
        if len(card_matches) == len(icons):
            new_cards_block = cards_block
            # Replace in reverse order so string offsets stay valid
            for i in reversed(range(len(icons))):
                cm = card_matches[i]
                replacement = f'{cm.group(1)},\n                "icon": "{icons[i]}"{cm.group(2)}'
                new_cards_block = new_cards_block[:cm.start()] + replacement + new_cards_block[cm.end():]
            content = content[:match.start(2)] + new_cards_block + content[match.end(2):]
            print(f"Updated cards for {s_id}")
        else:
            print(f"Warning: card count mismatch for {s_id}: found {len(card_matches)}, expected {len(icons)}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scripts/build_full_slides_and_export.py successfully!")
