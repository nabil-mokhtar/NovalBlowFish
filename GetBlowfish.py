from os import urandom

from blowfish import Cipher
from helper_functions import bytes_to_image, pkcs7_pad, pkcs7_unpad, image_to_bytes


class GetBlowfish:

    def __init__(self, key1):
        self.cipher = Cipher(key1)
        self.iv = urandom(8)

    def encrypt_image(self, image_path, output_path):
        image_bytes = image_to_bytes(image_path)

        padded_image_bytes = pkcs7_pad(image_bytes)


        encrypted_bytes = bytearray()
        for i in range(0, len(padded_image_bytes), 8):
            block = padded_image_bytes[i:i + 8]
            encrypted_block = self.cipher.encrypt_cbc(block, self.iv)
            encrypted_bytes.extend(encrypted_block)

        bytes_to_image(encrypted_bytes, output_path)
        print(f"Encrypted image saved to {output_path}")
        return encrypted_bytes

    def decrypt_image(self, encrypted_image_path, output_path):
        encrypted_bytes = image_to_bytes(encrypted_image_path)

        decrypted_bytes = bytearray()
        for i in range(0, len(encrypted_bytes), 8):
            block = encrypted_bytes[i:i + 8]

            decrypted_block = self.cipher.decrypt_cbc(block, self.iv)
            decrypted_bytes.extend(decrypted_block)

        decrypted_bytes = pkcs7_unpad(decrypted_bytes)

        bytes_to_image(decrypted_bytes, output_path)
        print(f"Decrypted image saved to {output_path}")
        return decrypted_bytes

    def encrypt_text(self, data):
        data = data.encode()
        padded_data = pkcs7_pad(data)

        encrypted_bytes = bytearray()

        for i in range(0, len(padded_data), 8):
            block = padded_data[i:i + 8]
            encrypted_block = b"".join(self.cipher.encrypt_cbc(block, self.iv))
            encrypted_bytes.extend(encrypted_block)

        return encrypted_bytes

    def decrypt_text(self, data):

        decrypted_bytes = bytearray()

        for i in range(0, len(data), 8):
            block = data[i:i + 8]
            decrypted_block = b"".join(self.cipher.decrypt_cbc(block, self.iv))
            decrypted_bytes.extend(decrypted_block)

        unpadded_data = pkcs7_unpad(decrypted_bytes)

        return unpadded_data.decode()
