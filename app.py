import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
# Spotify API credentials
CLIENT_ID = '081cd4ac8df64a62b8a02257115a78a6'
CLIENT_SECRET = 'ce37b10a077348319b21f33cebcda13b'
REDIRECT_URI = 'https://localhost:3000/callback'
# Scopes to request (including playlist-modify-private)
SCOPE = 'playlist-modify-private'
# Function to scrape JioSaavn playlist and extract song details
def scrape_jiosaavn_playlist(playlist_url):
    song_details = []
    response = requests.get(playlist_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tracks = soup.find_all('figure', class_='o-flag o-flag--stretch o-flag--mini')
        #print(tracks)
        for track in tracks:
            a_tag = track.find('a')
             # Extract the title attribute
            title = a_tag['title']
            song_details.append(title)
            print(title)
            
       # print("song details")
       # print(song_details)
    return song_details

# Function to create a new Spotify playlist
def create_spotify_playlist(playlist_name):
     sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
     user_id = sp_oauth.me()['id']
     playlist = sp_oauth.user_playlist_create(user_id, playlist_name, public=False)
     return playlist['id']

# Function to search and add songs to Spotify playlist
def add_songs_to_spotify_playlist(playlist_id, song_details):
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    for song in song_details:
        result = sp_oauth.search(q=f"track:{song}", type='track', limit=1)
        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['uri']
            sp_oauth.playlist_add_items(playlist_id, [track_uri])

def getAccesToken(playlist_name):
     # Create a SpotifyOAuth object with the desired scopes
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)

    # Get authorization URL
    auth_url = sp_oauth.get_authorize_url()

    print("Please visit this URL to authorize your app:", auth_url)

    # After the user authorizes the app, get the authorization code from the redirect URI
    authorization_code = input("Enter the authorization code from the URL: ")

    # Exchange the authorization code for access and refresh tokens
    token_info = sp_oauth.get_access_token(authorization_code)
    print(token_info)
    # Use the access token to make authenticated requests to the Spotify API
    if token_info:
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        
        # Get current user's information
        user_info = sp.current_user()
        user_id = user_info['id']
        print(user_id)
        # Example: create a private playlist
        
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        print(f"Private playlist '{playlist_name}' created successfully!")
    else:
        print("Failed to obtain access token.")

    return playlist['id']


# Main function
def main():
    # JioSaavn playlist URL
    jiosaavn_playlist_url = 'https://www.jiosaavn.com/s/playlist/405c238058e239184ceae33f78a8c024/%F0%9F%92%9D%F0%9F%92%9D/ZPxKZ38G7O1ieSJqt9HmOQ__'
    
    # Scrape JioSaavn playlist
    song_details = scrape_jiosaavn_playlist(jiosaavn_playlist_url)
   
    # Create a new Spotify playlist
   # playlist_name = input("What Playlist name you want?")
   
   # playlist_id = create_spotify_playlist(playlist_name)
    
    # Add songs to Spotify playlist
   # add_songs_to_spotify_playlist(playlist_id, song_details)
    
    print("Playlist created and songs added successfully!")

if __name__ == "__main__":
    main()
