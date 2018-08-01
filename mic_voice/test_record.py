import os
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=5)
    print("Say something!")
    audio = r.listen(source)

# write audio to a RAW file
with open(os.getcwd()+"/voice/microphone-results.raw", "wb") as f:
    f.write(audio.get_raw_data())

# write audio to a WAV file
with open(os.getcwd()+"/voice/microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())

# write audio to an AIFF file
with open(os.getcwd()+"/voice/microphone-results.aiff", "wb") as f:
    f.write(audio.get_aiff_data())

# write audio to a FLAC file
with open(os.getcwd()+"/voice/microphone-results.flac", "wb") as f:
    f.write(audio.get_flac_data())
