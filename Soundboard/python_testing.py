import sounddevice as sd
import os
import subprocess
from mutagen import File as MutagenFile
import soundfile as sf

audio_files = [f"sounds/{file}" for file in os.listdir('sounds')]

print(f"\n{audio_files}\n")

data, samplerate = sf.read(f"{audio_files[4]}")

sd.play(data, samplerate = samplerate, device  = 6)
sd.wait()