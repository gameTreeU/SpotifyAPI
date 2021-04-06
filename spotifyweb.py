from flask import Flask, redirect, url_for, render_template, request
import keys
import katie_playlist as kp
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import json
import chart_studio
import chart_studio.plotly as csp
import chart_studio.tools as cst
chart_studio.tools.set_credentials_file(username=keys.CHARTLYID, api_key=keys.CHARTLYSECRET)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        # Enter two playlists
        URI1 = request.form['playlist1']
        URI2 = request.form['playlist2']
        filename1 = request.form['file1']
        filename2 = request.form['file2']

        features_list1 = []
        features_list2 = []

        playlist1 = kp.getURI(URI1)
        playlist2 = kp.getURI(URI2)
        features1 = kp.getPlaylistData(playlist1)
        features2 = kp.getPlaylistData(playlist2)

        kp.writeToJSONFile(filename1, features1)
        kp.writeToJSONFile(filename2, features2)

        features_list1 = kp.getAvgPlaylistData(features1)
        energy = features_list1[0]
        valence = features_list1[1]
        tempo = features_list1[2]
        graph_tempo = tempo *.01
        loudness = features_list1[3]
        graph_loudness = loudness *.1
        danceability = features_list1[4]
        songKey = features_list1[5]
        songMode = features_list1[6]

        features_list2 = kp.getAvgPlaylistData(features2)
        energy2 = features_list2[0]
        valence2 = features_list2[1]
        tempo2 = features_list2[2]
        graph_tempo2 = tempo2 * .01
        loudness2 = features_list2[3]
        graph_loudness2 = loudness2 * .1
        danceability2 = features_list2[4]
        songKey2 = features_list2[5]
        songMode2 = features_list2[6]

       
        categories = ['Energy', 'Tempo', 'Valence', 'Loudness', 'Danceability']

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[energy, graph_tempo, valence, graph_loudness, danceability],
            theta=categories,
            fill='toself',
            name='Playlist A'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[energy2, graph_tempo2, valence2, graph_loudness2, danceability2],
            theta=categories,
            fill='toself',
            name='Playlist B'
        ))
        fig.update_traces(fill='toself', mode='markers', marker=dict(size=10, line=dict(color='DarkSlateGrey', width=.75)))
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 1.5]
            )),
        showlegend=True
        )
        csp.plot(fig, filename="Spotify Playlist Comparison", auto_open=False)



        '''df = pd.DataFrame(dict(
            Value=[energy, graph_tempo, valence, graph_loudness],
            Metric=['Energy','Tempo','Valence','Loudness']))
        fig = px.line_polar(df, r='Value', theta='Metric', line_close=True, range_r=[0,2], template="plotly_dark")

        fig.update_traces(fill='toself', mode='markers')
        fig.show()'''

    return render_template('index.html', energy=energy, valence=valence, tempo=tempo, loudness=loudness, songKey=songKey, songMode=songMode, danceability=danceability,
    energy2=energy2, valence2=valence2, tempo2=tempo2, loudness2=loudness2, songKey2=songKey2, songMode2=songMode2, danceability2=danceability2)
        

if __name__ == '__main__':
    app.debug=True
    app.run()