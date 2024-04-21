import speech_recognition as sr
import subprocess
import spacy
from playsound import playsound
from gtts import gTTS
import tempfile
import os

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Predefined responses or knowledge base
responses = {
    "cumin seeds": {
        "price": "10 USD",
        "quality": "High",
        "brand_name": "ABC Seeds",
        "response": "The price of cumin seeds is 10 USD. They are of high quality and sold under the brand name ABC Seeds."
    }
}

# Function to convert speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

# Function to dial a phone number
def dial_phone_number(phone_number):
    subprocess.call(["xdg-open", "tel:" + phone_number])

# Function to perform semantic search and retrieve relevant response
def get_response(query):
    max_similarity = 0
    best_response = ""
    query_doc = nlp(query)
    for key, value in responses.items():
        response_doc = nlp(value["response"])
        similarity = query_doc.similarity(response_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = value["response"]
    return best_response

# Function to convert text to speech and play it

def text_to_speech(text):
    print("Bot:", text)
    tts = gTTS(text=text, lang='en')
    # Save the generated speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        tts.save(temp_audio.name)
        # Play the temporary audio file
        playsound(temp_audio.name)
    # Delete the temporary audio file after playing
    os.unlink(temp_audio.name)

def main():
    while True:
        # Convert speech to text
        query = speech_to_text()
        
        if query:
            response = get_response(query)
            if response:
                # Output response as speech
                text_to_speech(response)
            else:
                print("Bot: Sorry, I couldn't find a relevant response.")
        else:
            print("Bot: Sorry, I couldn't understand you. Could you please repeat?")

if __name__ == "__main__":
    main()
