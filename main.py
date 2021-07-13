import time
from PIL import Image
import os

dirname = os.path.dirname(__file__)
default_watermark_dir = os.path.join(dirname, "default_watermark")
full_watermark_dir = os.path.join(dirname, "full_watermark")


def left_top(base_image_size, watermark_size):
    x = watermark_size[0]
    y = watermark_size[1]
    return x, y


def right_top(base_image_size, watermark_size):
    x = base_image_size[0] - watermark_size[0]
    y = watermark_size[1]
    return x, y


def left_bottom(base_image_size, watermark_size):
    x = watermark_size[0]
    y = base_image_size[1] - watermark_size[1]
    return x, y


def right_bottom(base_image_size, watermark_size):
    x = base_image_size[0] - watermark_size[0]
    y = base_image_size[1] - watermark_size[1]
    return x, y


def middle(base_image_size, watermark_size):
    x = base_image_size[0] // 2
    y = base_image_size[1] // 2
    return x, y


def paste(base_image, watermark, position, fully=False):
    if base_image.mode == 'RGBA':
        pass
    else:
        base_image = base_image.convert('RGBA')

    if watermark.mode == 'RGBA':
        pass
    else:
        watermark = watermark.convert('RGBA')

    watermark_width = base_image.width // 10
    watermark_height = base_image.height // 10
    watermark = watermark.resize(size=(watermark_width, watermark_height))

    position = positions[position](base_image.size, watermark.size)

    watermark = watermark.copy()
    base_image = base_image.copy()
    if fully:
        for x in range(watermark_width, base_image.width, watermark_width * 2):
            for y in range(watermark_height, base_image.height, watermark_height * 2):
                position = (x, y)
                base_image.paste(watermark, position, watermark)
    else:
        base_image.paste(watermark, position, watermark)
    global dirname
    save_path = os.path.join(dirname, 'done')
    base_image.save(save_path + '/' + "wm_" + base_image_name + ".png", "PNG", quality=75)


positions = {

    1: left_top,
    2: right_top,
    3: left_bottom,
    4: right_bottom,
    5: middle,

}

print("File with watermark should have transparent background")
print("Place the watermark image in the program folder")
while True:
    try:
        watermark_name = input("\x1b[1mEnter name of the watermark image\n")
        watermark_path = os.path.join(dirname, watermark_name)
        f = open(watermark_path)
        f.close()
        break
    except FileNotFoundError:
        print("\x1b[31;1mFile not found\x1b[39;49m")
        print("Enter filename with an extension")
        pass
print("watermark will be inserted in all images from folders default_watermark and full_watermark")
time.sleep(2)
while True:
    try:
        position = input("\x1b[1mEnter position for watermark \n"
                         "1 - left top/2 - right top/3 - left bottom/ 4 - right bottom/5 - in the middle]\n")
        position = int(position)
        if position in range(0, 6): break
    except ValueError:
        pass

print("Processing...\n")
for image in os.listdir(default_watermark_dir):
    base_image_name = image.split(".")[0]
    base_image = Image.open(default_watermark_dir + "/" + image)
    watermark = Image.open(watermark_path)
    paste(base_image, watermark, position)

for image in os.listdir(full_watermark_dir):
    base_image_name = image.split(".")[0]
    base_image = Image.open(full_watermark_dir + "/" + image)
    watermark = Image.open(watermark_path)
    paste(base_image, watermark, position, True)

print("Successfully")
