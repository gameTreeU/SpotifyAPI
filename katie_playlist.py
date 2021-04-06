import requests
import json
import spotipy
import statistics as s
import math
from spotipy.oauth2 import SpotifyClientCredentials
import keys as k

# Add your spotify developer client ID and client secret codes into these strings.
CLIENT_ID = k.ID
CLIENT_SECRET = k.SECRET

# Lines 10-14 connect to the API. Don't worry about understanding this.
token = spotipy.oauth2.SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
accessToken = token.get_access_token(as_dict=False)
clientCredentialsManager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)
cache_token: object = token.get_access_token(as_dict=False)

#Assigns literal song keys to the coordinated number signature returned from the dictionary.
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


# Create a function to gather the input of a spotify songs URI (Uniform Resource Identifier).
def getURI(entry):
    URI = sp.playlist_tracks(entry)
    return URI

#This function will get playlist tracks and track features
#The data is organized in a dictionary
def getPlaylistData(playlist):
    jsonDict = {}

    headers = {'Authorization': "Bearer " + accessToken}
    for track in playlist['items']:
        songId = track['track']['id']
        url = "https://api.spotify.com/v1/audio-features/" + songId
        response = requests.get(url, headers=headers)
        jsonDict[track['track']['name']] = json.loads(response.text)
    return jsonDict

# Create a function to write the inData to JSON file.
def writeToJSONFile(fileName, indata):
    filePathNameWExt = './' + fileName +'.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(indata, fp, indent=4)


# Create a function that will get playlist averages and print the output.
def getAvgPlaylistData(data):
    energy = round(s.mean([data[track]['energy'] for track in data]), 3)
    valence = round(s.mean([data[track]['valence'] for track in data]), 3)
    tempo = round(s.mean([data[track]['tempo'] for track in data]), 3)
    loudness = (round(s.mean([data[track]['loudness'] for track in data]), 3) * -1)
    danceability = round(s.mean([data[track]['danceability'] for track in data]), 3)

    #Find the song key that occurs the most frequently
    songKey = s.mode([data[track]['key'] for track in data])

    modality = (s.mode([data[track]['mode'] for track in data]), 3)
    if modality == 0:
        songMode = 'Minor'
    else:
        songMode = 'Major'

    for key, match in songKeyShaper.items():
        if match == songKey:
            songKey = key

    return energy, valence, tempo, loudness, danceability, songKey, songMode
    '''
    print('Average energy is:', energy)
    print('Average valence is:', valence)
    print('Average tempo is:', tempo)
    print('Average loudness is:', loudness)
    #Create a for loop that pairs song keys and song modes and prints a statement with your matched output.
    for key, match in songKeyShaper.items():
        if match == songKey: print("The most common key is:", key)
    print("The most common modality is:", songMode, '\n')


def run():
    print('\nAverage data for playlist 1:')
    getAvgPlaylistData(features1)
    print('Average data for playlist 2:')
    getAvgPlaylistData(features2)

    input('\nPress ENTER to quit')

if __name__ == "__main__":
    # Enter two playlists
    print('\nFIRST PLAYLST')
    playlist1 = getURI()
    print('\nSECOND PLAYLIST')
    playlist2 = getURI()

    # Return songs and features for the playlists
    features1 = getPlaylistData(playlist1)
    features2 = getPlaylistData(playlist2)

    # Name the output file
    path = './'
    file1 = input('\nFilename for playlist 1: ')
    file2 = input('\nFilename for playlist 2: \n')
    writeToJSONFile(path, file1, features1)
    writeToJSONFile(path, file2, features2)

    # Try to create a dictionary that will map song keys to HTML color codes.
    # Could be useful for data visualizations.
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
    '''