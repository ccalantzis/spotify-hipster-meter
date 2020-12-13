import requests
import json
from flask import Flask, render_template, request
from flask_request_params import bind_request_params

app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.before_request(bind_request_params)

@app.route("/",  methods=['GET'])
def login():
    return render_template('index.html', result='hipster')

@app.route('/redirect', methods=['GET'])
def redirect():
    return render_template('redirect.html')

@app.route("/results",  methods=['GET'])
def results():
    token = request.args.get('access_token')

    headers = {'Authorization': 'Bearer ' + str(token)}
    req = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)

    if not req.status_code == 200:
        return 'Failed to retrieve information'

    all_data = json.loads(req.content)
    num_tracks = len(all_data['items'])

    popularity_sum = 0
    for i in range(num_tracks):
        popularity_sum += all_data['items'][i]['popularity']

    popularity_score = popularity_sum/(100*num_tracks)
    hipster = ""
    if popularity_score < 0.25:
        hipster = "Maximum hipster"
    elif popularity_score < 0.5:
        hipster = "Up and coming hipster"
    elif popularity_score < 0.75:
        hipster = "Hip, but not hipster"
    else:
        hipster = "You're on the mainstream side"

    tracks = []
    for i in range(num_tracks):
        tracks.append([all_data['items'][i]['name'], all_data['items'][i]['artists'][0]['name'], 
            all_data['items'][i]['album']['images'][0]['url'], all_data['items'][i]['popularity']])
    tracks = sorted(tracks, key=lambda x: x[3])
    hipster_track_name = tracks[0][0]
    hipster_artist_name = tracks[0][1]
    hipster_art_url = tracks[0][2]
    mainstream_track_name = tracks[-1][0]
    mainstream_artist_name = tracks[-1][1]
    mainstream_art_url = tracks[-1][2]


    results = {"hipster" : hipster, "hipster_art_url" : hipster_art_url, "hipster_track_name" : hipster_track_name, 
    "hipster_artist_name" : hipster_artist_name, "mainstream_art_url" : mainstream_art_url, 
    "mainstream_track_name" : mainstream_track_name, "mainstream_artist_name" : mainstream_artist_name}

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run()