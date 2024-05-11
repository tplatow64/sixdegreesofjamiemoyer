from flask import Flask, redirect, url_for, request, render_template
from neo4j import GraphDatabase
from py2neo import Graph
import json
import os
import requests


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
uri = app.config.get('NEO_URI')
pwd = app.config.get('NEO_PWD')
general_image_dir = app.config.get('GENERAL_IMAGES_DIR')
franchise_image_dir = app.config.get('FRANCHISE_IMAGE_DIR')
team_image_dir = app.config.get('TEAM_IMAGE_DIR')
player_image_dir = app.config.get('PLAYER_IMAGE_DIR')
bball_ref_url = app.config.get('BBALL_REFERENCE_URL')
not_found_image = '_notfound'

print('connecting')
driver = GraphDatabase.driver(uri, auth=("neo4j", pwd))
print('connected')
neo4J_session = driver.session(database="neo4j")
print('neo session created')
PLAYER1_PARAM = 'player1ID'
PLAYER2_PARAM = 'player2ID'
JAMIE_ID = 'moyerja01'
NEWLINE = '<br>'
TR = '<tr style="border: none;" align="left">'
TD = '<td align="left" style="border: none;">'
FONT_SPAN_RED = """
<b><span
style='font-size:16.0pt;font-family:"Verdana";mso-fareast-font-family:
"Times New Roman";mso-bidi-font-family:Arial;color:#C00000'>
"""
FONT_SPAN_BLACK = """
<b><span
style='font-size:16.0pt;font-family:"Verdana";mso-fareast-font-family:
"Times New Roman";mso-bidi-font-family:Arial;'>
"""
END_FONT_SPAN = "</b></span>"


def all_people() -> json:
    print('getting cache')
    query = f"""MATCH (p:Person)
        WHERE p.debut <> ""
        RETURN p.playerID as playerID, p.name + ' ' + left(p.debut,4) + ' - ' + left(p.finalGame, 4) AS name
        ORDER BY p.nameLast      
        """
    ret_val = neo4J_session.run(query)
    return ret_val.data() 

def find_person(name: str) -> json:
    print(f'finding {name}')
    query = f"""MATCH (p:Person)
        WHERE toLower(p.name) Starts with toLower($p1) 
        or toLower(p.nameLast) starts with toLower($p2)
        RETURN p.playerID as playerID, p.bbrefid as bbrefid, p.name AS name, p.nameGiven as nameGiven, 
        p.nameLast as nameLast, p.debut AS debut, p.finalGame as finalGame,
        p.imageUrl as imageUrl
        """
    ret_val = neo4J_session.run(query, p1=name, p2=name)
    return ret_val.data()   

def determine_degrees(start_player: str, end_player: str = JAMIE_ID) -> json:
    print('determine degrees')
    query = f"""MATCH
            (p1:Person %%playerID:'{start_player}'$$),
            (p2:Person %%playerID:'{end_player}'$$),
            p = shortestPath((p1)-[:MEMBER_OF*]-(p2))
            RETURN p"""
    query = query.replace('%%', '{').replace('$$','}')
    ret_val = neo4J_session.run(query)
    return ret_val.data() 

def build_bball_link(bbrefid: str):
    print('build bball link')
    return bball_ref_url.replace("@@playerID@@", bbrefid).replace("@@alpha@@", bbrefid[:1])

def build_player_image(item: object) -> str:
    print('build player image')
    # if(os.path.exists(f"{player_image_dir}{item["playerID"]}.jpg")):
    #     return f'<img src="{player_image_dir}{item["playerID"]}.jpg" alt="{item['name']}">'
    if(item['imageUrl'] != ''):
        response = requests.get(f'{item['imageUrl']}')
        if response.status_code == 200:
            return f'<img src="{item['imageUrl']}" alt="{item['name']}">'

    return f'<img src="{player_image_dir}{not_found_image}.jpg" alt="{item['name']}">'

def draw_same_person_path()->str:
    print('draw same person')
    ret_val = '<div align=center>'
    ret_val = ret_val + '<table align=center style="border: none;">'
    ret_val = ret_val + TR + TD
    ret_val = ret_val + "Please choose different starting and ending people"
    ret_val = ret_val + "</td></tr>"
    ret_val = ret_val + "</table>"
    ret_val = ret_val + "</div>"
    return ret_val

