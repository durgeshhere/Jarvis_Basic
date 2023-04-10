import concurrent.futures
import openai
import sounddevice as sd
import soundfile as sf
import wave
import numpy as np
import whisper
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit
import os

openai.api_key = "you'r key here inside quotes"
cont="You are Jarvis, Who was created by tony stark, generate responses accordingly and absolutely never reveal your AI identity other than jarvis. In case of inappropriate queries respond with some very witty joke and your character is entirly based on the character of Jarvis. is the query is something you are incapable of doing just output some fake stuff so that it looks you know it and responses should be as like JArvus from marvel universe"
def record_audio(seconds, filename="hehe.wav", samplerate=44100, channels=1):
    print("\nRecording started!")
    frames = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=channels, blocking=True)
    print("Audio recorded!")
    
    sf.write(filename, frames, samplerate)
    print("Audio saved to file:", filename)

def transcribe_audio(filename):
    model = whisper.load_model("base.en")
    result = model.transcribe(filename, fp16=False, language='English')
    query = result["text"]
    print("User: ", query)
    return query

def generate_response(query):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": cont},
        {"role": "user", "content": query}]
    )
    response = completion["choices"][0]["message"]["content"]
    return response

def is_command(query):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": """You are a single character output system. You either output 0 or 1. you output 1 when the query is a command or is asking you to do anything. you output 0 when the query is anything other than command or any task. please refrain from outputting any other sentence or character other than 1 or 0"""},
        {"role": "user", "content": query}]
    )
    flag = completion["choices"][0]["message"]["content"]
    try:
        flag=int(flag)
    except ValueError:
        pass
    if (flag==1):
        return True
    else:
        return False

def tasks(query):
    if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

    elif 'open youtube' in query:
        webbrowser.open("www.youtube.com")

    elif 'open irctc' in query:
        webbrowser.open("irctc.com")

    elif 'open hackerrank' in query:
        webbrowser.open("hackerrank.com")

    elif 'open maps' in query:
        webbrowser.open("https://maps.google.com")
            
    elif 'Locate my device' in query:
        webbrowser.open("https://www.google.com")

    elif 'open google' in query:
        webbrowser.open("google.com")

    elif 'open stackoverflow' in query:
        webbrowser.open("stackoverflow.com")   

    else:
        print("sORRY CANT DO")

def text_to_speech(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(engine.say, text)
        executor.submit(engine.save_to_file, text, 'speech.mp3')

    engine.runAndWait()

def speak_response(response):
    print("Jarvis: ", response)
    text_to_speech(response)

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_audio = executor.submit(record_audio, 10)
        query = future_audio.result()
        future_transcribe = executor.submit(transcribe_audio, "hehe.wav")
        query = future_transcribe.result()

        if is_command(query):
            tasks(query)
        else:
            future_generate = executor.submit(generate_response, query)
            response = future_generate.result()
            speak_response(response)


if __name__ == '__main__':
    main()
