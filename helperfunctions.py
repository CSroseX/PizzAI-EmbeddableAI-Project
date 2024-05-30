import os
from difflib import SequenceMatcher
import nltk
import glob
from zipfile import ZipFile
from nltk.corpus import stopwords
from jinja2 import *
import requests



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
from google.cloud import speech
from google.cloud import texttospeech
STT_CLIENT = speech.SpeechClient.from_service_account_file('Key.json')
TTS_CLIENT = texttospeech.TextToSpeechClient()


try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

def clean_words(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please", "the", "and",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day", "can", "could",
                       "my", "mine", "I" "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want",
                       "send", "sent", "order", "pizza", "piz", "pizze", "address", "addrez", "to", "too"])
    clean_texts = " ".join([word.replace("X","").replace] for word in text.split() if word.lower() not in stop_words)
    return clean_texts

def get_keywords(text):
    pizza_size = ["Giant", "Large", "Medium"]
    pizza_topping = ["Pepperoni", "Bacon", "Chicken", "Anchovies", "Mushroom", "Onion", "Black olive", "Green pepper"]
    order_size, order_topping = [], []
    check_size = True

    for word in text.split():
        if check_size:
            for size in pizza_size:
                if SequenceMatcher(None, word, size).ratio() > 0.6:
                    order_size.append(size)
                    check_size = False
                    break  # Stop checking sizes after a match is found
        for topping in pizza_topping:
            if SequenceMatcher(None, word, topping).ratio() > 0.6:
                order_topping.append(topping)
                break  # Stop checking toppings after a match is found

    return order_size, order_topping

    

def text_to_speech(text, name):

    
    # Check if the file exists and remove it
    if os.path.exists(name):
        os.remove(name)
        print(f"Deleted existing file: {name}")
    else:
        print(f"No existing file to delete: {name}")

    # Synthesis input
    synthesis_input = {"text": text}

    # Voice selection parameters
    voice = {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL}

    # Audio file configuration
    audio_config = {"audio_encoding": texttospeech.AudioEncoding.LINEAR16}

    # Construct the request
    request = {
        "input": synthesis_input,
        "voice": voice,
        "audio_config": audio_config,
    }

    # Send the request to the Google Cloud Text-to-Speech API
    response = TTS_CLIENT.synthesize_speech(request)

    with open(name, "bx") as f:
        f.write(response.audio_content)

    print('Audio content written to file "' + name + '.wav"')





def speech_to_text(file_name):

    with open(file_name, 'rb') as f:
        wav = f.read()
        print(f)

    audio_file = speech.RecognitionAudio(content=wav)

    config = speech.RecognitionConfig(
        enable_automatic_punctuation = True,
        language_code = 'en-US'
    )

    response = STT_CLIENT.recognize(
        config=config,
        audio=audio_file
    )

    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript




def play_local_wav_file(file_name):
    with open(str("./" + file_name), "rb") as wav:
        data = wav.read(1024)
        while data:
            yield data
            data = wav.read(1024)
    # audio = AudioSegment.from_wav(file_name)
    # chunk_size = 1024
    # for i in range(0, len(audio), chunk_size):
    #     yield audio[i:i+chunk_size].raw_data




def read_zip_file(zip_name):
    files = str(os.getcwd() + "/" + zip_name + ".zip")
    with ZipFile(files, "r") as zip_object:
        zip_object.extractall()

    path = str(os.getcwd() + "/" + zip_name + "/*.wav")
    folder = glob.glob(path)
    return sorted(folder, reverse=False)


def save_audio(file, file_name):
    with open(file_name, "wb") as audio:
        file.save(audio)
        print("file uploaded successfully")

# Testing 
# result = "how's it going? Where should we send your delicious pizza order to?"
# getinfo = "getinfo"
# text_to_speech(result,getinfo)