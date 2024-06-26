from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import Record, VoiceResponse
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import csv
import os
import subprocess
import time
import requests

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC66a810449e6945a613d5161b54adf708'
auth_token = '90987d62cedd4ab1369f71da4c0b1d86'
from_phone_number = '+12513166471'

# Load GPT-2 model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set pad token ID to EOS token ID for open-end generation
model.config.pad_token_id = tokenizer.eos_token_id

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Directory to store call recordings
recordings_dir = 'recordings'
os.makedirs(recordings_dir, exist_ok=True)

# Function to make a call using Twilio
@app.route('/make_call', methods=['POST'])
def make_call():
    data = request.get_json()
    to_phone_number = data.get('to_phone_number')
    message = data.get('message')

    try:
        # Generate TwiML for recording a call
        twiml = generate_twiml_for_recording()
        
        # Initiate the call with Twilio
        call = client.calls.create(
            to=to_phone_number,
            from_=from_phone_number,
            twiml=twiml
        )
        
        print(f"Call to {to_phone_number} initiated successfully.")
        
        # Record call details
        record_call_details(call.sid, to_phone_number)
        
        time.sleep(10)  # Wait for call to connect (adjust as necessary)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Failed to initiate call to {to_phone_number}. Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

# Function to generate TwiML for recording a call
def generate_twiml_for_recording(timeout=10, transcribe=True):
    # Create a VoiceResponse object
    response = VoiceResponse()

    # Add a Record element to the response
    response.record(timeout=timeout, transcribe=transcribe)

    # Return the generated TwiML
    return str(response)

# Function to record call details
def record_call_details(call_sid, to_phone_number):
    # Append call details to a CSV file
    with open('call_details.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([call_sid, to_phone_number, 'initiated'])

# Function to generate response using GPT-2 model
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    response_ids = model.generate(input_ids, 
                                  max_length=1000, 
                                  num_return_sequences=1)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

# Function to handle sales process
def sales_process(phone_number, requirement):
    # Record the call
    record_command = f"some_recording_command {phone_number}"  # Replace with actual recording command
    subprocess.run(record_command, shell=True)
    
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

if __name__ == '__main__':
    app.run(debug=True)
