import csv
import time
from twilio.rest import Client
from transformers import AutoModelForCausalLM, AutoTokenizer

# Twilio credentials
account_sid = 'AC66a810449e6945a613d5161b54adf708'
auth_token = '90987d62cedd4ab1369f71da4c0b1d86'
from_phone_number = '+12513166471'

# Load Mistral 8B model
model_name = "EleutherAI/mistral-cyt-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Function to make a call using Twilio
def make_call(to_phone_number, message):
    try:
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=to_phone_number,
            from_=from_phone_number,
            method='GET'
        )
        print(f"Call to {to_phone_number} initiated successfully.")
        time.sleep(10)  # Wait for call to connect (adjust as necessary)
    except Exception as e:
        print(f"Failed to initiate call to {to_phone_number}. Error: {str(e)}")

# Function to generate response using Mistral 8B model
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=1000, num_return_sequences=1)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

# Function to handle sales process
def sales_process(phone_number, requirement):
    make_call(phone_number, "Hello! We have noticed that you might be interested in our products. Let me tell you more about them.")
    # Wait for call to be connected
    time.sleep(30)  # Adjust as necessary
    # Generate response based on requirement
    response = generate_response(requirement)
    print("Agent: " + response)
    # Promote the product
    response = generate_response("Promote product")
    print("Agent: " + response)
    # Upsell or cross-sell
    response = generate_response("Upsell or cross-sell")
    print("Agent: " + response)
    # Close the deal
    response = generate_response("Close the deal")
    print("Agent: " + response)
    # Follow up for upcoming requirement
    response = generate_response("Follow up for upcoming requirement")
    print("Agent: " + response)

# Function to read contacts from CSV file and initiate sales process for each contact
def initiate_sales(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            phone_number = row['Phone']
            requirement = row['Requirement']
            sales_process(phone_number, requirement)

# Main function
if __name__ == "__main__":
    csv_file = "contacts.csv"  # Change to your CSV file name
    initiate_sales(csv_file)
