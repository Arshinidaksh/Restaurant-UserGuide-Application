from PIL import Image

im_f = Image.open("project/screens_parts_fk/F_takeaway_ticket_open.jpg")
# queue crop
im_f_crop = im_f.crop((50, 130, 550, 210))
im_f_crop.save("scratch/crop_f_queue.jpg")
# header badge
im_f_crop2 = im_f.crop((50, 210, 400, 320))
im_f_crop2.save("scratch/crop_f_header.jpg")
print("Saved F crops")
