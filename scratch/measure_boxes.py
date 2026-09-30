from PIL import Image

def find_text_box(img_path):
    im = Image.open(img_path)
    print(f"Image {img_path}:")

# Let's inspect J_accounts for Day Close
im_j = Image.open("project/screens_parts_fk/J_accounts.jpg")
# The Day Close tile is in Accounts modules (second row or first row?)
# Let's crop around x=1300 to 1800, y=180 to 320 to see Day Close
im_j_crop = im_j.crop((1400, 180, 1850, 320))
im_j_crop.save("scratch/crop_day_close.jpg")
print("Saved crop_day_close.jpg")

# In K_settings, let's see left sub-tabs
im_k = Image.open("project/screens_parts_fk/K_settings_live.jpg")
im_k_crop = im_k.crop((50, 140, 200, 600))
im_k_crop.save("scratch/crop_k_tabs.jpg")
print("Saved crop_k_tabs.jpg")

# In G_online, let's see QR menu link button and HungerStation card
im_g = Image.open("project/screens_parts_fk/G_online.jpg")
# QR menu link is at top right
im_g_crop1 = im_g.crop((1200, 60, 1800, 140))
im_g_crop1.save("scratch/crop_g_buttons.jpg")
# HungerStation card
im_g_crop2 = im_g.crop((50, 200, 450, 560))
im_g_crop2.save("scratch/crop_g_card.jpg")
print("Saved G crops")

# In H_kitchen, let's see boards
im_h = Image.open("project/screens_parts_fk/H_kitchen_kot_live.jpg")
im_h_crop = im_h.crop((50, 120, 400, 200))
im_h_crop.save("scratch/crop_h_boards.jpg")
print("Saved H crop")

# In I_riders, let's see riders
im_i = Image.open("project/screens_parts_fk/I_delivery_riders_view.jpg")
im_i_crop = im_i.crop((50, 120, 500, 200))
im_i_crop.save("scratch/crop_i_riders.jpg")
print("Saved I crop")
