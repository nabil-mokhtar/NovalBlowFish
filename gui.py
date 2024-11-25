import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from GetBlowfish import GetBlowfish
from TripleBlowfish import TripleBlowfish

# Global variable to keep track of selected image
selected_image = None


# First screen to choose algorithm
def show_first_screen():
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    # Title
    label = tk.Label(root, text="Choose Encryption Algorithm", font=("Helvetica", 16))
    label.pack(pady=20)

    # Blowfish button
    blowfish_btn = tk.Button(root, text="Blowfish Algorithm", width=20,
                             command=lambda: show_algorithm_screen("blowfish"))
    blowfish_btn.pack(pady=10)

    # Triple Blowfish button
    triple_blowfish_btn = tk.Button(root, text="Triple Blowfish Algorithm", width=20,
                                    command=lambda: show_algorithm_screen("triple_blowfish"))
    triple_blowfish_btn.pack(pady=10)


# Show the algorithm screen based on selection
def show_algorithm_screen(algorithm):
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()

    # Back button to go back to the first screen
    back_btn = tk.Button(root, text="Back", command=show_first_screen)
    back_btn.grid(row=0, column=0, padx=10, pady=10)

    # Set the title based on algorithm
    title = "Blowfish Algorithm" if algorithm == "blowfish" else "Triple Blowfish Algorithm"
    label = tk.Label(root, text=title, font=("Helvetica", 16))
    label.grid(row=0, column=1, columnspan=2, pady=20)

    # Data type selection
    data_type = tk.StringVar(value="text")
    tk.Label(root, text="Select Data Type:").grid(row=1, column=0, padx=10, sticky="w")
    text_radio = tk.Radiobutton(root, text="Text", variable=data_type, value="text",
                                command=lambda: toggle_data_input("text"))
    text_radio.grid(row=1, column=1, padx=10, sticky="w")
    image_radio = tk.Radiobutton(root, text="Image", variable=data_type, value="image",
                                 command=lambda: toggle_data_input("image"))
    image_radio.grid(row=1, column=2, padx=10, sticky="w")

    # Input for keys
    tk.Label(root, text="Enter Key(s):").grid(row=2, column=0, padx=10, sticky="w")
    key1_entry = tk.Entry(root, width=30)
    key1_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    # Initialize key2 and key3 entries only for Triple Blowfish
    key2_entry = None
    key3_entry = None
    if algorithm == "triple_blowfish":
        key2_entry = tk.Entry(root, width=30)
        key2_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        key3_entry = tk.Entry(root, width=30)
        key3_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

    # Text or Image Input
    text_entry = tk.Text(root, width=40, height=3)
    text_entry.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    # Non-modifiable text field for encrypted text
    encrypted_text_display = tk.Text(root, width=40, height=2, state="disabled")
    encrypted_text_display.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    # Non-modifiable text field for decrypted text
    decrypted_text_display = tk.Text(root, width=40, height=2, state="disabled")
    decrypted_text_display.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    image_button = tk.Button(root, text="Select Image", command=lambda: select_image())
    image_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
    image_button.grid_remove()  # Hide initially

    # Image display area
    image_display_label = tk.Label(root, bg="lightgray", width=40, height=20)
    image_display_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    image_display_label.grid_remove()

    # Action buttons for encryption and decryption
    encrypt_btn = tk.Button(root, text="Encrypt",
                            command=lambda: handle_encrypt(algorithm, data_type.get(), key1_entry, key2_entry,
                                                           key3_entry, text_entry, encrypted_text_display))
    encrypt_btn.grid(row=8, column=0, pady=20)

    decrypt_btn = tk.Button(root, text="Decrypt",
                            command=lambda: handle_decrypt(algorithm, data_type.get(), key1_entry, key2_entry,
                                                           key3_entry, encrypted_text_display, decrypted_text_display))
    decrypt_btn.grid(row=8, column=1, pady=20)

    # Function to toggle between text and image input
    def toggle_data_input(data_type):
        if data_type == "text":
            text_entry.grid()
            image_button.grid_remove()
            image_display_label.grid_remove()
        else:
            text_entry.grid_remove()
            image_button.grid()
            image_display_label.grid()

    # Function to select an image
    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            # Load and display image in original size
            img = Image.open(file_path)
            img_tk = ImageTk.PhotoImage(img)
            image_display_label.config(image=img_tk)
            image_display_label.image = img_tk  # Keep reference to avoid garbage collection
            global selected_image
            selected_image = img


