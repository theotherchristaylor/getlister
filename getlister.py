from youtube_videos import youtube_search
from youtube_videos import geo_query
import json
import sys
from spotify_client import SpotifyClient
import pafy
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'

    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getYoutubeLink(search_term):
	search_results_raw = youtube_search(search_term)
	search_results_raw = json.dumps(search_results_raw, indent = 4)
	search_results_raw = json.loads(search_results_raw)
	search_results_raw = search_results_raw[1]

	for video in search_results_raw:
		video_title = video['snippet']['title']
		video_id = video['id']['videoId']
		url = "http://www.youtube.com/watch?v=" + video_id
		video = pafy.new(url)
		youtube_length = int(video.length)
		spotify_length = int(track_list[search_term]) / 1000
		difference = abs(youtube_length - spotify_length)
		if(difference < 3): #if the difference is within 3 seconds
			return url
	return ""

#----------------------------------------------------------------------------
# Present list of playlists for given user, have user choose which playlist
# to download.
#----------------------------------------------------------------------------
user = raw_input("Enter spotify username: ")
MAX_TRACKS = 50
sp = SpotifyClient(user)
playlists = sp.getPlaylists()
print "\n\rPlaylists for " + user + ":"
for i, item in enumerate(playlists, 1):
	print str(i) + ": " + item
enum_playlists = list(enumerate(playlists))
index = raw_input("Enter number of playlist to download: ")
chosen = enum_playlists[int(index) - 1][1]
print "\n\r[*] Preparing to download tracks of " + chosen

#----------------------------------------------------------------------------
# Download tracklist (search terms) for chosen playlist
#----------------------------------------------------------------------------

track_list = sp.getTracksFromPlaylist(chosen)

#----------------------------------------------------------------------------
# Search youtube for each track, and find video that is close to the same 
# length as the duration from Spotify. Add link to that track to list
#----------------------------------------------------------------------------
search_terms = []
for search_term in track_list:
	search_terms.append(search_term)
last_index = len(search_terms)
if last_index > MAX_TRACKS:
	last_index = MAX_TRACKS
download_links = []
for term in search_terms[0:last_index]:
	print "[*] Searching for " + term
	link = ""
	link = getYoutubeLink(term)
	if link is not "":
		print bcolors.OKGREEN + "[+] Found link for " + term + bcolors.ENDC
		download_links.append(link)
	else:
		print bcolors.FAIL + "[-] Could not find link for " + term + bcolors.ENDC

#----------------------------------------------------------------------------
# Create a folder with the same name of the playlist. Download each track
# on the links list, then place all .mp3 files into folder
#----------------------------------------------------------------------------

command = 'mkdir "' + chosen + '"'
os.system(command)
command = 'cd "' + str(chosen) + '"'
os.system(command)
for i, link in enumerate(download_links, 1):
	print bcolors.OKGREEN + "[+] Downloading track " + str(i) + " of " + str(len(download_links)) + bcolors.ENDC
	command = "youtube-dl -i --extract-audio --audio-format mp3 -o '%(title)s.%(ext)s' --audio-quality 0 " + link 
	os.system(command) 

command = 'mv *.mp3 "' + str(chosen) + '"'
os.system(command) 
