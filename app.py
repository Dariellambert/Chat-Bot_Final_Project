import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st

# Load the pre-trained GPT-2 model
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Function to handle QA queries
def handle_qa_query(question):
    inputs = tokenizer.encode(question, return_tensors='pt')
    outputs = model.generate(
        inputs,
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        temperature=0.5,   # Lower temperature for more focused answers
        top_k=50,          # Limit to top 50 tokens
        top_p=0.9,         # Nucleus sampling
        early_stopping=True
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()

# Streamlit UI
st.title("Trivia Chatbot AI Bootcamp")

# Input form for trivia question
trivia_question = st.text_input("Ask a trivia question:", placeholder="What is the capital of France?")

# Button to get the answer
if st.button("Get Answer"):
    if trivia_question.strip():
        with st.spinner("Thinking..."):
            response = handle_qa_query(trivia_question)
        # Display the response
        st.subheader("Trivia Answer:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
        
# Sidebar information
st.sidebar.title("About")
st.sidebar.info("""
Chatbot that need a lot of improvement. deadline and my job are so tight.
""")
