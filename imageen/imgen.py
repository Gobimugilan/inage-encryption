import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os

# ---------- Image Encryption Functions ----------
def apply_math_operation(img):
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (255 - r, 255 - g, 255 - b)
    return img

def swap_pixels(img, seed):
    pixels = list(img.getdata())
    indices = list(range(len(pixels)))
    random.seed(seed)
    random.shuffle(indices)
    shuffled_pixels = [pixels[i] for i in indices]
    img.putdata(shuffled_pixels)
    return img, indices

def unswap_pixels(img, indices):
    shuffled_pixels = list(img.getdata())
    original_pixels = [None] * len(indices)
    for i, index in enumerate(indices):
        original_pixels[index] = shuffled_pixels[i]
    img.putdata(original_pixels)
    return img

# ---------- GUI Application ----------
class ImageEncryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("500x400")

        self.image_path = None
        self.indices = None  # Used for swap decryption

        # Widgets
        tk.Label(root, text="Choose Encryption Method:").pack(pady=10)
        self.method_var = tk.StringVar(value="math")
        tk.Radiobutton(root, text="Math Operation", variable=self.method_var, value="math").pack()
        tk.Radiobutton(root, text="Pixel Swap", variable=self.method_var, value="swap").pack()

        self.seed_label = tk.Label(root, text="Enter Seed (for swap):")
        self.seed_entry = tk.Entry(root)
        self.seed_label.pack()
        self.seed_entry.pack()

        tk.Button(root, text="Choose Image", command=self.load_image).pack(pady=10)
        tk.Button(root, text="Encrypt Image", command=self.encrypt_image).pack()
        tk.Button(root, text="Decrypt Image", command=self.decrypt_image).pack(pady=5)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            self.status_label.config(text=f"Loaded: {os.path.basename(path)}")

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please choose an image first.")
            return

        method = self.method_var.get()
        img = Image.open(self.image_path).convert("RGB")

        if method == "math":
            img = apply_math_operation(img)
            img.save("encrypted_math.png")
            self.status_label.config(text="Saved as: encrypted_math.png")

        elif method == "swap":
            seed = self.get_seed()
            img, self.indices = swap_pixels(img, seed)
            img.save("encrypted_swap.png")
            self.status_label.config(text="Saved as: encrypted_swap.png (keep seed for decryption)")

    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please choose an image first.")
            return

        method = self.method_var.get()
        img = Image.open(self.image_path).convert("RGB")

        if method == "math":
            img = apply_math_operation(img)
            img.save("decrypted_math.png")
            self.status_label.config(text="Saved as: decrypted_math.png")

        elif method == "swap":
            seed = self.get_seed()
            pixels = list(img.getdata())
            indices = list(range(len(pixels)))
            random.seed(seed)
            random.shuffle(indices)
            img = unswap_pixels(img, indices)
            img.save("decrypted_swap.png")
            self.status_label.config(text="Saved as: decrypted_swap.png")

    def get_seed(self):
        try:
            return int(self.seed_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Seed", "Please enter a valid integer seed.")
            return 0

# ---------- Run the Application ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorGUI(root)
    root.mainloop()
