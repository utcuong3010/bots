

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Define the URL of the API endpoint
API_URL = 'http://35.220.225.3:30001/api/v1/market/listing'

@app.route('/')
def index():
    try:
        # Make the GET request to the API
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()  # Parse the JSON response
    except requests.RequestException as e:
        # Handle exceptions and provide a friendly error message
        data = {'error': str(e)}
    
    return render_template('index.html', data=data)

@app.route('/api/data')
def api_data():
    try:
        # Make the GET request to the API
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()  # Parse the JSON response
    except requests.RequestException as e:
        # Handle exceptions and provide a friendly error message
        data = {'error': str(e)}
    
    return jsonify(data)

if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug=True)
    app.run(host='0.0.0.0', port=50001, debug=True)

