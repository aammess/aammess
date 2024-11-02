import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

# Function to open file dialog, convert image to PNG, and save
def convert_image_to_png():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an image file to convert",
        filetypes=[("Image Files", "*.jpg *.jpeg *.bmp *.tiff *.webp"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            # Open the selected image file
            image = Image.open(file_path)
            
            # Get the original file name and directory
            original_dir = os.path.dirname(file_path)
            original_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Set the default save path with a new PNG extension
            converted_image_path = filedialog.asksaveasfilename(
                initialdir=original_dir,
                initialfile=f"{original_name}_converted.png",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png")]
            )
            
            # Save the image in PNG format
            if converted_image_path:
                image.save(converted_image_path, format="PNG")
                result_text.insert(tk.END, f"Image saved as {converted_image_path}\n")
            else:
                result_text.insert(tk.END, "Image conversion cancelled.\n")
                
        except Exception as e:
            result_text.insert(tk.END, f"An error occurred: {e}\n")
    else:
        result_text.insert(tk.END, "No file selected.\n")

# Tkinter GUI setup
root = tk.Tk()
root.title("Image to PNG Converter")

# GUI label
file_label = tk.Label(root, text="Select an image file to convert to PNG format:")
file_label.pack()

# Button to select file and start conversion
convert_button = tk.Button(root, text="Choose Image and Convert", command=convert_image_to_png)
convert_button.pack()

# Text widget to display status messages
result_text = tk.Text(root, wrap=tk.WORD)
result_text.pack()

# Run the GUI loop
root.mainloop()
