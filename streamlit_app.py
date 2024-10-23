import streamlit as st
import requests
import json
import html

# Trivia API URL (or your own trivia question source)
TRIVIA_API_URL = 'https://opentdb.com/api.php?amount=1&type=multiple'

# Set up the page title and header
st.title('Trivia Chatbot')


# Function to get a random trivia question
def get_random_question():
    response = requests.get(TRIVIA_API_URL)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0:
            question = data['results'][0]['question']
            question = html.unescape(question)  # Decode HTML entities
            return question
    return "No trivia question available."


# Initialize session state for user input and history
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []  # To store questions and answers

# Add a sidebar for question and answer history
with st.sidebar:
    st.image("trivia-chatbot-circle.png", use_column_width=True)

    st.header("About")
    st.write("This Dariel Lambert Wahyudiono's Trivia Chat Bot for AI Bootcamp Final Project, just ask your trivial question or generate random question by pressing the button")

    st.write("## Question & Answer History")
    # Display the history of questions and answers
    if st.session_state['history']:
        for q, a in st.session_state['history']:
            st.write(f"**Q**: {q}")
            st.write(f"**A**: {a}")
            st.write("---")
    else:
        st.write("No interactions yet.")

# Add a button to generate a random question and populate the input field
if st.button('Generate Random Question'):
    random_question = get_random_question()
    st.session_state['user_input'] = random_question  # Update session state with random question

# Create a text input for user to type their question, pre-filled with session state
user_input = st.text_input("Your Question:", value=st.session_state['user_input'], key='user_input')

# When the user clicks the "Send" button
if st.button('Send'):
    if user_input:
        # Send the user input to the Flask backend
        response = requests.post(
            "https://chat-botfinalproject-production.up.railway.app/chat",  # Adjust this URL to match where your Flask server is running
            headers={"Content-Type": "application/json"},
            data=json.dumps({"message": user_input})
        )

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                answer = data['response']
                # Display the answer
                st.write(f"**Answer**: {answer}")
                # Append the question and answer to the session state history
                st.session_state['history'].append((user_input, answer))
            else:
                st.write("The chatbot did not understand the question.")
        else:
            st.write("Error: Could not get a response from the chatbot.")
    else:
        st.write("Please enter a message.")
