import base64


def image2str(image):
    with open(image, 'rb') as f:
        image_byte = base64.b64encode(f.read())
    image_str = image_byte.decode('ascii')  # byte类型转换为str

    return image_str


def str2image(str):
    image_str = str.encode('ascii')
    image_byte = base64.b64decode(image_str)

    return image_byte
