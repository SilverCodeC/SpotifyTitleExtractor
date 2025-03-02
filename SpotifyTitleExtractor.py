import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# Replace these with your actual Spotify Client ID and Client Secret
CLIENT_ID = ''
CLIENT_SECRET = ''

# Set up authorization to interact with the Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_playlist_id_from_url(url):
    """Extract the playlist ID from a Spotify playlist URL."""
    match = re.search(r'playlist/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        print("Invalid URL format. Make sure it is a Spotify playlist URL.")
        return None

def extract_playlist_tracks(playlist_id):
    """Fetch all tracks from the playlist by repeatedly making requests."""
    tracks = []
    offset = 0
    limit = 100  # Maximum number of tracks allowed per request
    
    while True:
        # Fetch the playlist tracks with pagination (100 tracks per request)
        results = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        
        # Add the tracks to the list
        for item in results['items']:
            track = item['track']
            track_name = track['name']
            track_artist = track['artists'][0]['name']  # Get the first artist name
            tracks.append(f"{track_name} by {track_artist}")
        
        # Check if there are more tracks to fetch
        if results['next']:  # If there's a 'next' page, continue fetching
            offset += limit  # Increment the offset by 100 (for the next page)
        else:
            break  # No more tracks, exit the loop

    return tracks

def save_tracks_to_file(tracks, filename="playlist_tracks.txt"):
    """Save the tracks to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for track in tracks:
            file.write(track + "\n")
    print(f"\nTracks have been saved to {filename}")

def main():
    # Ask the user for the Spotify playlist URL
    playlist_url = input("Please enter the Spotify playlist URL: ")
    
    # Extract the playlist ID from the URL
    playlist_id = extract_playlist_id_from_url(playlist_url)
    
    if playlist_id:
        # Get the tracks from the playlist
        tracks = extract_playlist_tracks(playlist_id)
        
        # Print the track list in order
        print("\nSongs in your playlist:")
        for idx, track in enumerate(tracks, start=1):
            print(f"{idx}. {track}")
        
        # Save the tracks to a text file in the current directory
        save_tracks_to_file(tracks)
    else:
        print("Could not extract a valid playlist ID from the URL.")

if __name__ == "__main__":
    main()
