from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/power', methods=['POST'])
def power():
    payload = request.get_json()
    return payload.get('state')
