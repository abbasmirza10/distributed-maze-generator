import pytest
import json
import importlib

generators = json.load(open("generators.json","r"))


from abbasam2.mp8.MGs.static.app import app

@pytest.fixture(scope="module")
def test_dynamic():
    flask_app = importlib.import_module(generators['dynamic']).app
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope="module")
def test_static():
    flask_app = importlib.import_module(generators['static']).app
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


def unicode_vis(geom):
    cells = (
        ('┘  └',' {}{} ','┐  ┌'), # ----
        ('│  └','│{}{} ','│  ┌'), # ---w
        ('┘  └',' {}{} ','────'), # --s-
        ('│  └','│{}{} ','└───'), # --sw
        ('┘  │',' {}{}│','┐  │'), # -e--
        ('│  │','│{}{}│','│  │'), # -e-w
        ('┘  │',' {}{}│','───┘'), # -es-
        ('│  │','│{}{}│','└──┘'), # -esw
        ('────',' {}{} ','┐  ┌'), # n---
        ('┌───','│{}{} ','│  ┌'), # n--w
        ('────',' {}{} ','────'), # n-s-
        ('┌───','│{}{} ','└───'), # n-sw
        ('───┐',' {}{}│','┐  │'), # ne--
        ('┌──┐','│{}{}│','│  │'), # ne-w
        ('───┐',' {}{}│','───┘'), # nes-
        ('┌──┐','│{}{}│','└──┘'), # nesw
    )
    ans = ''
    for row in range(7):
        for tier in range(3):
            for col in range(7):
                ans += cells[int(geom[row][col],16)][tier].format(row,col)
            ans += '\n'
    return ans+str(geom)


def check_response_format(response):
    assert response.status_code == 200
    try: json = response.json
    except: assert False, "GET /generate should return JSON object"
    assert type(json) is dict
    assert 'geom' in json
    assert type(json['geom']) is list
    assert len(json['geom']) == 7
    assert all(type(s) is str for s in json['geom'])
    assert all(len(s) == 7 for s in json['geom'])
    assert all(c in '0123456789abcdefABCDEF' for s in json['geom'] for c in s)
    return json['geom']

def check_boundaries(geom):
    for i in range(7):
        problem_name = 'center opening missing' if i == 3 else 'unexpected hole'
        assert bool(int(geom[0][i],16) & 8) == (i != 3), problem_name+' in north wall of\n'+unicode_vis(geom)
        assert bool(int(geom[i][6],16) & 4) == (i != 3), problem_name+' in east wall of\n'+unicode_vis(geom)
        assert bool(int(geom[6][i],16) & 2) == (i != 3), problem_name+' in south wall of\n'+unicode_vis(geom)
        assert bool(int(geom[i][0],16) & 1) == (i != 3), problem_name+' in west wall of\n'+unicode_vis(geom)

def check_twosided(geom):
    for i in range(6):
        for j in range(7):
            assert bool(int(geom[i][j],16) & 2) == bool(int(geom[i+1][j],16) & 8), f'inconsistent wall between {(i,j)} and {(i+1,j)} in\n{unicode_vis(geom)}'
            assert bool(int(geom[j][i],16) & 4) == bool(int(geom[j][i+1],16) & 1), f'inconsistent wall between {(j,i)} and {(j,i+1)} in\n{unicode_vis(geom)}'

def test_format_static(test_static):
    response = test_static.get('/generate')
    check_response_format(response)

def test_boundaries_static(test_static):
    response = test_static.get('/generate')
    geom = check_response_format(response)
    check_boundaries(geom)

def test_twosided_static(test_static):
    response = test_static.get('/generate')
    geom = check_response_format(response)
    check_twosided(geom)
    
def test_static_is_static(test_static):
    variants = set()
    for k in range(20):
        response = test_static.get('/generate')
        geom = check_response_format(response)
        variants.add(json.dumps(geom))
    assert len(variants) == 1


def test_format_dynamic(test_dynamic):
    response = test_dynamic.get('/generate')
    check_response_format(response)

def test_boundaries_dynamic(test_dynamic):
    for k in range(10):
        response = test_dynamic.get('/generate')
        geom = check_response_format(response)
        check_boundaries(geom)

def test_twosided_dynamic(test_dynamic):
    for k in range(10):
        response = test_dynamic.get('/generate')
        geom = check_response_format(response)
        check_twosided(geom)

def test_dynamic_is_dynamic(test_dynamic):
    variants = set()
    for k in range(20):
        response = test_dynamic.get('/generate')
        geom = check_response_format(response)
        variants.add(json.dumps(geom))
    assert len(variants) >= 10

