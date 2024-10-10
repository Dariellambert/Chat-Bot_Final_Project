from flask import Flask, request, render_template
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Initialize the Flask app
app = Flask(__name__)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Function to generate trivia responses using GPT-2
def generate_trivia_response(question):
    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=150, num_beams=5, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.form['msg']
    response = generate_trivia_response(user_input)
    return response

if __name__ == "__main__":
    app.run(debug=True)
