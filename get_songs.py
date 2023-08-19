import requests
import csv
import sys
from datetime import datetime

api_key = "cc7d8adb7f3edc14567397edda3ddc97"
mode = "dev"
keyword = "car"


def search_songs_by_keyword():
    base_url = "http://api.musixmatch.com/ws/1.1/"
    search_url = base_url + "track.search"

    page = 1
    all_tracks = []

    while True:
        params = {
            "apikey": api_key,
            "q_lyrics": keyword,
            "f_has_lyrics": 1,
            "page_size": 1 if mode == "dev" else 100,
            "f_track_release_group_first_release_date_max": "20100101",
            "page": page,
            "s_track_rating": "desc"  # Sort by track rating in descending order
        }

        response = requests.get(search_url, params=params)
        data = response.json()

        track_list = data \
            .get("message", {}) \
            .get("body", {}) \
            .get("track_list", [])

        if not track_list:
            break

        all_tracks.extend(track_list)
        page += 1

        if mode == "dev" and len(all_tracks) > 1:
            break

    return all_tracks


def get_album_release_date(album_id):
    base_url = "http://api.musixmatch.com/ws/1.1/"
    track_info_url = base_url + "album.get"

    params = {
        "apikey": api_key,
        "album_id": album_id
    }

    response = requests.get(track_info_url, params=params)
    data = response.json()

    album_release_date = data.get("message", {}).get("body", {}).get("album", {}).get("album_release_date", None)
    return album_release_date


def get_songs():
    tracks = search_songs_by_keyword()

    if not tracks:
        print("No tracks found with the given keyword.")
        return

    filtered_tracks = []

    for track in tracks:
        try:
            album_id = track["track"]["album_id"]
        except KeyError:
            continue
        album_release_date = get_album_release_date(album_id)

        if album_release_date:
            release_date = datetime.strptime(album_release_date, "%Y-%m-%d")
            if release_date < datetime(2010, 1, 1):
                filtered_tracks.append(track)

    if not filtered_tracks:
        print("No tracks found with the given keyword released before 1/1/2010.")

    return filtered_tracks


def create_csv(tracks):
    with open(f"{keyword}_songs.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["song Name", "performer Name", "album Name", "song share URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for track in tracks:
            track_info = track["track"]
            writer.writerow({
                "song Name": track_info["track_name"],
                "performer Name": track_info["artist_name"],
                "album Name": track_info["album_name"],
                "song share URL": track_info["track_share_url"]
            })


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]

        if len(sys.argv) >= 3 and any(sys.argv[2] in x for x in ["dev", "prod"]):
            mode = sys.argv[2]

    songs = get_songs()
    create_csv(songs)
