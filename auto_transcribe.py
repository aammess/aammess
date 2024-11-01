import whisper  # Import the Whisper library for speech recognition
import tkinter as tk  # Import the tkinter library for GUI
from tkinter import filedialog  # Import file dialog for file selection
import warnings  # Import warnings to manage warning messages
import torch  # Import PyTorch library for tensor computations

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Disable FP16 to avoid the warning
torch.set_float32_matmul_precision('high')

# Load the Whisper model for CPU
try:
    model = whisper.load_model("base", device="cpu")  # Use "base" model and CPU only
    print("Model loaded successfully.")  # Print success message
except Exception as e:
    print(f"Failed to load the model: {e}")  # Print error if model loading fails
    exit()  # Exit the program if model loading fails

# Function to open file dialog and transcribe file
def transcribe_file():
    try:
        # Open file dialog to select an audio file
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(
            title="Select an audio file for transcription",  # Dialog title
            filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.ogg"), ("All Files", "*.*"))  # Supported file types
        )

        if file_path:  # Check if a file was selected
            print(f"Transcribing {file_path}...")  # Print the file being transcribed
            # Transcribe the selected file
            result = model.transcribe(file_path)
            print("Transcription complete.")  # Print completion message

            # Save transcription to a text file
            output_path = f"{file_path}_transcription.txt"  # Define output file path
            try:
                with open(output_path, "w", encoding="utf-8") as f:  # Open output file for writing
                    f.write(result["text"])  # Write transcription text to file
                print(f"Transcription saved as {output_path}\n")  # Print success message for saving
            except UnicodeEncodeError as e:
                print(f"An error occurred while saving the transcription: {e}")  # Print error if saving fails
                print("The transcription could not be saved due to unsupported characters.")  # Print message for unsupported characters
        else:
            print("No file selected.")  # Print message if no file was selected

    except Exception as e:
        print(f"An error occurred during transcription: {e}")  # Print error if transcription fails

# Run the transcription function
transcribe_file()  # Call the function to execute transcription
