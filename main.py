import tkinter as tk
import threading
import pyaudio
import torch

# ... (existing code)

def start_transcription():
    threading.Thread(target=transcribe_real_time, daemon=True).start()
    start_button.config(state="disabled")
    stop_button.config(state="normal")

def stop_transcription():
    global should_run
    should_run = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")

def transcribe_real_time():
    global should_run
    should_run = True

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Start speaking. Press the 'Stop' button to stop.")
    while should_run:
        data = stream.read(1024, exception_on_overflow=False)
        audio = torch.from_numpy(data.astype('float32')).unsqueeze(0).to(device)
        input_values = processor(audio, sampling_rate=16000, return_tensors="pt").input_values
        output = model.generate(input_values)
        transcription = processor.decode(output[0])[0]
        print(f"Transcription: {transcription}", end="\r")

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\nStopping real-time transcription.")

# Create the Tkinter GUI
root = tk.Tk()
root.title("Real-time Speech Transcription")

start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Transcription", command=stop_transcription, state="disabled")
stop_button.pack(pady=10)

root.mainloop()
