from flask import Flask, render_template, request, jsonify
from workflowAPI import process_new_episode, get_secret_from_key_vault
from threading import Thread


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Try to read the updated bullet points from response.txt
    try:
        with open('workload/response.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        bullet_points = content.split('\n')  # Assuming each bullet point is on a new line
    except FileNotFoundError:
        bullet_points = ["No summary available."]
    
    # Render the home page with bullet points
    return render_template('index.html', bullet_points=bullet_points)

@app.route('/trigger-processing', methods=['POST'])
def trigger_processing():
    # Simple token-based authentication
    expected_token = get_secret_from_key_vault("https://vault57765.vault.azure.net/", "apitoken")
    incoming_token = request.headers.get('Authorization')
    
    if not incoming_token or incoming_token != f"Bearer {expected_token}":
        return jsonify({"error": "Unauthorized"}), 401
# Define a function to run the process in a new thread
    def start_process_new_episode():
        process_new_episode()
    
    # Start the thread
    thread = Thread(target=start_process_new_episode)
    thread.start()
    
    # Return immediately to the client
    return jsonify({"message": "Episode processing started"}), 202

if __name__ == '__main__':
    app.run(debug=True)
