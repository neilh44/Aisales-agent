import speech_recognition as sr
import subprocess
import spacy
import pyttsx3

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

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Predefined responses or knowledge base
knowledge_base = {
    "cumin seeds": {
        "price": "10 USD",
        "brand": "Pehel",
        "quality": ["S99", "Europe", "Bold"],
        "color": "Brown",
        "origin": "Ahmedabad",
        "moq": "20 kg per bag"
    }
}

# Function to perform semantic search and retrieve relevant response
def get_response(query):
    max_similarity = 0
    best_response = ""
    query_doc = nlp(query)
    for key, value in knowledge_base.items():
        response_text = f"Price: {value['price']}, Brand: {value['brand']}, Quality: {', '.join(value['quality'])}, Color: {value['color']}, Origin: {value['origin']}, MOQ: {value['moq']}"
        response_doc = nlp(response_text)
        similarity = query_doc.similarity(response_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response_text
    return best_response

# Function to convert text to speech and play it
def text_to_speech(text):
    print("Bot:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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
