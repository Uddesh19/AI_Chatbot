from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your Hugging Face API token
HF_TOKEN = "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"  # <-- put your token here

# Hugging Face model endpoint
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Function to query Hugging Face API
def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # Debugging: print full API response in terminal
    print("API Response:", result)

    # Normal case
    if isinstance(result, list) and 'generated_text' in result[0]:
        return result[0]['generated_text']

    # Error case
    elif 'error' in result:
        return "API Error: " + result['error']

    else:
        return "No valid response from AI model."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_response():
    user_message = request.form['msg']
    bot_reply = query_huggingface(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
