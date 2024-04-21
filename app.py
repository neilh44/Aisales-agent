import speech_recognition as sr
import subprocess
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

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

# Function to perform semantic search and retrieve relevant response
def get_response(query):
    max_similarity = 0
    best_response = ""
    for key, value in knowledge_base.items():
        response_text = f"Price: {value['price']}, Brand: {value['brand']}, Quality: {', '.join(value['quality'])}, Color: {value['color']}, Origin: {value['origin']}, MOQ: {value['moq']}"
        similarity = get_similarity(query, response_text)
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response_text
    return best_response

# Function to calculate similarity between two texts
def get_similarity(text1, text2):
    # Here you can use spaCy or any other library to calculate similarity
    # For simplicity, let's assume the texts are the same for now
    return 1.0

def main():
    while True:
        # Convert speech to text
        query = speech_to_text()
        
        if query:
            response = get_response(query)
            if response:
                # Output response as speech
                engine.say(response)
                engine.runAndWait()
            else:
                print("Bot: Sorry, I couldn't find a relevant response.")
        else:
            print("Bot: Sorry, I couldn't understand you. Could you please repeat?")

if __name__ == "__main__":
    main()
