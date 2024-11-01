import whisper
import tkinter as tk
from tkinter import filedialog
import warnings
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import pyaudio

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Disable FP16 to avoid the warning
torch.set_float32_matmul_precision('high')

# Load the Transformer-based speech recognition model
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using GPU for speech recognition.")
else:
    device = torch.device("cpu")
    print("Using CPU for speech recognition.")

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(device)

# Function to transcribe a selected audio file
def transcribe_file():
    try:
        # Open file dialog to select an audio file
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select an audio file for transcription",
            filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.ogg"), ("All Files", "*.*"))
        )

        if file_path:
            print(f"Transcribing {file_path}...")
            audio, sample_rate = torchaudio.load(file_path)
            audio = audio.to(device)
            input_values = processor(audio, sampling_rate=sample_rate, return_tensors="pt").input_values
            output = model.generate(input_values)
            transcription = processor.decode(output[0])[0]
            print("Transcription complete.")

            # Save transcription to a text file
            output_path = f"{file_path}_transcription.txt"
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(transcription)
                print(f"Transcription saved as {output_path}\n")
            except UnicodeEncodeError as e:
                print(f"An error occurred while saving the transcription: {e}")
                print("The transcription could not be saved due to unsupported characters.")
        else:
            print("No file selected.")

    except Exception as e:
        print(f"An error occurred during transcription: {e}")

# Function to transcribe audio in real-time
def transcribe_real_time():
    try:
        # Open the audio stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

        print("Start speaking. Press Ctrl+C to stop.")
        while True:
            data = stream.read(1024)
            audio = torch.from_numpy(data.astype('float32')).unsqueeze(0).to(device)
            input_values = processor(audio, sampling_rate=16000, return_tensors="pt").input_values
            output = model.generate(input_values)
            transcription = processor.decode(output[0])[0]
            print(f"Transcription: {transcription}", end="\r")

    except KeyboardInterrupt:
        print("\nStopping real-time transcription.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Run the transcription functions
transcribe_file()
transcribe_real_time()
