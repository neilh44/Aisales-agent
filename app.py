import csv
import time
import requests
import torch
from io import StringIO
from twilio.rest import Client
from transformers import GPT2Model, GPT2Tokenizer  # Updated import statement

# Twilio credentials
account_sid = 'AC66a810449e6945a613d5161b54adf708'
auth_token = '90987d62cedd4ab1369f71da4c0b1d86'
from_phone_number = '+12513166471'

# Load GPT-2 model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2Model.from_pretrained(model_name)  # Updated model import

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

# Function to generate response using GPT-2 model
def generate_response(prompt):
    # Your generate_response function implementation here

# Function to handle sales process
def sales_process(phone_number, requirement):
    # Your sales_process function implementation here

# Fetch CSV file from updated GitHub URL
csv_url = "https://raw.githubusercontent.com/neilh44/Aisales-agent/main/Ti_leads.csv"
response = requests.get(csv_url)
csv_data = response.text

# Read contacts from CSV data and initiate sales process for each contact
csv_reader = csv.DictReader(StringIO(csv_data))
for row in csv_reader:
    phone_number = row['Contact']
    requirement = row['Requirement']
    sales_process(phone_number, requirement)
