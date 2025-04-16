"""main"""

import os
import creds

from flask import Flask, session, redirect, url_for, request, render_template

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from word_manipulation import return_closest, merge_filler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

redirect_uri = 'http://127.0.0.1:5000/callback'
scope = 'playlist-modify-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=creds.client_id,
    client_secret=creds.client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)


@app.route('/')
@app.route('/home')
def home():
    """check if user is logged in"""
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('webpage'))


@app.route('/callback')
def callback():
    """callback"""
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('home'))


@app.route('/webpage', methods=['POST', 'GET'])
def webpage():
    """get input sentence"""
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        create_playlist(sentence)
    return render_template('webpage.html')


@app.route('/logout')
def logout():
    """logout"""
    session.clear()
    return redirect(url_for('home'))


def create_playlist(sentence: str):
    """create playlist"""
    user = sp.current_user()
    user_id = user['id']
    playlist = sp.user_playlist_create(
        user=f'{user_id}',
        name=sentence,
        public=False,
        collaborative=False,
        description=f'We tried to build the sentence: {sentence}'
    )
    playlist_id = playlist['id']
    sentence_split = sentence.split()

    sentence_split = merge_filler(sentence_split)
    song_ids = search_spotify(sentence_split)

    sp.playlist_add_items(playlist_id, song_ids)


def search_spotify(queries: list[str]) -> list[str]:
    """search words get songs"""
    uris = []
    for item in queries:
        song = sp.search(
            q=item,
            type='track',
            limit=50
        )

        track_names = [song['tracks']['items'][i]['name'].upper() for i in range(len(song['tracks']['items']))]
        index = return_closest(item.upper(), track_names)

        track_uri = song['tracks']['items'][index]['uri']
        uris.append(track_uri)
    return uris


if __name__ == '__main__':
    app.run(debug=True)
