import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

# Function to open file dialog, compress image by resizing, and save
def compress_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an image file to compress",
        filetypes=[("Image Files", "*.jpg *.jpeg *.bmp *.tiff *.png *.webp"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            # Open the selected image file
            image = Image.open(file_path)
            
            # Get the original dimensions and calculate new dimensions (80% of original size)
            width, height = image.size
            new_dimensions = (int(width * 0.8), int(height * 0.8))
            
            # Resize the image using LANCZOS filter for high-quality downsampling
            compressed_image = image.resize(new_dimensions, Image.LANCZOS)
            
            # Set the default save path with "_compressed" suffix
            original_dir = os.path.dirname(file_path)
            original_name = os.path.splitext(os.path.basename(file_path))[0]
            
            compressed_image_path = filedialog.asksaveasfilename(
                initialdir=original_dir,
                initialfile=f"{original_name}_compressed.png",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png")]
            )
            
            # Save the compressed image with optimized settings
            if compressed_image_path:
                compressed_image.save(compressed_image_path, format="PNG", optimize=True)
                result_text.insert(tk.END, f"Image compressed and saved as {compressed_image_path}\n")
            else:
                result_text.insert(tk.END, "Image compression cancelled.\n")
                
        except Exception as e:
            result_text.insert(tk.END, f"An error occurred: {e}\n")
    else:
        result_text.insert(tk.END, "No file selected.\n")

# Tkinter GUI setup
root = tk.Tk()
root.title("Image Compression Tool")

# GUI label
file_label = tk.Label(root, text="Select an image file to compress:")
file_label.pack()

# Button to select file and start compression
compress_button = tk.Button(root, text="Choose Image and Compress", command=compress_image)
compress_button.pack()

# Text widget to display status messages
result_text = tk.Text(root, wrap=tk.WORD)
result_text.pack()

# Run the GUI loop
root.mainloop()
