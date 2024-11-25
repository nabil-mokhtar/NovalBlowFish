from PIL import Image


def pkcs7_pad(data, block_size=8):
    # Calculate the number of bytes needed to pad to the block size
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len]) * padding_len  # e.g., 05 05 05 05 05 for 5 padding bytes
    return data + padding


def pkcs7_unpad(data):
    # Get the last byte which represents the padding length
    padding_len = data[-1]
    return data[:-padding_len]


def image_to_bytes(image_path):
    # Open image and convert it to bytes
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    return image_bytes


def bytes_to_image(image_bytes, output_path):
    # Convert bytes back to an image and save it
    with open(output_path, 'wb') as output_file:
        output_file.write(image_bytes)


