from flask import Flask, request, redirect, session, url_for, jsonify, render_template
from concurrent.futures import ThreadPoolExecutor
from helpers import all_helpers
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API credentials
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:8000/callback"

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_ARTISTS_ALBUMS_URL = "https://api.spotify.com/v1/artists/{artist_id}/albums"

SCOPES = "user-follow-read user-read-private user-read-email"

@app.route("/")
def home():
    return render_template("landing_page.html")

@app.route("/login")
def login():
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code provided.", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        return f"Error: {response.json()}", 400

    tokens = response.json()
    session["access_token"] = tokens["access_token"]

    return redirect(url_for("list_artists"))

@app.route("/list_artists")
def list_artists():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.spotify.com/v1/me/following?type=artist&limit=50"
    artists = all_helpers.paginate_requests(url, headers, {}, ["artists","items"], "next")
    
    return render_template("list_artists.html", artists=artists)

@app.route("/select_artists", methods=["POST"])
def select_artists():
    selected_artists = request.form.getlist("artists")
    session["selected_artists"] = selected_artists  
    return redirect(url_for("latest_releases"))


def fetch_albums(artist_id, headers):
    url = SPOTIFY_ARTISTS_ALBUMS_URL.format(artist_id=artist_id)
    params = {"include_groups": "album,single", "limit": 50, "offset": 0}
    return all_helpers.paginate_requests(url, headers, params, ["items"], "next")

@app.route("/latest_releases")
def latest_releases():
    access_token = session.get("access_token")
    selected_artists = session.get("selected_artists")

    if not access_token or not selected_artists:
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {access_token}"}
    releases = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_albums, artist_id, headers): artist_id for artist_id in selected_artists}

        for future in futures:
            try:
                albums = future.result()
                for album in albums:
                    release_date = album["release_date"]
                    release_date_precision = album["release_date_precision"]

                    if release_date_precision == "day":
                        album_date = datetime.strptime(release_date, "%Y-%m-%d")
                    elif release_date_precision == "month":
                        album_date = datetime.strptime(release_date, "%Y-%m")
                    else:
                        continue

                    if album_date >= datetime.now() - timedelta(days=60):
                        releases.append({
                            "name": album["name"],
                            "artist": ", ".join([artist["name"] for artist in album["artists"]]),
                            "type": album["album_type"],
                            "release_date": release_date,
                            "id": album["id"],
                        })
            except Exception as e:
                artist_id = futures[future]
                print(f"Error fetching albums for artist {artist_id}: {e}")

    grouped_releases = {"single": [], "album": []}
    for release in sorted(releases, key=lambda x: x["release_date"], reverse=True):
        grouped_releases[release["type"]].append(release)

    return render_template("latest_releases.html", releases=grouped_releases)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
