import os
import tkinter as tk
from tkinter import filedialog, messagebox
from TripleBlowfish import TripleBlowfish


class ImageEncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Triple Blowfish Image Encryptor")
        self.root.geometry("500x300")

        self.image_path = None

        # Initialize TripleBlowfish with random keys for simplicity
        key1 = b'secret_k1'
        key2 = b'secret_k2'
        key3 = b'secret_k3'
        self.triple_blowfish = TripleBlowfish(key1, key2, key3)

        # Setup GUI components
        self.setup_gui()

    def setup_gui(self):
        """Setup the buttons and labels for the GUI."""
        # Title
        self.title_label = tk.Label(self.root, text="Triple Blowfish Image Encryptor", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Upload Button
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Encrypt Button
        self.encrypt_button = tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.pack(pady=10)

        # Decrypt Button
        self.decrypt_button = tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image)
        self.decrypt_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 10), fg="green")
        self.status_label.pack(pady=10)

    def upload_image(self):
        """Open file dialog to upload image."""
        self.image_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if self.image_path:
            self.status_label.config(text=f"Image Uploaded: {self.image_path}")
        else:
            self.status_label.config(text="No image uploaded.")

    def encrypt_image(self):
        """Encrypt the uploaded image."""
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first.")
            return

        try:
            encrypted_image_path = os.path.splitext(self.image_path)[0] + "_encrypted.png"
            self.triple_blowfish.encrypt_image(self.image_path, encrypted_image_path)
            self.status_label.config(text=f"Encrypted Image Saved: {encrypted_image_path}")
            messagebox.showinfo("Success", "Image encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error encrypting image: {e}")

    def decrypt_image(self):
        """Decrypt the encrypted image."""
        if not self.image_path or not self.image_path.endswith('_encrypted.png'):
            messagebox.showwarning("Warning", "Please upload an encrypted image first.")
            return

        try:
            decrypted_image_path = os.path.splitext(self.image_path)[0] + "_decrypted.png"
            self.triple_blowfish.decrypt_image(self.image_path, decrypted_image_path)
            self.status_label.config(text=f"Decrypted Image Saved: {decrypted_image_path}")
            messagebox.showinfo("Success", "Image decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error decrypting image: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionGUI(root)
    root.mainloop()
