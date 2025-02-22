import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import random
import string
from FrequencyTest import FrequencyTest
from GetBlowfish import GetBlowfish
from RunTest import RunTest
from Matrix import Matrix
from Spectral import SpectralTest
from TemplateMatching import TemplateMatching
from TripleBlowfish import TripleBlowfish
from Universal import Universal
from Complexity import ComplexityTest
from Serial import Serial
from ApproximateEntropy import ApproximateEntropy
from CumulativeSum import CumulativeSums
from RandomExcursions import RandomExcursions

num_bytes = 10000


class StatisticalTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistical Tests for Noval Blowfish")
        self.root.geometry("1200x600")

        # Create a top frame for control buttons
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        # Add buttons for comparison
        self.compare_button = tk.Button(top_frame, text="Compare Blowfish and Noval Blowfish Image",
                                        command=lambda: self.select_algorithm(True))
        self.compare_button.pack(side=tk.LEFT, padx=10)

        # Create notebook with tabs for Triple and Single Blowfish comparisons
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs for each test's output
        self.tab_triple_blowfish = ttk.Frame(self.notebook)
        self.tab_single_blowfish = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_triple_blowfish, text="Noval Blowfish")
        self.notebook.add(self.tab_single_blowfish, text="Single Blowfish Results")

        # Create Treeview for organized results display in each tab
        self.result_tree_triple = ttk.Treeview(self.tab_triple_blowfish, columns=("Result"), show="tree headings")
        self.result_tree_triple.heading("#0", text="Test Name")
        self.result_tree_triple.heading("Result", text="Result Summary")
        self.result_tree_triple.pack(expand=True, fill='both', padx=10, pady=10)

        self.result_tree_single = ttk.Treeview(self.tab_single_blowfish, columns=("Result"), show="tree headings")
        self.result_tree_single.heading("#0", text="Test Name")
        self.result_tree_single.heading("Result", text="Result Summary")
        self.result_tree_single.pack(expand=True, fill='both', padx=10, pady=10)

        # Bind the event to display details on double-click
        self.result_tree_triple.bind("<Double-1>", self.show_test_details)
        self.result_tree_single.bind("<Double-1>", self.show_test_details)

    def generate_random_test_t(self, rand_string):
        key1, key2, key3 = b"KEY-1", b"KEY-2", b"KEY-3"
        triple_blowfish = TripleBlowfish(key1, key2, key3)
        encrypted = triple_blowfish.encrypt_text(rand_string)
        binary_data = ''.join(format(byte, '08b') for byte in encrypted)
        return binary_data

    def generate_random_test(self, rand_string):
        key1 = b"KEY-1"
        blowfish = GetBlowfish(key1)
        encrypted = blowfish.encrypt_text(rand_string)
        binary_data = ''.join(format(byte, '08b') for byte in encrypted)
        return binary_data

    def test_image_t(self):
        key1, key2, key3 = b"KEY-1", b"KEY-2", b"KEY-3"
        triple_blowfish = TripleBlowfish(key1, key2, key3)
        encrypted = triple_blowfish.encrypt_image("blowfish.jpg", "encrypted_fish.jpg")
        binary_data = ''.join(format(byte, '08b') for byte in encrypted)
        return binary_data

    def test_image(self,key1):
        blowfish = GetBlowfish(key1)
        encrypted = blowfish.encrypt_image("blowfish.jpg", "encrypted_fish.jpg")
        binary_data = ''.join(format(byte, '08b') for byte in encrypted)
        return binary_data

    def readfromfile(self, file_path):

        with open(file_path, "r") as file:
            binary_data = file.read().strip()

        return binary_data

    def select_algorithm(self, image_flag):
            # try:
            # Run tests for both algorithms and display in respective tabs
            # self.run_tests(self.test_image_t(), self.result_tree_triple)
            self.run_tests(self.readfromfile("binary_data_for_image.txt"), self.result_tree_triple)
            self.run_tests(self.readfromfile("binary_data_for_image_single.txt"), self.result_tree_single)

            # except Exception as e:
            #     messagebox.showerror("Error", f"An error occurred: {str(e)}")



    def run_tests(self, binary_data, tree):
        # Clear previous results from Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Run tests and insert results into the Treeview
        results = {"Frequency Test": FrequencyTest.monobit_test(binary_data),
                   "Block Frequency Test": FrequencyTest.block_frequency(binary_data),
                   "Run Test": RunTest.run_test(binary_data),
                   "Longest Run of Ones Test": RunTest.longest_one_block_test(binary_data),
                   "Binary Matrix Rank Test": Matrix.binary_matrix_rank_text(binary_data),
                   "Spectral Test": SpectralTest.spectral_test(binary_data),
                   "Non-overlapping Template Matching Test": TemplateMatching.non_overlapping_test(binary_data,
                                                                                                   "000000001"),
                   "Overlapping Template Matching Test": TemplateMatching.overlapping_patterns(binary_data),
                   "Universal Test": Universal.statistical_test(binary_data),
                   "Linear Complexity Test": ComplexityTest.linear_complexity_test(binary_data),
                   "Serial Test": Serial.serial_test(binary_data),
                   "Approximate Entropy Test": ApproximateEntropy.approximate_entropy_test(binary_data),
                   "Cumulative Sums Test (Forward)": CumulativeSums.cumulative_sums_test(binary_data, 0),
                   "Cumulative Sums Test (Backward)": CumulativeSums.cumulative_sums_test(binary_data, 1),
                   "Random Excursion Test": RandomExcursions.random_excursions_test(binary_data),
                   "Random Excursion Variant Test": RandomExcursions.variant_test(binary_data[:1000000])}

        # Random Excursions Tests

        for test_name, result_summary in results.items():
            tree.insert("", "end", text=test_name, values=(result_summary,))

    def show_test_details(self, event):
        # Get selected item and show details
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            test_name = tree.item(selected_item, "text")
            result_summary = tree.item(selected_item, "values")[0]

            # Display detailed result in a new window
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Details for {test_name}")
            detail_text = tk.Text(detail_window, wrap=tk.WORD, width=80, height=20)
            detail_text.pack(expand=True, fill='both')
            detail_text.insert("1.0", f"{test_name}:\n{result_summary}")

            detail_window.transient(self.root)  # Make the details window appear over the main window
            detail_window.grab_set()  # Modal mode


if __name__ == "__main__":
    root = tk.Tk()
    app = StatisticalTestApp(root)
    root.mainloop()