def path_team(item: object) -> str:
    print('path team called')
    print(f'Team: {item["franchiseName"]}  -  {item["year"]}')
    ret_val = draw_team_logo(item)
    ret_val = ret_val + f'{TD}{FONT_SPAN_BLACK}{item["teamName"]}{END_FONT_SPAN}<br>'
    ret_val = ret_val + f'{FONT_SPAN_BLACK} in {item["year"]}{END_FONT_SPAN}</td>'
    ret_val = ret_val + f'<tr>{TD}{FONT_SPAN_BLACK}WITH{END_FONT_SPAN}</td></tr>'
    return ret_val

def draw_team_logo(item: object) -> str:
    print('draw team logo')
    team_logo_path = f'{team_image_dir}{item["year"]}/{item["teamID"]}.gif'
    if os.path.exists(team_logo_path):
        ret_val = f'{TD}<img src="{team_logo_path}" alt="{item["teamName"]}" title="{item["teamName"]}"></td>'
    else:
        franchise_logo_path = f'{franchise_image_dir}{item["franchiseID"]}.gif'
        if(os.path.exists(franchise_logo_path)):
            ret_val = f'{TD}<img src="{franchise_logo_path}" alt="{item["franchiseName"]}" title="{item["franchiseName"]}"></td>'
        else:
            unknown_path = f'{franchise_image_dir}__not_found.gif'
            ret_val = f'{TD}<img src="{unknown_path}" alt="{item["franchiseName"]}" title="{item["franchiseName"]}"></td>'
    return ret_val



def path_player(end_player: str, item_count: int, item: object) -> str:
    print('path player')
    playerID = item["playerID"]
    bbrefid = item["bbrefid"]
    name = item["name"]
    print(f'Player: {playerID} - {name}') 
    link = build_bball_link(bbrefid)
    image = build_player_image(item)
    ret_val = f'{TR}{TD}<a href="{link}" target="_blank">{image}{NEWLINE}</a></td>'
    ret_val = ret_val + f'{TD}<a href="{link}" target="_blank">{NEWLINE}{FONT_SPAN_RED}{name}{END_FONT_SPAN}</a>'
    if item["playerID"] != end_player:
        if item_count == 1:
            ret_val = ret_val + f'<tr>{TD}{FONT_SPAN_BLACK}PLAYED FOR{END_FONT_SPAN}</td></tr>'
        else:
            ret_val = ret_val + f'<tr>{TD}{FONT_SPAN_BLACK}WHO PLAYED FOR{END_FONT_SPAN}</td></tr>'
    return ret_val

def draw_path(path: object, end_player: str)->str:
    print('draw path')
    #logos found at: 
    #https://www.sportslogos.net/teams/list_by_league/53/American_League/AL/logos/
    len_list = len(path[0]['p'])-1
    ret_val = '<div align=center>'
    ret_val = ret_val + '<table align=center style="border: none;">'
    last_team = ''
    item_count = 0
    for item in path[0]['p']:
        item_count+=1
        if 'playerID' in item:
            # print(item)
            ret_val = ret_val + path_player(end_player, item_count, item)
        elif 'team_year' in item:
            ret_val = ret_val + path_team(item)
        else:
            continue
        if item_count < len_list:
            print('   |   ')
            print('   v   ')
    ret_val = ret_val + "</table>"
    ret_val = ret_val + "</div>"
    return ret_val


print('cache people')
player_cache = all_people()
@app.route('/')
def index():
    print('index called')
    if PLAYER1_PARAM not in request.args:
        return render_template('index2.html', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str='')
    else:
        player1ID = request.args.get(PLAYER1_PARAM)
        player2ID = request.args.get(PLAYER2_PARAM)
        print(f'getting {player1ID} -> {player2ID} info') 
        if player1ID == player2ID:
            path_str = draw_same_person_path()
            return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)
        path = determine_degrees(player1ID, player2ID)
        path_str = draw_path(path, player2ID)
        return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)

@app.route('/', methods=['POST'])
def show_person():
    print('show person')
    player1ID = request.form[PLAYER1_PARAM]
    player2ID = request.form[PLAYER2_PARAM]
    print(f'getting {player1ID} -> {player2ID} info') 
    if player1ID == player2ID:
        path_str = draw_same_person_path()
        return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)
    path = determine_degrees(player1ID, player2ID)
    path_str = draw_path(path, player2ID)
    return render_template('index2.html/', title='6 Degrees of Jamie Moyer', general_image_dir=general_image_dir, player_cache=player_cache, people=['n/a'], path_str=path_str)

print('not closing the bitch here')
#neo4J_session.close()

