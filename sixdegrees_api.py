from flask import Flask, redirect, url_for, request, render_template
from neo4j import GraphDatabase
from py2neo import Graph
import json
import os


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
uri = app.config.get('NEO_URI')
pwd = app.config.get('NEO_PWD')
general_image_dir = app.config.get('GENERAL_IMAGES_DIR')
team_image_dir = app.config.get('TEAM_IMAGE_DIR')
player_image_dir = app.config.get('PLAYER_IMAGE_DIR')
bball_ref_url = app.config.get('BBALL_REFERENCE_URL')

driver = GraphDatabase.driver(uri, auth=("neo4j", pwd))
PLAYER1_PARAM = 'player1ID'
PLAYER2_PARAM = 'player2ID'
NEWLINE = '</br>'
TR = '<tr style="border: none;">'
TD = '<td align="center" style="border: none;">'
TD_2 = '<td colspan=2 align="center" style="border: none;">'
img_down_arrow = f'{TR}{TD_2}<img src="{general_image_dir}blue_arrow_down_small.png" alt="down arrow"></td></tr>'


def all_people() -> json:
    print('getting cache')
    query = f"""MATCH (p:Person)
        RETURN p.playerID as playerID, p.name + ' ' + left(p.debut,4) + ' - ' + left(p.finalGame, 4) AS name
        ORDER BY p.nameLast      
        """
    ret_val = session.run(query)
    return ret_val.data() 

def find_person(name: str) -> json:
    print(f'finding {name}')
    query = f"""MATCH (p:Person)
        WHERE toLower(p.name) Starts with toLower($p1) 
        or toLower(p.nameLast) starts with toLower($p2)
        RETURN p.playerID as playerID, p.name AS name, p.nameGiven as nameGiven, 
        p.nameLast as nameLast, p.debut AS debut, p.finalGame as finalGame
        """
    ret_val = session.run(query, p1=name, p2=name)
    return ret_val.data()   

def determine_degrees(start_player: str, end_player: str = 'moyerja01') -> json:
    query = f"""MATCH
            (p1:Person %%playerID:'{start_player}'$$),
            (p2:Person %%playerID:'{end_player}'$$),
            p = shortestPath((p1)-[:MEMBER_OF*]-(p2))
            RETURN p"""
    query = query.replace('%%', '{').replace('$$','}')
    ret_val = session.run(query)
    return ret_val.data() 

def build_bball_link(playerID: str):
    return bball_ref_url.replace("@@playerID@@", playerID).replace("@@alpha@@", playerID[:1])

def build_player_image(playerID : str, name : str) -> str:
    if os.path.exists(f'{player_image_dir}{playerID}.jpg'):
        return f'<img src="{player_image_dir}{playerID}.jpg" alt="{name}">'
    else:
        return ''

def draw_path(path: [], end_player: str)->str:
    #logos found at: 
    #https://www.sportslogos.net/teams/list_by_league/53/American_League/AL/logos/
    len_list = len(path[0]['p'])-1
    ret_val = '<div align=center>'
    ret_val = '<table align=center style="border: none;">'
    last_team = ''
    item_count = 0
    for item in path[0]['p']:
        item_count+=1
        if 'playerID' in item:
            playerID = item["playerID"]
            name = item["name"]
            print(f'Player: {playerID} - {name}') 
            link = build_bball_link(playerID)
            image = build_player_image(playerID, name)
            ret_val = ret_val + f'{TR}{TD_2}<a href="{link}" target="_blank">{image}</br>{name}</a></td></tr>'
            ret_val = ret_val + f'<script>fetchPlayerImage({playerID});</script>'
            if item["playerID"] != end_player:
                #ret_val = ret_val + img_down_arrow
                ret_val = ret_val + '<tr><td>Played For:</td></tr>'
        elif 'team_year' in item:
            print(f'Team: {item["franchiseName"]}  -  {item["year"]}')
            last_team = f'{TD}<img src="{team_image_dir}{item["franchiseID"]}.gif" alt="{item["franchiseName"]}"></td>{TD} in {item["year"]}</td>' + NEWLINE
            ret_val = ret_val + last_team + '<tr><td>Played With:</td></tr>' + NEWLINE
        else:
            continue
        if item_count < len_list:
            print('   |   ')
            print('   v   ')
    ret_val = ret_val + "</table>"
    ret_val = ret_val + "</div>"
    return ret_val

with driver.session(database="neo4j") as session:
    print('cache people')
    player_cache = all_people()
    @app.route('/')
    #@app.route('/test')
    def index():
        if PLAYER1_PARAM not in request.args:
            return render_template('index2.html', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str='')
        else:
            player1ID = request.args.get(PLAYER1_PARAM)
            player2ID = request.args.get(PLAYER2_PARAM)
            print(f'getting {player1ID} -> {player2ID} info') 
            path = determine_degrees(player1ID, player2ID)
            path_str = draw_path(path, player2ID)
            return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)
    
    @app.route('/', methods=['POST'])
    def show_person():
        player1ID = request.form[PLAYER1_PARAM]
        player2ID = request.form[PLAYER2_PARAM]
        print(f'getting {player1ID} -> {player2ID} info') 
        path = determine_degrees(player1ID, player2ID)
        path_str = draw_path(path, player2ID)
        return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)
    app.run(host='0.0.0.0', port=5000, debug=True)
driver.close()
