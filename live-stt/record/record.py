import pyaudio
import wave
import threading


class Recorder:
    def __init__(self, output_filename: str, chunk=1024, format=pyaudio.paInt16s,
                 channels=2, samples_per_second=44100):
        self.chunk = chunk   # Record chunks of 1024 samples
        self.format = format
        self.channels = 2
        self.fs = samples_per_second
        self.filename = output_filename

        self.listening = False

    def _write_to_file(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def _listen(self):
        while self.listening:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def start(self):
        self.listening = True

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True
        )

        self.frames = []

        # create thread
        t = threading.Thread(target=self._listen)

    def end(self):
        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()

        self._write_to_file()


chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
