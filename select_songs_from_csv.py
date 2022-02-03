import pandas
import os


def select(csv_path, valence_range, instrumentalness_range, speechiness_range, tempo_range):
    df = pandas.read_csv(csv_path)
    selected_songs = pandas.DataFrame(
        {
            "index": [], "Speechiness": [], "Valence": [], "Instrumentalness": [],
            "Tempo": [], "Song": [], "Artist": []
        }
    )
    for index, row in df.iterrows():
        valence = row["Valence"]
        instrumentalness = row["Instrumentalness"]
        speechiness = row["Speechiness"]
        tempo = row["Tempo"]
        song = row["Song"]
        artist = row["Artist"]
        if valence_range[0] <= valence and valence <= valence_range[1]:
            if instrumentalness_range[0] <= instrumentalness and instrumentalness <= instrumentalness_range[1]:
                if speechiness_range[0] <= speechiness and speechiness <= speechiness_range[1]:
                    if tempo_range[0] <= tempo and tempo <= tempo_range[1]:
                        selected_songs = selected_songs.append(
                            {
                                "index": index+1, "Tempo": tempo, "Instrumentalness": instrumentalness,
                                "Song": song, "Artist": artist, "Speechiness": speechiness, "Valence": valence
                            }, ignore_index=True
                        )

    return selected_songs


DIR = r"C:\Users\Max\OneDrive\Documenten\Sound and Music Technology\Project\playlists"
valence_range = [0.7, 1.0]
instrumentalness_range = [0.85, 1.0]
speechiness_range = [0, 0.1]
tempo_range = [105, 135]
songs = pandas.DataFrame(
    {
        "index": [], "Speechiness": [], "Valence": [], "Instrumentalness": [],
        "Tempo": [], "Song": [], "Artist": [], "Playlist": []
    }
)
for f in os.listdir(DIR):
    csv_path = os.path.join(DIR, f)
    if not os.path.isfile(csv_path):
        continue
    _songs = select(csv_path, valence_range, instrumentalness_range, speechiness_range, tempo_range)
    playlistname_column = [f.replace(".csv", "") for _ in _songs.iterrows()]
    _songs["Playlist"] = playlistname_column
    songs = songs.append(_songs)

songs.to_csv(os.path.join(DIR, "result", "Valence_playlist-v03.csv"))

