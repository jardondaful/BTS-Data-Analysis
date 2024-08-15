from flask import Flask, request, redirect, session, render_template
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Import the db object from db.py
from db import db
from models import Artist, Album, Track

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the db object with the Flask app
db.init_app(app)

# Spotify API credentials loaded from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'
SCOPE = 'user-top-read user-read-recently-played playlist-modify-private'

@app.route('/')
def index():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/season-summary")

@app.route('/season-summary')
def season_summary():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    # Fetch and store data
    fetch_and_store_artist_data('3Nrfpe0tUJi4K4DXYWgMUX')  # Example: BTS Artist ID
    fetch_and_store_album_data('3Nrfpe0tUJi4K4DXYWgMUX')
    
    # Query top artists from the database
    top_artists = Artist.query.order_by(Artist.popularity.desc()).limit(10).all()
    
    # Query top albums from the database
    top_albums = Album.query.order_by(Album.release_date.desc()).limit(10).all()
    
    # Pass this data to the template
    return render_template('index.html', top_artists=top_artists, top_albums=top_albums)

def fetch_and_store_artist_data(artist_id):
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    artist = sp.artist(artist_id)
    
    # Check if the artist already exists in the database
    existing_artist = Artist.query.get(artist['id'])
    if not existing_artist:
        new_artist = Artist(
            id=artist['id'],
            name=artist['name'],
            popularity=artist['popularity'],
            followers=artist['followers']['total'],
            genres=", ".join(artist['genres'])
        )
        db.session.add(new_artist)
        db.session.commit()

def fetch_and_store_album_data(artist_id):
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    albums = sp.artist_albums(artist_id)
    
    for album in albums['items']:
        existing_album = Album.query.get(album['id'])
        if not existing_album:
            new_album = Album(
                id=album['id'],
                artist_id=artist_id,
                name=album['name'],
                release_date=album['release_date']
            )
            db.session.add(new_album)
            db.session.commit()

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE)

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port=8000)
