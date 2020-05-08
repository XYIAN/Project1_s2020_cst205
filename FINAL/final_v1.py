

# After running and getting authcode, Pick Favorites, then Check for new videos
# Currently the check for new videos just pulls the latest 2 from the channel
# Clear data before pushing updates

# TO DO:
# -- Clean up code / More OOP
# -- Make so you don't have to auth each time.
# -- Maybe add more custom features


#API 
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from apiclient.discovery import build
#PYQT
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

#Other
from datetime import date, datetime,timezone
import json
#API - Make into a class... somehow
scopes = ["https://www.googleapis.com/auth/youtube.readonly",	"https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtube.force-ssl"]

def loginSave():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    client_config={
            "installed":{
                "auth_uri" : "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "client_id": "282059832027-l4lvaddcl0mtgka3hook75rfea87035u.apps.googleusercontent.com",
                "project_id":"api-access-275200",
                "client_secret":"Gk05LhRZNVlZH-WXVCuZfme-"
                }
            }
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_console(); 

    drive = build('drive','v3',credentials=credentials)
    resp = drive.files().list().execute()
    access_token=credentials.token
    refresh_token=credentials.refresh_token
    print(resp)
#Auth method adapted from Youtube API example
def auth():
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

	api_service_name = "youtube"
	api_version = "v3"
	client_secrets_file = "KyleID.json" #ADD OWN JSON SECRETS FILE HERE

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
		maxResults=50,
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
	today_date = date.today()
	today_date = today_date.strftime('%Y-%m-%d')

	for channels in favorites.values():
		request = youtube.search().list(
			part='id',
			channelId=channels,
			maxResults=20,
			publishedAfter= today_date+"T00:00:00Z",
			order="date",
			type="video"
		)
		response = request.execute()
		# print(response)
		
		for videos in response['items']:
			#video_title.append(videos['snippet']['title']) #Keep in case want to get title of each video for GUI #also has keyerror that needs to be fix
	
			video_id.append(videos['id']['videoId'])
		#video_info = dict(zip(video_title,video_id))
	return video_id



def create_playlist(youtube): #change title of playlist to date
	today = date.today()

	request = youtube.playlists().insert(
		part="snippet,status",
		body={
			"snippet": {
				"title": today.strftime("%m/%d/%y") + " Playlist",
				"description": "A playlist for " + today.strftime("%m/%d/%y"),
		  },
		  "status":{
				"privacyStatus":"private"
		  }	
		}
	)
	playlist_info = request.execute()
	
	return playlist_info['id']

def add_videos_to_playlist(youtube,video_ids,playlist_id):
	
	for video in video_ids:
		request = youtube.playlistItems().insert(
			part="snippet",
			body={
			  "snippet": {
				"playlistId": playlist_id,
				"resourceId": {
				  "kind": "youtube#video",
				  "videoId": video
				}
			  }
			}
		)
		response = request.execute()

def load_user_data():
		with open('user_data.json') as f:
			return json.load(f)

def save_user_data(data):
		with open('user_data.json', 'w') as f:
			json.dump(data, f)

######################################
#pyqt

class MainWindow(QWidget):

	''' Creates a Main Window '''

	def __init__(self,youtube_info):
		super().__init__()
		# MainWindow.all_subs = subscriptions
		# MainWindow.fav_subs = []
		self.youtube_info = youtube_info

		self.setWindowTitle("Daily Playlist")
		self.setGeometry(800, 400, 200, 300)

		layout = QGridLayout()

		title_label = QLabel("Daily Playlist")
		title_label.setFont(QFont("Times", 18, QFont.Black))
		layout.addWidget(title_label,0,1,1,2)

		self.playlist_button = QPushButton("Check New Videos!")
		self.playlist_button.clicked.connect(self.playlist_add)
		layout.addWidget(self.playlist_button,1,1,1,2)

		self.sub_list_button = QPushButton("Pick Favorites!")
		self.sub_list_button.clicked.connect(self.fav_window)
		layout.addWidget(self.sub_list_button,2,1,1,2)

		self.clear_button = QPushButton("Clear Data!")
		self.sub_list_button.clicked.connect(self.clear_data)
		layout.addWidget(self.clear_button,3,1,1,2)

		self.setLayout(layout)
		self.main_window_list = list()

	@pyqtSlot()
	def clear_data(self):
		self.user_data = load_user_data()
		self.user_data["fav_subs"] = []
		self.user_data["today_playlist"] = ""
		self.user_data["today_videos"] = []
		save_user_data(self.user_data)


	@pyqtSlot()
	def fav_window(self):
		fav_window = FavoriteWindow(self.youtube_info)
		self.main_window_list.append(fav_window)

	@pyqtSlot()
	def playlist_add(self):
		self.all_subs = get_subs(self.youtube_info)
		self.user_data = load_user_data()
		#date check
		today = date.today()
		today_date = today.strftime("%m/%d/%y")

		#Creates a dict with channel name and channel id
		self.fav_current = {key:value for key,value in self.all_subs.items() if key in self.user_data["fav_subs"]}

		self.video_list = find_videos(self.fav_current)
		self.new_videos = list(set(self.video_list).difference(self.user_data["today_videos"]))

		
		if (self.user_data["today_playlist"] == "" or self.user_data["current_date"] != today_date ):
			self.user_data["today_playlist"] = create_playlist(self.youtube_info)
			self.user_data["current_date"] = today_date
		add_videos_to_playlist(self.youtube_info, self.new_videos, self.user_data["today_playlist"])

		# Updating user data
		self.user_data["today_videos"].extend(self.new_videos)
		save_user_data(self.user_data)

		msg = QMessageBox()
		msg.setText(str(len(self.new_videos)) + " Video(s) added to your playlist")
		msg.exec_()



class FavoriteWindow(QWidget):
	def __init__(self,youtube_info):
		super().__init__()
		
		self.youtube_info = youtube_info
		self.user_data = load_user_data()

		self.setWindowTitle("Daily Playlist")
		self.setGeometry(800, 600, 300, 400)
		layout = QGridLayout()
		vbox = QVBoxLayout()
		
		self.list = QListWidget()
		self.sub_list()        
		vbox.addWidget(self.list)

		self.save_button = QPushButton("Save Favorites")
		self.save_button.clicked.connect(self.save_list)
		vbox.addWidget(self.save_button)
		


		self.setLayout(vbox)
		self.show()

	# Added Full subscriptions to list
	def sub_list(self):
		self.all_sub = get_subs(self.youtube_info)
		for i in self.all_sub:
			title = QListWidgetItem(i)
			title.setFlags(title.flags() | Qt.ItemIsUserCheckable)
			title.setCheckState(Qt.Unchecked)
			for fav in self.user_data["fav_subs"]:
				if title.text() == fav:
					title.setCheckState(Qt.Checked)
			self.list.addItem(title)

	#Updates Favorite Subscriptions List
	@pyqtSlot()
	def save_list(self):
		self.user_data["fav_subs"] = []
		for index in range(len(self.list)):
			if self.list.item(index).checkState() == Qt.Checked:
				self.user_data["fav_subs"].append(self.list.item(index).text())
		save_user_data(self.user_data)
		self.close()


	
if __name__ == "__main__":

	youtube = auth()

	app = QApplication(sys.argv)
	my_window = MainWindow(youtube)

	my_window.show()
	sys.exit(app.exec_())
