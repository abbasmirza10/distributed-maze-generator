from mazelib import Maze
import random
from flask import Flask, jsonify
import requests

app = Flask(__name__)

def generate_two_sided_maze():
    maze = Maze()
    maze.removeAllWalls()
    for i in range(1, 6):
        for j in range(1, 6):
            if random.choice([True, False]):
                maze.addWall((j, i), 'north')
            if random.choice([True, False]):
                maze.addWall((j, i), 'east')
    return maze.sendable()

@app.route('/generate', methods=['GET'])
def generate():
    maze = generate_two_sided_maze()
    return jsonify({"geom": maze})

def register_mg():
    data = {
        "name": "generator2",
        "url": "http://127.0.0.1:35000/",
        "author": "abbasam2"
    }
    response = requests.put("http://127.0.0.1:5000/addMG", json=data)

if __name__ == '__main__':
    register_mg()
    app.run(host="0.0.0.0", port=35000)