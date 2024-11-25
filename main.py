import random
import string
import os

from TripleBlowfish import TripleBlowfish
from helper_functions import image_to_bytes

if __name__ == "__main__":
    key1 = b"KEY-1"
    key2 = b"KEY-2"
    key3 = b"KEY-3"

    # Initialize TripleBlowfish with the provided keys
    triple_blowfish = TripleBlowfish(key1, key2, key3)

    choice = input("Enter 0 to encrypt text, 1 to encrypt an image: ")

    if choice == '0':
        rand_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100000))
    
        print(f"Original Text (first 10 chars): {rand_string[:10]}")
        encrypted = triple_blowfish.encrypt_text(rand_string)
        print(f"Encrypted Text (first 10 bytes): {encrypted[:10].hex()}")
        decrypted = triple_blowfish.decrypt_text(encrypted)
        print(f"Decrypted Text (first 10 chars): {decrypted[:10]}")
    
    elif choice == '1':
        image_path = input("Enter the path of the image file to encrypt: ")
        
        # Determine the output paths
        dir_name = os.path.dirname(image_path)
        file_name = os.path.basename(image_path)
        name, ext = os.path.splitext(file_name)
        
        encrypted_image_path = os.path.join(dir_name, f"{name}_encrypted{ext}")
        decrypted_image_path = os.path.join(dir_name, f"{name}_decrypted{ext}")

        # Encrypt the image
        triple_blowfish.encrypt_image(image_path, encrypted_image_path)
        print(f"Encrypted image saved to {encrypted_image_path}")

        # Decrypt the image
        triple_blowfish.decrypt_image(encrypted_image_path, decrypted_image_path)
        print(f"Decrypted image saved to {decrypted_image_path}")

    else:
        print("Invalid choice. Please enter 0 for text or 1 for image.")
