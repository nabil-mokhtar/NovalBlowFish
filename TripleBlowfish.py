from os import urandom
from blowfish import Cipher
from helper_functions import image_to_bytes, pkcs7_pad, bytes_to_image, pkcs7_unpad


class TripleBlowfish:
    def __init__(self, key1, key2, key3):
        self.cipher1 = Cipher(key1)
        self.cipher2 = Cipher(key2)
        self.cipher3 = Cipher(key3)

    def encrypt(self, data):
        # Generate IV for this session
        iv = urandom(8)

        # Triple encryption
        data_encrypted = b"".join(self.cipher1.encrypt_cbc(data, iv))
        data_decrypted = b"".join(self.cipher2.decrypt_cbc(data_encrypted, iv))
        data_encrypted = b"".join(self.cipher3.encrypt_cbc(data_decrypted, iv))

        # Return IV prepended to encrypted data
        return iv + data_encrypted

    def decrypt(self, data):
        # Extract IV and actual encrypted data
        iv = data[:8]
        data = data[8:]

        # Triple decryption
        data_decrypted = b"".join(self.cipher3.decrypt_cbc(data, iv))
        data_encrypted = b"".join(self.cipher2.encrypt_cbc(data_decrypted, iv))
        data_decrypted = b"".join(self.cipher1.decrypt_cbc(data_encrypted, iv))

        return data_decrypted

    def encrypt_text(self, text):
        # Convert text to bytes and pad
        data = text.encode()
        padded_data = pkcs7_pad(data)

        # Encrypt and return
        return self.encrypt(padded_data)

    def decrypt_text(self, data):
        # Decrypt and remove padding
        decrypted_data = self.decrypt(data)
        unpadded_data = pkcs7_unpad(decrypted_data)

        # Convert back to string
        return unpadded_data.decode()

    def encrypt_image(self, image_path, output_path):
        # Convert image to bytes and pad
        image_bytes = image_to_bytes(image_path)
        padded_image_bytes = pkcs7_pad(image_bytes)

        # Encrypt image
        encrypted_data = self.encrypt(padded_image_bytes)

        # Save encrypted image (IV included)
        bytes_to_image(encrypted_data, output_path)
        print(f"Encrypted image saved to {output_path}")
        return encrypted_data

    def decrypt_image(self, encrypted_image_path, output_path):
        # Read encrypted image bytes
        encrypted_data = image_to_bytes(encrypted_image_path)

        # Decrypt and remove padding
        decrypted_data = self.decrypt(encrypted_data)
        unpadded_data = pkcs7_unpad(decrypted_data)

        # Save decrypted image
        bytes_to_image(unpadded_data, output_path)
        print(f"Decrypted image saved to {output_path}")
        return unpadded_data
