from PIL import Image

im_k = Image.open("project/screens_parts_fk/K_settings_live.jpg")
im_k_crop = im_k.crop((240, 180, 650, 520))
im_k_crop.save("scratch/crop_k_tiles.jpg")
print("Saved K tiles crop")
