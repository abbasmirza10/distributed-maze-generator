from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate():
    #empty generation as given on the mp page as an eg.
    maze = ["988088c", "1000004", "1000004", "0000000", "1000004", "1000004", "3220226"]
    return jsonify({"geom": maze})

def register_mg():
    data = {
        "name": "generator1",
        "url": "http://127.0.0.1:34000/",
        "author": "abbasam2"
    }
    response = requests.put("http://127.0.0.1:5000/addMG", json=data)

if __name__ == '__main__':
    register_mg()
    app.run(host="0.0.0.0", port=34000)