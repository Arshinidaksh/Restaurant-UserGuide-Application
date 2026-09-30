from PIL import Image

im = Image.open("Slides/Part H/Part H - Kitchen screen (Kitchen Manager).jpg")
print("Slide size:", im.size)
# The monitor screen inside the slide is scaled down!
# Let's crop the screen from H_kitchen_kot_live.jpg vs the generated slide
im_h = Image.open("project/screens_parts_fk/H_kitchen_kot_live.jpg")
print("Original size:", im_h.size)
