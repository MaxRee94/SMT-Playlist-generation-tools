client_id = "033c3ebcc06047a4b3448d1d1023c46b"
client_secret = "1a5768ee12de4b2fb960a7147cdb8901"

import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

'''
This script gets a playlist URI (if you view a playlist in the web version of spotify like this
https://open.spotify.com/playlist/6yPiKpy7evrwvZodByKvM9 the part 6yPiKpy7evrwvZodByKvM9 is the URI)
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=76e896dae2b74941
and creates a csv file with the following format:
Song Name, Artist Name, Speechiness, Valence, Instrumentalness, Tempo
'''

playlist_uri = "4RART2hlJKhaKSmlUetv79"  # SPECIFY THE PLAYLIST URI HERE
csv_name = playlist_uri+".csv"

res = spotify.playlist_items(playlist_uri, limit=100)
ids = []
features = []
finaltracks = []
finalartists = []
cond = True

while cond:
    temp_feature = []
    ids = []
    tracks = res['items']

    for track in tracks:
        if track['track']['id'] is not None:
            finaltracks.append(track['track']['name'].replace(",", ""))
            finalartists.append(track['track']['artists'][0]['name'].replace(",", ""))
            ids.append(track['track']['id'])

    id_str = ','.join(ids)

    temp_f = spotify.audio_features(id_str)

    for feature in temp_f:
        temp_feature.append([feature['speechiness'],
                             feature['valence'],
                             feature['instrumentalness'],
                             feature['time_signature'],
                             feature['tempo']])

    features.extend(temp_feature)

    if res['next'] is None:
        cond = False
    else:
        res = spotify.next(res)

with open(csv_name, 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(["Speechiness", "Valence", "Instrumentalness", "Time Signature", "Tempo", "Song", "Artist"])

    for index, feature in enumerate(features):
        feature.append(finaltracks[index])
        feature.append(finalartists[index])

    for row in features:
        row = list(row)
        spamwriter.writerow(row)

print("Program completed")

