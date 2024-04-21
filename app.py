import streamlit as st
import sounddevice as sd
import numpy as np

def record_audio(duration):
    fs = 44100  # Sample rate
    seconds = duration  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    return myrecording

def main():
    st.title("Audio Recorder")
    duration = st.slider("Duration (seconds):", min_value=1, max_value=10, value=3)

    if st.button("Record"):
        st.write("Recording...")
        recording = record_audio(duration)
        st.write("Recording finished!")
        st.audio(recording, format="audio/wav")

if __name__ == "__main__":
    main()
