import requests, json, spotipy, statistics as s
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask

CLIENT_ID=""
CLIENT_SECRET=""

token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
accessToken = token.get_access_token()
clientCredentialsManager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)
cache_token: object = token.get_access_token()

"""
print(token)
print(accessToken)
print(clientCredentialsManager)
print(sp)
print(cache_token)
"""

def getURI():
    URI = sp.audio_features(input('\nCopy the Spotify URI of your song and paste it here: '))
    return URI

inData = getURI()

# write to JSON file
def writeToJSONFile(path, fileName, inData):
    filePathNameWExt = './' + path + '/' + fileName +'.json'
    with open (filePathNameWExt, 'w') as fp:
        json.dump(inData, fp, indent = 4)

path = './'
fileName = 'songData'
data = inData

writeToJSONFile(path, fileName, data)

with open("songData.json") as read_file:
    dictData = json.load(read_file)[0]

print(dictData)

songKey = dictData['key']
songValence = dictData['valence']
songTempo = dictData['tempo']
songTimeSignature = dictData['time_signature']
songMode = dictData['mode']

if songMode == 0:
    songMode = 'Minor'
else:
    songMode = 'Major'

def matchSongKey():
    #the most frequently add music was #this scale#:
    songKeyShaper = {
        'C': 0,
        'C# / Db': 1,
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
        if match == songKey: print("\nThe key of the song that you entered is:", key, songMode)

matchSongKey()

def outputDetails():
    print("\nThe tempo is: {:0.0f}".format(songTempo),
        "BPM, and the time signature is:",
        songTimeSignature, "/ 4")

outputDetails()

input("\nPress Enter to exit")