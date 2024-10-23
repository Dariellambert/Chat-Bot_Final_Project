from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from typing import Optional, List

# Load the environment variables (API keys)
load_dotenv("gemini.env")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
else:
    print("Failed to load Gemini API key")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Custom Gemini LLM class for Langchain integration
class GeminiLLM(LLM):
    model_name: str = "models/gemini-1.5-flash"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Create a GenerativeModel object
        model = genai.GenerativeModel(model_name=self.model_name)

        # Generate the response using the Gemini API
        response = model.generate_content(prompt)

        # Extract the generated text
        if response and response.text:
            return response.text
        else:
            return "No response from Gemini API."

    @property
    def _llm_type(self) -> str:
        return "gemini_llm"

# Step 2: Initialize the Gemini LLM and use it in LangChain
gemini_llm = GeminiLLM()

# Step 3: Define a prompt template (example)
prompt_template = """
You are a helpful assistant answering questions based on the question provided by the user.

Question: {question}

Answer:
"""

# Create a Langchain prompt using the template
prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

# Step 4: Create a Langchain chain using the Gemini LLM and the prompt
chain = LLMChain(llm=gemini_llm, prompt=prompt)

# Flask route to handle user requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Use the Langchain chain to get a formatted response from Gemini LLM
    formatted_response = chain.run(user_input)

    # Return the formatted response
    return jsonify({
        'response': formatted_response
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Railway provides PORT environment variable
    app.run(host='0.0.0.0', port=port)
