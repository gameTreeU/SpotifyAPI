import requests
import json
import spotipy
import statistics as s
import math
from spotipy.oauth2 import SpotifyClientCredentials
#from convertToJSON import convert

CLIENT_ID=""
CLIENT_SECRET=""
#hey
"""
Using spotipy, another API, we can authenticate Spotify accounts using Oauth2

Set a variable, token, = the spotipy.oauth2.SpotifyClientCredentials request
print(token) to make sure we're finding it

Set a variable, cache_token = token.get_access_token()
This returns the string form of the previous class we were looking at

cache_token: object = token.get_access_token()
^^^ This creates an object of the access token ^^^
print(cache_token) to make sure we're finding it
"""

token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
accessToken = token.get_access_token()
clientCredentialsManager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)
cache_token: object = token.get_access_token()

print(token)
print(accessToken)
print(clientCredentialsManager)
print(sp)
print(cache_token)

"""
This module will get playlist tracks and track features
The data is organized in a dictionary 
"""
indata = sp.playlist_tracks("6sMmJun3rrgXQwKJnsoNPO?si=xAwrEBknQR6gnC1CdOZoZg")
#get playlist tracks and track data
def getPlaylistData():
    jsonDict = {}

    headers = {'Authorization': "Bearer " + accessToken}
    for track in indata['tracks']['items']:
        songId = track['track']['id']
        url = "https://api.spotify.com/v1/audio-features/" + songId
        response = requests.get(url, headers=headers)
        jsonDict[track['track']['name']] = json.loads(response.text)
    return jsonDict

#return the songs and song features for the playlist
out = getPlaylistData()
#print(out)



# write to JSON file
def writeToJSONFile(path, fileName, indata):
    filePathNameWExt = './' + path + '/' + fileName +'.json'
    with open (filePathNameWExt, 'w') as fp:
        json.dump(indata, fp, indent = 4)

path = './'
fileName = 'playlistData'
data = out

writeToJSONFile(path, fileName, data)
'''
def get_energy():
    temp = data['Ghost Safari']
    for question_data in temp:
        replies_access = question_data['items']
        for replies_data in replies_access:
            energy = replies_data['track']['energy']
            save_energy.append(energy)

save_energy = []
get_energy()
save_energy
'''


#Creates a list with all energy values from a playlist and averages them with statistics.mean()

def getAvgPlaylistData():
    energy = round(s.mean([data[track]['energy'] for track in data]), 3)
    valence = round(s.mean([data[track]['valence'] for track in data]), 3)
    tempo = round(s.mean([data[track]['tempo'] for track in data]), 3)
    loudness = round(s.mean([data[track]['loudness'] for track in data]), 3)
    print("Average energy is: ", energy)
    print("Average valence is: ", valence)
    print("Average tempo is: ", tempo)
    print("Average loudness is: ", loudness)
getAvgPlaylistData()
songKey = s.mode([data[track]['key'] for track in data])

def matchSongKey():
    #the most frequently add music was #this scale#:
    songKeyShaper = {
        'C': 0,
        'C#': 1,
        'D': 2,
        'D# / Eb': 3,
        'E': 4,
        'F': 5,
        'F# / Gb': 6,
        'G': 7,
        'G#': 8,
        'A': 9,
        'A# / Bb': 10,
        'B': 11}

    for key, match in songKeyShaper.items():
        if match == songKey: print("The key is: ", key)

#matchSongKey()

songKeyColor = {
          0: '#f00',
          1: '#90f',
          2: '#ff0',
          3: '#c49',
          4: '#cff',
          5: '#b03',
          6: '#89f',
          7: '#f80',
          8: '#c7f',
          9: '#3d3',
         10: '#b68',
         11: '#9df'}



#print(energy, valence, tempo, loudness, key)
