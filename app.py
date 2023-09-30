import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
from moviepy.editor import VideoFileClip
import tempfile
import os

# Initialize Google Cloud client
client = speech.SpeechClient()

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript

def summarize_text(text):
    sentences = text.split('. ')
    return " ".join(sentences[:3])  # Simple extractive summary: first 3 sentences

# Streamlit UI
st.title("VidSum: Video Tutorial Summarizer")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mkv", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    # Extract audio from video
    video = VideoFileClip(tfile.name)
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    video.audio.write_audiofile(audio_file.name)

    # Transcribe audio to text
    transcript = transcribe_audio(audio_file.name)

    # Summarize the transcript
    summary = summarize_text(transcript)

    st.write("### Summary:")
    st.write(summary)

    # Cleanup temporary files
    os.remove(tfile.name)
    os.remove(audio_file.name)
