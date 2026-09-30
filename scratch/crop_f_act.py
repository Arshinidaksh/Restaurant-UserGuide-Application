from PIL import Image

im_f = Image.open("project/screens_parts_fk/F_takeaway_ticket_open.jpg")
im_f_crop = im_f.crop((1500, 210, 1910, 280))
im_f_crop.save("scratch/crop_f_actions.jpg")
print("Saved F action crop")
