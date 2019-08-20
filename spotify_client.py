import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyClient:
	def __init__(self, user=""):
		self.user = user
		client_credentials_manager = SpotifyClientCredentials()
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		self.sp = sp
	
	def setUser(user):
		self.user = user
	
	def getPlaylists(self):
		playlist_ids = {}
		playlists = self.sp.user_playlists(self.user)
		playlists = json.dumps(playlists, indent = 4)
		playlists = json.loads(playlists)		

		# Unpack playlists json into a dictionary with "name: id"
		for playlist in playlists['items']:
			playlist_ids[playlist['name'].encode('ascii', 'ignore')] = playlist['id'].encode('ascii', 'ignore')
		
		return playlist_ids 

	# getTracksFromPlaylist
	# Input: playlist name as string
	# Output: Dictionary in form of "artist track_name: duration_ms"
	def getTracksFromPlaylist(self, playlist_name):
		playlists = self.getPlaylists()
		playlist_ID = playlists[playlist_name]
		tracks = self.sp.user_playlist_tracks(self.user, playlist_id = playlist_ID, fields = None, limit = 100, offset = 0, market = None)
		tracks = json.dumps(tracks,indent = 4)
		tracks = json.loads(tracks)
		tracklist = {}
		for item in tracks['items']:
			track_object = item['track']
			track_name = track_object['name'].encode('ascii', 'ignore')
			track_duration = track_object['duration_ms']
			artist_object = track_object['artists']
			primary_artist = artist_object[0]
			artist_name = primary_artist['name'].encode('ascii', 'ignore')
			search_string = str(artist_name + " " + track_name)
			tracklist[search_string] = track_duration

		return tracklist
	

