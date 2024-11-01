import whisper
import tkinter as tk
from tkinter import filedialog
import warnings
import torch

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load the Whisper model for CPU
try:
    model = whisper.load_model("small", device="cpu")  # Use "small" model and CPU only
    print("Model loaded successfully.")
except Exception as e:
    print(f"Failed to load the model: {e}")
    exit()

# Function to open file dialog and transcribe file
def transcribe_file():
    try:
        # Open file dialog to select an audio file
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(
            title="Select an audio file for transcription",
            filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.ogg"), ("All Files", "*.*"))
        )

        if file_path:
            print(f"Transcribing {file_path}...")
            # Transcribe the selected file
            result = model.transcribe(file_path)
            print("Transcription complete.")

            # Save transcription to a text file
            output_path = f"{file_path}_transcription.txt"
            with open(output_path, "w") as f:
                f.write(result["text"])
            print(f"Transcription saved as {output_path}\n")
        else:
            print("No file selected.")

    except Exception as e:
        print(f"An error occurred during transcription: {e}")

# Run the transcription function
transcribe_file()

