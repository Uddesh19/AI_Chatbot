from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv   # <-- import dotenv

# Load variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable (stored in .env)
PERPLEXITY_API_KEY = os.getenv("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")

# Perplexity API endpoint (chat completion)
API_URL = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json"
}

def query_perplexity(prompt):
    payload = {
        "model": "sonar-small-chat",  # You can change the model if needed
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    
    # Debugging: print full API response in terminal
    print("API Response:", result)
    
    # Get reply text safely
    if "choices" in result and len(result["choices"]) > 0 and "message" in result["choices"][0]:
        return result["choices"][0]["message"]["content"]
    elif "error" in result:
        return "API Error: " + str(result["error"])
    else:
        return "No valid response from Perplexity API."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_response():
    user_message = request.form['msg']
    bot_reply = query_perplexity(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
