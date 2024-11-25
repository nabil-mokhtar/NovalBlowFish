import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from TripleBlowfish import TripleBlowfish
import subprocess
from tkinter import messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Triple Blowfish Encryptor")
        self.root.geometry("600x500")

        # Create tab control
        self.tab_control = ttk.Notebook(self.root)
        self.image_tab = ttk.Frame(self.tab_control)
        self.text_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.image_tab, text='Image Encryptor')
        self.tab_control.add(self.text_tab, text='Text Encryptor')
        self.tab_control.pack(expand=1, fill='both')

        self.setup_image_tab()
        self.setup_text_tab()

        self.original_image = None
        self.encrypted_image_path = None
        self.noise_image_path = None

    def setup_image_tab(self):
        """Setup GUI components for image encryption/decryption."""
        # Title
        self.title_label = tk.Label(self.image_tab, text="Triple Blowfish Image Encryptor", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Key Inputs
        self.key1_label_image = tk.Label(self.image_tab, text="Enter Key 1:")
        self.key1_label_image.pack(pady=5)
        self.key1_entry_image = tk.Entry(self.image_tab, width=50)
        self.key1_entry_image.pack(pady=5)

        self.key2_label_image = tk.Label(self.image_tab, text="Enter Key 2:")
        self.key2_label_image.pack(pady=5)
        self.key2_entry_image = tk.Entry(self.image_tab, width=50)
        self.key2_entry_image.pack(pady=5)

        self.key3_label_image = tk.Label(self.image_tab, text="Enter Key 3:")
        self.key3_label_image.pack(pady=5)
        self.key3_entry_image = tk.Entry(self.image_tab, width=50)
        self.key3_entry_image.pack(pady=5)

        # Upload Button
        self.upload_button = tk.Button(self.image_tab, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Encrypt Button
        self.encrypt_button = tk.Button(self.image_tab, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.pack(pady=10)

        # Decrypt Button
        self.decrypt_button = tk.Button(self.image_tab, text="Decrypt Image", command=self.decrypt_image)
        self.decrypt_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.image_tab, text="", font=("Helvetica", 10), fg="green")
        self.status_label.pack(pady=10)

        self.image_path = None

    def upload_image(self):
        """Open file dialog to upload image."""
        filetypes = [
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("All Files", "*.*")
        ]

        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)

        if self.image_path:
            self.status_label.config(text=f"Image Uploaded: {self.image_path}")
            self.original_image = Image.open(self.image_path)  # Store the original image
        else:
            self.status_label.config(text="No image uploaded.")

    def encrypt_image(self):
        """Encrypt the uploaded image."""
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first.")
            return

        try:
            # Get keys from user inputs
            key1 = self.key1_entry_image.get().encode('utf-8')
            key2 = self.key2_entry_image.get().encode('utf-8')
            key3 = self.key3_entry_image.get().encode('utf-8')

            if not key1 or not key2 or not key3:
                messagebox.showwarning("Warning", "Please enter all three keys.")
                return

            # Generate paths for encrypted and noise images in the same directory as the original image
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            dir_name = os.path.dirname(self.image_path)

            self.encrypted_image_path = os.path.join(dir_name, f"{base_name}_encrypted.png")
            self.noise_image_path = os.path.join(dir_name, f"{base_name}_noise.png")

            # Initialize TripleBlowfish with the entered keys
            self.triple_blowfish = TripleBlowfish(key1, key2, key3)
            # Encrypt the image
            self.triple_blowfish.encrypt_image(self.image_path, self.encrypted_image_path)

            # Create noise image
            self.noise_image = self.generate_noise_image()

            image = Image.open(self.image_path)
            binary_data = image.tobytes()
            self.binary_data = ''.join(format(byte, '08b') for byte in binary_data)
            print(f"Encrypted Data Size (Bits): {len(self.binary_data)}")
            print(f"Binary Data (First 100 bits): {self.binary_data[:100]}...")

            with open("binary_data_for_image.txt", "w") as f:
                 f.write(self.binary_data[:1000000])


            self.status_label.config(text=f"Encrypted Image Saved: {self.encrypted_image_path}")
            messagebox.showinfo("Success", "Image encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error encrypting image: {e}")

    def generate_noise_image(self):
        """Generate a binary noise image based on the original image."""
        if self.original_image:
            # Create a binary noise image (black or white)
            width, height = self.original_image.size
            noise_data = np.random.choice([0, 255], size=(height, width), p=[0.5, 0.5])  # 50% chance for black or white
            noise_image_data = np.clip(noise_data, 0, 255).astype(np.uint8)  # Ensure values are in the correct range
            noise_image = Image.fromarray(noise_image_data)
            noise_image.save(self.noise_image_path)  # Save noise image to the specified path
            return noise_image  # Return noise image without resizing
        return None

    def decrypt_image(self):
        """Decrypt the last encrypted image."""
        if not self.encrypted_image_path:
            messagebox.showwarning("Warning", "Please encrypt an image first.")
            return

        try:
            decrypted_image_path = os.path.splitext(self.encrypted_image_path)[0] + "_decrypted.png"

            # Get keys from user inputs
            key1 = self.key1_entry_image.get().encode('utf-8')
            key2 = self.key2_entry_image.get().encode('utf-8')
            key3 = self.key3_entry_image.get().encode('utf-8')

            if not key1 or not key2 or not key3:
                messagebox.showwarning("Warning", "Please enter all three keys.")
                return

            # Initialize TripleBlowfish with the entered keys
            self.triple_blowfish = TripleBlowfish(key1, key2, key3)

            self.triple_blowfish.decrypt_image(self.encrypted_image_path, decrypted_image_path)

            # Load decrypted image
            decrypted_image = Image.open(decrypted_image_path)

            # Show images in a pop-up window
            self.show_images(self.original_image, self.noise_image_path, decrypted_image)

            messagebox.showinfo("Success", "Image decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error decrypting image: {e}")

    def show_images(self, original, noise_path, decrypted):
        """Show original, noise, and decrypted images in a new window."""
        pop_up = tk.Toplevel(self.root)
        pop_up.title("Image Comparison")

        # Create a frame for better layout management
        frame = tk.Frame(pop_up)
        frame.pack(padx=10, pady=10)

        # Load noise image for display
        noise_image = Image.open(noise_path)

        # Resize images to fit in a reasonable area
        max_size = (200, 200)  # Set a maximum size for images
        original = original.resize(max_size, Image.ANTIALIAS)
        noise_image = noise_image.resize(max_size, Image.ANTIALIAS)
        decrypted = decrypted.resize(max_size, Image.ANTIALIAS)

        # Create labels for images
        original_label = tk.Label(frame, text="Original Image:")
        original_label.grid(row=0, column=0, padx=10, pady=10)
        original_image_tk = ImageTk.PhotoImage(original)
        original_image_widget = tk.Label(frame, image=original_image_tk)
        original_image_widget.image = original_image_tk
        original_image_widget.grid(row=1, column=0, padx=10, pady=10)

        noise_label = tk.Label(frame, text="Noise Image:")
        noise_label.grid(row=0, column=1, padx=10, pady=10)
        noise_image_tk = ImageTk.PhotoImage(noise_image)
        noise_image_widget = tk.Label(frame, image=noise_image_tk)
        noise_image_widget.image = noise_image_tk
        noise_image_widget.grid(row=1, column=1, padx=10, pady=10)

        decrypted_label = tk.Label(frame, text="Decrypted Image:")
        decrypted_label.grid(row=0, column=2, padx=10, pady=10)
        decrypted_image_tk = ImageTk.PhotoImage(decrypted)
        decrypted_image_widget = tk.Label(frame, image=decrypted_image_tk)
        decrypted_image_widget.image = decrypted_image_tk
        decrypted_image_widget.grid(row=1, column=2, padx=10, pady=10)

        # Center the images in the pop-up
        frame.update_idletasks()  # Update the frame with the size of its children
        pop_up_width = frame.winfo_width()
        pop_up_height = frame.winfo_height()
        screen_width = pop_up.winfo_screenwidth()
        screen_height = pop_up.winfo_screenheight()
        pop_up.geometry(f"{pop_up_width}x{pop_up_height}+{(screen_width // 2) - (pop_up_width // 2)}+{(screen_height // 2) - (pop_up_height // 2)}")

    def setup_text_tab(self):
        """Setup GUI components for text encryption/decryption."""
        # Title
        self.title_label_text = tk.Label(self.text_tab, text="Triple Blowfish Text Encryptor", font=("Helvetica", 16))
        self.title_label_text.pack(pady=10)

        # Key Inputs
        self.key1_label_text = tk.Label(self.text_tab, text="Enter Key 1:")
        self.key1_label_text.pack(pady=5)
        self.key1_entry_text = tk.Entry(self.text_tab, width=50)
        self.key1_entry_text.pack(pady=5)

        self.key2_label_text = tk.Label(self.text_tab, text="Enter Key 2:")
        self.key2_label_text.pack(pady=5)
        self.key2_entry_text = tk.Entry(self.text_tab, width=50)
        self.key2_entry_text.pack(pady=5)

        self.key3_label_text = tk.Label(self.text_tab, text="Enter Key 3:")
        self.key3_label_text.pack(pady=5)
        self.key3_entry_text = tk.Entry(self.text_tab, width=50)
        self.key3_entry_text.pack(pady=5)

        # Plain Text Entry
        self.plain_text_label = tk.Label(self.text_tab, text="Enter Plain Text:")
        self.plain_text_label.pack(pady=5)
        self.plain_text_entry = tk.Text(self.text_tab, height=5, width=50)
        self.plain_text_entry.pack(pady=5)

        # Encrypt Button
        self.encrypt_text_button = tk.Button(self.text_tab, text="Encrypt Text", command=self.encrypt_text)
        self.encrypt_text_button.pack(pady=5)

        # Encrypted Text Display
        self.encrypted_text_label = tk.Label(self.text_tab, text="Encrypted Text:")
        self.encrypted_text_label.pack(pady=5)
        self.encrypted_text_display = tk.Text(self.text_tab, height=5, width=50)
        self.encrypted_text_display.pack(pady=5)

        # Decrypt Button
        self.decrypt_text_button = tk.Button(self.text_tab, text="Decrypt Text", command=self.decrypt_text)
        self.decrypt_text_button.pack(pady=5)

        # Decrypted Text Display
        self.decrypted_text_label = tk.Label(self.text_tab, text="Decrypted Text:")
        self.decrypted_text_label.pack(pady=5)
        self.decrypted_text_display = tk.Text(self.text_tab, height=5, width=50)
        self.decrypted_text_display.pack(pady=5)

    def encrypt_text(self):
        """Encrypt the text from the input box and display it."""
        plain_text = self.plain_text_entry.get("1.0", tk.END).strip()
        if not plain_text:
            messagebox.showwarning("Warning", "Please enter some text to encrypt.")
            return

        try:
            # Get keys from user inputs
            key1 = self.key1_entry_text.get().encode('utf-8')
            key2 = self.key2_entry_text.get().encode('utf-8')
            key3 = self.key3_entry_text.get().encode('utf-8')

            if not key1 or not key2 or not key3:
                messagebox.showwarning("Warning", "Please enter all three keys.")
                return

            # Initialize TripleBlowfish with the entered keys
            self.triple_blowfish = TripleBlowfish(key1, key2, key3)

            encrypted_data = self.triple_blowfish.encrypt_text(plain_text)
            binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)
            print (binary_data)

            with open("binary_data_for_text.txt", "w") as f:
                 f.write(binary_data)

            self.encrypted_text_display.delete("1.0", tk.END)  # Clear previous output
            self.encrypted_text_display.insert(tk.END, encrypted_data.hex())  # Show encrypted data in hex
        except Exception as e:
            messagebox.showerror("Error", f"Error encrypting text: {e}")

    def decrypt_text(self):
        """Decrypt the text from the encrypted box and display the original text."""
        encrypted_text_hex = self.encrypted_text_display.get("1.0", tk.END).strip()
        if not encrypted_text_hex:
            messagebox.showwarning("Warning", "Please encrypt some text first.")
            return
        try:
            encrypted_data = bytes.fromhex(encrypted_text_hex)  # Convert hex back to bytes

            # Get keys from user inputs
            key1 = self.key1_entry_text.get().encode('utf-8')
            key2 = self.key2_entry_text.get().encode('utf-8')
            key3 = self.key3_entry_text.get().encode('utf-8')

            if not key1 or not key2 or not key3:
                messagebox.showwarning("Warning", "Please enter all three keys.")
                return

            # Initialize TripleBlowfish with the entered keys
            self.triple_blowfish = TripleBlowfish(key1, key2, key3)

            decrypted_text = self.triple_blowfish.decrypt_text(encrypted_data)
            self.decrypted_text_display.delete("1.0", tk.END)  # Clear previous output
            self.decrypted_text_display.insert(tk.END, decrypted_text)  # Show original text
        except Exception as e:
            messagebox.showerror("Error", f"Error during decryption: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()