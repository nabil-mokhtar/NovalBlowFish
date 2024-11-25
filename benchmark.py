import tkinter as tk
from tkinter import ttk
from time import perf_counter
import random
import string
from os import urandom
import blowfish
from TripleBlowfish import TripleBlowfish


class Timer(object):
    def __init__(self, clock):
        self.clock = clock
        self.elapsed = 0

    def __enter__(self):
        self._enter_time = self.clock()

    def __exit__(self, exc_type, exc_value, traceback):
        t = self.clock()
        self.elapsed += t - self._enter_time


class BenchmarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmark Triple Blowfish")
        self.root.geometry("600x500")

        # Setup GUI components
        self.title_label = tk.Label(self.root, text="Benchmarking Triple Blowfish", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.benchmark_button = tk.Button(self.root, text="Run Benchmarks", command=self.run_benchmarks)
        self.benchmark_button.pack(pady=20)

        self.benchmark_results = tk.Text(self.root, height=20, width=70)
        self.benchmark_results.pack(pady=10, fill=tk.BOTH, expand=True)

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def run_benchmarks(self):
        """Run the benchmarks and display results."""
        self.benchmark_results.delete("1.0", tk.END)  # Clear previous results

        # Parameters for benchmarking
        times = 6
        num_bytes = 10000

        # Blowfish cipher setup
        test_cipher = blowfish.Cipher(b"this ist a key")
        rand_bytes = urandom(num_bytes)
        iv = urandom(8)

        self.benchmark_results.insert(tk.END, "\nBenchmarking 'encrypt_cbc'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                b"".join(test_cipher.encrypt_cbc(rand_bytes, iv))
            self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec\n".format(num_bytes, timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec (average)\n\n".format(num_bytes, total / (times - 1)))

        self.benchmark_results.insert(tk.END, "Benchmarking 'decrypt_cbc'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                b"".join(test_cipher.decrypt_cbc(rand_bytes, iv))
            self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec\n".format(num_bytes, timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec (average)\n\n".format(num_bytes, total / (times - 1)))

        key1 = b"KEY-1"
        key2 = b"KEY-2"
        key3 = b"KEY-3"
        rand_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_bytes))
        triple_blowfish = TripleBlowfish(key1, key2, key3)

        self.benchmark_results.insert(tk.END, "Benchmarking 'encrypt_text_triple_blowfish'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                encrypted = triple_blowfish.encrypt_text(rand_string)
            self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec\n".format(num_bytes, timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec (average)\n\n".format(num_bytes, total / (times - 1)))

        self.benchmark_results.insert(tk.END, "Benchmarking 'decrypt_text_triple_blowfish'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                triple_blowfish.decrypt_text(encrypted)
            self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec\n".format(num_bytes, timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "{} random bytes in {:.5f} sec (average)\n\n".format(num_bytes, total / (times - 1)))

        self.benchmark_results.insert(tk.END, "Benchmarking 'encrypt_image_triple_blowfish'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                triple_blowfish.encrypt_image("blowfish.jpg", "encrypted_fish.jpg")
            self.benchmark_results.insert(tk.END, "Image 1024 * 793 in {:.5f} sec\n".format(timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "Image 1024 * 793 in {:.5f} sec (average)\n\n".format(total / (times - 1)))

        self.benchmark_results.insert(tk.END, "Benchmarking 'decrypt_image_triple_blowfish'...\n")
        total = 0
        for n in range(1, times):
            timer = Timer(perf_counter)
            with timer:
                triple_blowfish.decrypt_image("encrypted_fish.jpg", "decrypted_fish.jpg")
            self.benchmark_results.insert(tk.END, "Image 1024 * 793 in {:.5f} sec\n".format(timer.elapsed))
            total += timer.elapsed
        self.benchmark_results.insert(tk.END, "Image 1024 * 793 in {:.5f} sec (average)\n".format(total / (times - 1)))


if __name__ == "__main__":
    root = tk.Tk()
    app = BenchmarkApp(root)
    root.mainloop()
