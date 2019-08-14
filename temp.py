import os
import time

from PIL import Image, ImageDraw
from pdf2image import convert_from_path
from pytesseract import image_to_string




def pdf_to_png(pdf_file_path, root, dpi=200):
    pages = convert_from_path(pdf_file_path, dpi)
    count = 1
    os.chdir(root)
    for page in pages:
        page.save(str(count) + ".png", "PNG")
        count += 1


def threshold(png, value=600):
    image = Image.open(png)
    draw = ImageDraw.Draw(image)
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()

    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            S = r + g + b
            if S > value:
                draw.point((i, j), (255, 255, 255))
    image.save(png)


def png_threshold(root):
    os.chdir(root)
    pages = os.listdir(root)
    for page in pages:
        threshold(page)


def png_to_txt(root):
    os.chdir(root)
    pages = os.listdir(root)
    pages.sort()
    text = ''
    for page in pages:
        text += image_to_string(Image.open(page), 'rus')
    process_text(root, text)


def process_file(pdf_file_path):
    root, ext = os.path.splitext(pdf_file_path)
    os.mkdir(root)
    pdf_to_png(pdf_file_path,root)
    png_threshold(root)
    png_to_txt(root)


def process_all_files(start_dir):
    file_iterator = os.walk(start_dir)
    files = []
    count = 1
    for items in file_iterator:
        print(items)
        for file in items[2]:
            print(str(count) + ' ' + items[0] + '/' + file)
            files.append(items[0] + '/' + file)
            count += 1
    for f in files:
        process_file(f)


def process_text(name,text):
    print(text)
    os.chdir(name)
    f = open(name + '.txt', 'w')
    f.write(text)
    f.close()


t1 = time.time()
process_all_files('/home/k3l/Рабочий стол')
t2 = time.time()
print(t2 - t1)