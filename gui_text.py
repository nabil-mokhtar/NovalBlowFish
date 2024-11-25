import tkinter as tk
from tkinter import messagebox
from TripleBlowfish import TripleBlowfish

class TextEncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Triple Blowfish Text Encryptor")
        self.root.geometry("500x400")

        # Initialize TripleBlowfish with random keys for simplicity
        key1 = b'secret_k1'
        key2 = b'secret_k2'
        key3 = b'secret_k3'
        self.triple_blowfish = TripleBlowfish(key1, key2, key3)

        # Setup GUI components
        self.setup_gui()

    def setup_gui(self):
        # Plain Text Entry
        self.plain_text_label = tk.Label(self.root, text="Enter Plain Text:")
        self.plain_text_label.pack(pady=5)
        self.plain_text_entry = tk.Text(self.root, height=5, width=50)
        self.plain_text_entry.pack(pady=5)

        # Encrypt Button
        self.encrypt_button = tk.Button(self.root, text="Encrypt Text", command=self.encrypt_text)
        self.encrypt_button.pack(pady=5)

        # Encrypted Text Display
        self.encrypted_text_label = tk.Label(self.root, text="Encrypted Text:")
        self.encrypted_text_label.pack(pady=5)
        self.encrypted_text_display = tk.Text(self.root, height=5, width=50)
        self.encrypted_text_display.pack(pady=5)

        # Decrypt Button
        self.decrypt_button = tk.Button(self.root, text="Decrypt Text", command=self.decrypt_text)
        self.decrypt_button.pack(pady=5)

        # Decrypted Text Display
        self.decrypted_text_label = tk.Label(self.root, text="Decrypted Text:")
        self.decrypted_text_label.pack(pady=5)
        self.decrypted_text_display = tk.Text(self.root, height=5, width=50)
        self.decrypted_text_display.pack(pady=5)

    def encrypt_text(self):
        """Encrypt the text from the input box and display it."""
        plain_text = self.plain_text_entry.get("1.0", tk.END).strip()
        if not plain_text:
            messagebox.showwarning("Warning", "Please enter some text to encrypt.")
            return
        encrypted_data = self.triple_blowfish.encrypt_text(plain_text)
        self.encrypted_text_display.delete("1.0", tk.END)  # Clear previous output
        self.encrypted_text_display.insert(tk.END, encrypted_data.hex())  # Show encrypted data in hex

    def decrypt_text(self):
        """Decrypt the text from the encrypted box and display the original text."""
        encrypted_text_hex = self.encrypted_text_display.get("1.0", tk.END).strip()
        if not encrypted_text_hex:
            messagebox.showwarning("Warning", "Please encrypt some text first.")
            return
        try:
            encrypted_data = bytes.fromhex(encrypted_text_hex)  # Convert hex back to bytes
            decrypted_text = self.triple_blowfish.decrypt_text(encrypted_data)
            self.decrypted_text_display.delete("1.0", tk.END)  # Clear previous output
            self.decrypted_text_display.insert(tk.END, decrypted_text)  # Show original text
        except Exception as e:
            messagebox.showerror("Error", f"Error during decryption: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEncryptionGUI(root)
    root.mainloop()
