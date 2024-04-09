import openai
from dotenv import find_dotenv, load_dotenv


load_dotenv()

client = openai.OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=input("Input for an audio file: ")
)

response.stream_to_file("audio_file/output.mp3")