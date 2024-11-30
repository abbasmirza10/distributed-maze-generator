import random
from re import S
import requests
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

servers = []

# lists of MG names and weights for random.choices
names = []
weights = []


def update_rng():
    '''Update `names` and `weights` variables'''
    global servers, names, weights
    for server in servers:
        names += [server['name']]
        weights += [server['weight']]
    pass


@app.route('/', methods=["GET"])
def GET_index():
    '''Route for "/" (frontend)'''
    return render_template("index.html")


@app.route('/generateSegment', methods=["GET"])
def gen_rand_maze_segment():
    '''Route for maze generation with random generator'''
    global servers, names, weights

    if not servers:
        return 'No maze generators available', 503

    mg_name = random.choices(names, weights=weights)[0]
    return gen_maze_segment(mg_name)


@app.route('/generateSegment/<mg_name>', methods=['GET'])
def gen_maze_segment(mg_name: str):
    '''Route for maze generation with specific generator'''
    global servers
    
    server = None

    for s in servers:
        if s['name'] == mg_name:
            server = s
            break

    if not server:
        return 'Maze generator not found', 404

    mg_url = server['url']

    if mg_url[-1] == '/':  # handle trailing slash
        mg_url = mg_url[:-1]

    r = requests.get(f'{mg_url}/generate', params=dict(request.args))

    if int(r.status_code / 100) != 2:  # if not a 200-level response
        return 'Maze generator error', 500

    return jsonify(r.json())


@app.route('/addMG', methods=['PUT'])
def add_maze_generator():
    '''Route to add a maze generator'''

    # Validate packet:
    for requiredKey in ['name', 'url', 'author']:
        if requiredKey not in request.json.keys():
            return f'Key "{requiredKey}" missing', 400

    if 'weight' in request.json.keys():
        new_weight = request.json['weight']
        if new_weight <= 0:
            return 'Weight cannot be 0 or negative', 400
    else:
        new_weight = 1

    server = {
        'name': request.json['name'],
        'url': request.json['url'],
        'author': request.json['author'],
        'weight': new_weight
    }

    servers.append(server)

    update_rng()
    return 'OK', 200


@app.route('/servers', methods=['GET'])
def FindServers():
    global servers
    return render_template('servers.html', data={"servers": servers})


@app.route('/listMG', methods=['GET'])
def list_maze_generators():
    '''Route to get list of maze generators'''
    global servers
    return jsonify(servers), 200
