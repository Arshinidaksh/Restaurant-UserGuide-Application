from PIL import Image

def analyze(name, path):
    im = Image.open(path)
    print(f"{name}: size={im.size}")

analyze("F_takeaway", "project/screens_parts_fk/F_takeaway_ticket_open.jpg")
analyze("G_online", "project/screens_parts_fk/G_online.jpg")
analyze("H_kitchen", "project/screens_parts_fk/H_kitchen_kot_live.jpg")
analyze("I_riders", "project/screens_parts_fk/I_delivery_riders_view.jpg")
analyze("J_accounts", "project/screens_parts_fk/J_accounts.jpg")
analyze("K_settings", "project/screens_parts_fk/K_settings_live.jpg")
