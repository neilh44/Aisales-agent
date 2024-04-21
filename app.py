import speech_recognition as sr
import subprocess

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

# Function to provide information about cumin seeds
def pitch_cumin_seeds():
    # Your logic to fetch cumin seeds information from a database or API
    price = "10 USD"
    quality = "High"
    brand_name = "ABC Seeds"
    return f"The price of cumin seeds is {price}. They are of {quality} quality and sold under the brand name {brand_name}."

# Function to convert text to speech and play it
def text_to_speech(text):
    os.system(f"say '{text}'")

def main():
    while True:
        # Convert speech to text
        query = speech_to_text()
        
        if query:
            if "cumin seeds" in query:
                response = pitch_cumin_seeds()
            elif "dial" in query:
                # Extract the phone number from the query
                words = query.split()
                phone_number = next((word for word in words if word.isdigit() and len(word) == 10), None)
                if phone_number:
                    dial_phone_number(phone_number)
                    response = f"Dialing {phone_number}..."
                else:
                    response = "Please provide a valid 10-digit phone number to dial."
            else:
                response = "Sorry, I didn't understand your query."
            
            # Output response as speech
            text_to_speech(response)
        else:
            print("Bot: Sorry, I couldn't understand you. Could you please repeat?")

if __name__ == "__main__":
    main()
