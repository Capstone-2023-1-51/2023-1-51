import glob
import os
from PIL import Image

push = {'60': 1, '61': 2, '62': 3, '63': 4, '64': 5, '65': 6, '66': 7, '67': 8, '68': 9, '69': 10,
        '6A': 11, '6B': 12, '6C': 13, '6D': 14, '6E': 15, '6F': 16, '70': 17, '71': 18, '72': 19, '73': 20,
        '74': 21, '75': 22, '76': 23, '77': 24, '78': 25, '79': 26, '7A': 27, '7B': 28, '7C': 29, '7D': 30,
        '7E': 31, '7F': 32}


def extract_label_bytecode(file):
    with open(file, 'r', encoding='UTF8') as f:
        bytecode = f.read()

    arr = bytecode.split(',')
    label = arr[0]
    bytecode = arr[1]
    return label, bytecode


# 바이트 단위로 나눠 RGB값 지정
def create_pixels(bytecode):
    pixel_colors = []
    i = 0
    push_keys = push.keys()
    while i < len(bytecode):
        byte = bytecode[i:i + 2]
        i += 2
        r = int(byte, 16)
        g = 0
        b = 0
        if byte in push_keys:
            g = int(bytecode[i:i + 2], 16)
            i += 2
            n = push[byte]
            if n != 1:
                b = int(bytecode[i:i + 2], 16)
                i += 2 * (n - 1)
        pixel_colors.append((r, g, b))
    return pixel_colors


def create_image(file_name, pixel_colors):
    width = len(pixel_colors)
    if width != 0:
        image = Image.new('RGB', (width, 1))  # 이미지 생성
        pixels = pixel_colors   # 픽셀 색상 설정
        image.putdata(pixels)   # 이미지에 픽셀 색상 적용
        gray_image = image.convert("L")
        gray_image.save('./images/' + file_name + '.png')


def bytecode_to_image(folder_path):
    files = glob.glob(folder_path + '/*.bin')

    for file in files:
        file_name = (os.path.basename(file)).split('.')[0]
        label, bytecode = extract_label_bytecode(file)
        print(label)
        pixel_colors = create_pixels(bytecode)
        create_image(file_name, pixel_colors)