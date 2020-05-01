# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ["https://www.googleapis.com/auth/youtube.readonly",	"https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube1():
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	client_secrets_file = "client_secret_01.json"

	# Get credentials and create an API client
   
	flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
		client_secrets_file, scopes)
	credentials = flow.run_console()

	youtube = googleapiclient.discovery.build(
		api_service_name, api_version, credentials=credentials)
	return youtube
	
def get_subs(youtube):
	request = youtube.subscriptions().list(
		part="snippet,contentDetails",
		mine=True    
	)
	response = request.execute()

	# print(response['title'])
	sub_title = []
	sub_id = []
	for subs in response['items']:
		sub_title.append(subs['snippet']['title'])
		sub_id.append(subs['snippet']["resourceId"]['channelId'])
	sub_info = dict(zip(sub_title, sub_id))
	return sub_info

def find_videos(favorites):
	video_title = []
	video_id = []
	for channels in favorites.values():
		request = youtube.search().list(
			part='id',
			channelId=channels,
			maxResults=2,
        	order="date",
        	type="video"
		)
		response = request.execute()
		# print(response)
		
		for videos in response['items']:
			# video_title.append(videos['snippet']['title'])
			print("inloop")
			video_id.append(videos['id']['videoId'])
	return video_id

		

def create_playlist(youtube):
	request = youtube.playlists().insert(
		part="snippet",
		body={
			"kind": "youtube#playlist",
			"snippet": {
				"title": "Test Playlist 01"
		  }	
		}
	)
	response = request.execute()


if __name__ == "__main__":
	youtube = youtube1()
	sub_list = get_subs(youtube)
	print(str(sub_list))
	video_list = find_videos(sub_list)
	print(video_list)
	#create_playlist(youtube)