import whisper  # Whisper library for speech recognition
import tkinter as tk  # Tkinter for GUI
from tkinter import filedialog  # File dialog for file selection
import warnings  # Suppress warnings
import torch  # PyTorch for device management
import numpy as np  # For handling audio data as arrays
import concurrent.futures  # For asynchronous transcription

# Set float precision for torch without triggering warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)  # Ignore FP32 warning
    torch.set_float32_matmul_precision('high')

# Detect available device (GPU if available, else CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper model with specific warning suppression for torch.load
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)  # Ignore torch.load weights_only warning
        model = whisper.load_model("base", device=device)  # Load "base" model on the selected device
    print("Model loaded successfully.")
except Exception as e:
    print(f"Failed to load the model: {e}")
    exit()  # Exit if the model fails to load

# Function to perform asynchronous transcription
def transcribe_async(file_path):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(model.transcribe, file_path)
        return future.result()

# Real-time transcription function (with bytes conversion fix)
def transcribe_real_time(data):
    try:
        # Convert raw audio bytes to NumPy array
        np_data = np.frombuffer(data, dtype=np.float32)
        
        # Convert to PyTorch tensor and add batch dimension
        audio = torch.from_numpy(np_data).unsqueeze(0).to(device)
        
        # Perform transcription
        result = model.transcribe(audio)
        print("Transcription:", result["text"])
        
    except Exception as e:
        print(f"An error occurred during real-time transcription: {e}")

# Function to open file dialog, transcribe file, and save the result
def transcribe_file():
    # Open file dialog to select an audio file
    file_path = filedialog.askopenfilename(
        title="Select an audio file for transcription",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.ogg"), ("All Files", "*.*")]
    )
    
    if file_path:
        result_text.insert(tk.END, f"Transcribing {file_path}...\n")
        
        try:
            # Run transcription asynchronously
            transcription = transcribe_async(file_path)
            result_text.insert(tk.END, transcription["text"] + "\nTranscription complete!\n")

            # Save the transcription to a text file
            output_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save transcription"
            )
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(transcription["text"])
                result_text.insert(tk.END, f"Transcription saved as {output_path}\n")
            else:
                result_text.insert(tk.END, "Transcription not saved.\n")

        except Exception as e:
            result_text.insert(tk.END, f"An error occurred during transcription: {e}\n")
    else:
        result_text.insert(tk.END, "No file selected.\n")

# Tkinter GUI setup
root = tk.Tk()
root.title("Audio Transcription")

# GUI label
file_label = tk.Label(root, text="Select an audio file for transcription:")
file_label.pack()

# Button to select file and start transcription
open_button = tk.Button(root, text="Choose File", command=transcribe_file)
open_button.pack()

# Text widget to display transcription result and status messages
result_text = tk.Text(root, wrap=tk.WORD)
result_text.pack()

# Run the GUI loop
root.mainloop()
