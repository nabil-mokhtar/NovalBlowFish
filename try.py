import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from math import floor
from scipy.special import erfc, gammaincc


class FrequencyTest:
    @staticmethod
    def monobit_test(binary_data: str):
        length_of_bit_string = len(binary_data)
        count = sum(1 if bit == '1' else -1 for bit in binary_data)
        sObs = count / (length_of_bit_string ** 0.5)
        p_value = erfc(abs(sObs) / (2 ** 0.5))
        return (p_value, (p_value >= 0.01))

    @staticmethod
    def block_frequency(binary_data: str, block_size=128):
        length_of_bit_string = len(binary_data)
        if length_of_bit_string < block_size:
            block_size = length_of_bit_string

        number_of_blocks = floor(length_of_bit_string / block_size)
        if number_of_blocks == 1:
            return FrequencyTest.monobit_test(binary_data[0:block_size])

        proportion_sum = 0.0
        for i in range(number_of_blocks):
            block_data = binary_data[i * block_size:(i + 1) * block_size]
            one_count = block_data.count('1')
            pi = one_count / block_size
            proportion_sum += (pi - 0.5) ** 2

        result = 4.0 * block_size * proportion_sum
        p_value = gammaincc(number_of_blocks / 2, result / 2)
        return (p_value, (p_value >= 0.01))


class TripleBlowfishEncryptor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Triple Blowfish Encryptor")
        self.geometry("600x400")

        self.key1_label = tk.Label(self, text="Key 1:")
        self.key1_label.pack()
        self.key1_entry = tk.Entry(self)
        self.key1_entry.pack()

        self.key2_label = tk.Label(self, text="Key 2:")
        self.key2_label.pack()
        self.key2_entry = tk.Entry(self)
        self.key2_entry.pack()

        self.key3_label = tk.Label(self, text="Key 3:")
        self.key3_label.pack()
        self.key3_entry = tk.Entry(self)
        self.key3_entry.pack()

        self.encrypt_button = tk.Button(self, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.pack()

        self.frequency_test_button = tk.Button(self, text="Run Frequency Tests", command=self.run_frequency_tests)
        self.frequency_test_button.pack()

        self.output_area = tk.Text(self, height=10, width=50)
        self.output_area.pack()

        # Store binary data for frequency tests
        self.binary_data = None

    def encrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return

        # Simulate encryption and generate binary data directly from image bytes
        image = Image.open(file_path)
        binary_data = image.tobytes()  # Get the raw byte data of the image

        # Convert bytes to a string of bits
        self.binary_data = ''.join(format(byte, '08b') for byte in binary_data)

        # Display the size of the binary data
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"Encrypted Data Size (Bits): {len(self.binary_data)}")

    def run_frequency_tests(self):
        if self.binary_data is None:
            messagebox.showerror("Error", "No binary data to test.")
            return

        # Run frequency tests using the binary data
        print(self.binary_data)
        monobit_result = FrequencyTest.monobit_test(self.binary_data)
        block_result = FrequencyTest.block_frequency(self.binary_data)

        # Display results without reprinting binary data
        self.output_area.delete(1.0, tk.END)  # Clear previous output
        results = (
            f"Monobit Test P-Value: {monobit_result[0]:.6f}, Random: {monobit_result[1]}\n"
            f"Block Frequency Test P-Value: {block_result[0]:.6f}, Random: {block_result[1]}"
        )
        self.output_area.insert(tk.END, results)  # Insert only the test results


if __name__ == "__main__":
    app = TripleBlowfishEncryptor()
    app.mainloop()