# Function to handle encryption
def handle_encrypt(algorithm, data_type, key1_entry, key2_entry, key3_entry, text_entry, encrypted_text_display):
    key1 = key1_entry.get()

    if algorithm == "triple_blowfish":
        key2 = key2_entry.get()
        key3 = key3_entry.get()

        # Check if keys are provided, else show an error message
        if not key1 or not key2 or not key3:
            messagebox.showerror("Error", "All three keys are required for Triple Blowfish!")
            return

        # Convert keys to bytes
        generic_enc_dec = TripleBlowfish(key1.encode(), key2.encode(), key3.encode())

    else:
        # Blowfish encryption (single key)
        if not key1:
            messagebox.showerror("Error", "Key is required for Blowfish encryption!")
            return
        # You would need a Blowfish class or implementation for this part
        generic_enc_dec = GetBlowfish(key1.encode())

    if data_type == "text":
        data = text_entry.get("1.0", tk.END).strip()
        encrypted_data = generic_enc_dec.encrypt_text(data)  # Encrypt text
        global temp_enc
        temp_enc = encrypted_data
        # Display encrypted data in the read-only text field
        encrypted_text_display.config(state="normal")
        encrypted_text_display.delete(1.0, "end")
        encrypted_text_display.insert("end", encrypted_data.hex())
        encrypted_text_display.config(state="disabled")

    elif data_type == "image" and selected_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            encrypted_image = generic_enc_dec.encrypt_image(selected_image, file_path)
            messagebox.showinfo("Encrypt", f"Image encrypted successfully and saved to {file_path}")


def handle_decrypt(algorithm, data_type, key1_entry, key2_entry, key3_entry, text_entry, decrypted_text_display):
    key1 = key1_entry.get()

    if algorithm == "triple_blowfish":
        key2 = key2_entry.get()
        key3 = key3_entry.get()

        # Check if keys are provided, else show an error message
        if not key1 or not key2 or not key3:
            messagebox.showerror("Error", "All three keys are required for Triple Blowfish!")
            return

        # Convert keys to bytes
        generic_enc_dec = TripleBlowfish(key1.encode(), key2.encode(), key3.encode())

    else:
        # Blowfish encryption (single key)
        if not key1:
            messagebox.showerror("Error", "Key is required for Blowfish encryption!")
            return
        # You would need a Blowfish class or implementation for this part
        generic_enc_dec = GetBlowfish(key1.encode())

    if data_type == "text":
        data = temp_enc  # Remove extra spaces or newlines
        print(type(data))

        # Check if the data is a valid hex string before decryption
        decrypted_data = generic_enc_dec.decrypt_text(data)  # Decrypt text

        # Display decrypted data in the read-only text field
        decrypted_text_display.config(state="normal")
        decrypted_text_display.delete(1.0, "end")
        print(decrypted_data)
        decrypted_text_display.insert("end", decrypted_data)
        decrypted_text_display.config(state="disabled")


    elif data_type == "image" and selected_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            decrypted_image = generic_enc_dec.decrypt_image(selected_image, file_path)
            messagebox.showinfo("Decrypt", f"Image decrypted successfully and saved to {file_path}")


# Root window
root = tk.Tk()
root.title("Blowfish Encryption Tool")
root.geometry("500x600")

# Show the first screen on start
show_first_screen()

# Start the main event loop
root.mainloop()
