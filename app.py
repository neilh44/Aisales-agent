import streamlit as st
import requests

# Streamlit UI
st.title('Twilio Dialer')

# Start/Stop button
start_stop_button = st.button('Start Dialing')

# Function to start dialing process
def start_dialing():
    # Request the Flask server to start dialing
    response = requests.get('http://localhost:5000/start_dialing')
    if response.status_code == 200:
        st.write("Dialing process started successfully!")
    else:
        st.write("Failed to start dialing process.")

# Handle button click event
if start_stop_button:
    start_dialing()
