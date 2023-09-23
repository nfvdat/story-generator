from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set OpenAI API key from environment variable
openai.api_key  = os.getenv('OPENAI_API_KEY')

# Create a Flask web server
app = Flask(__name__)
# Enable CORS for the Flask app
CORS(app)

# Dictionary to hold multiple conversations. Each conversation corresponds to a different bot.
conversations = {}

# Function to get the last 500 words from a conversation.
def get_last_500_words(conversation):
    all_words = " ".join([m["content"] for m in conversation])
    return " ".join(all_words.split()[-500:])

# Function to call OpenAI API for a conversation and return the model's response.
def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=150,
    )
    r = response.choices[0].message["content"]
    return r[:r.rindex(".") + 1]

# Main landing page
@app.route('/')
def index():
    return render_template('main.html')

# Route to generate the AI's response given a story and story idea
@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        model = data.get('model', 'gpt-3.5-turbo')
        story = data.get('story')  # get the story from the request
        story_idea = data.get('story_idea')  # get the story idea from the request

        with open('static/personalities.json') as f:
            personalities = json.load(f)['Personalities']
        if bot_id not in personalities:
            return jsonify({"error": "Bot id not found"}), 404

        character_prompt = personalities[bot_id]

        if bot_id not in conversations:
            conversations[bot_id] = [{"role": "assistant", "content": character_prompt}]
        conversation = conversations[bot_id]

        # Combine the story idea with the story
        conversation.append({"role": "user", "content": story_idea + ' ' + story})  
        
        response = get_completion(conversation, model)
        conversation.append({"role": "assistant", "content": response})

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete the last response of the bot
@app.route('/api/delete_last', methods=['POST'])
def delete_last():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if bot_id in conversations and len(conversations[bot_id]) > 0:
        conversations[bot_id].pop()
    return jsonify({"status": "last response deleted"})

# Run the Flask app on port 5000 with debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000)
