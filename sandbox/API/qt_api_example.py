
#PYQT and API interating with each other.
#After running and getting authcode, Pick Favorites, then Check for new videos
#Currently the check for new videos just pulls the latest 2 from the channel, can make day based later
#Playlist maker currently not working
#Also Want to make so you don't have to auth each time.
#API 
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
#PYQT
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeyEvent 
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from settings import SettingsWindow

#API - Make into a class... somehow
scopes = ["https://www.googleapis.com/auth/youtube.readonly",	"https://www.googleapis.com/auth/youtube"]

def auth():
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

	api_service_name = "youtube"
	api_version = "v3"
	client_secrets_file = "client_secret_01.json" #ADD OWN JSON FILE HERE

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
			#video_title.append(videos['snippet']['title']) #Keep in case want to get title of each video for GUI #also has keyerror that needs to be fix
	
			video_id.append(videos['id']['videoId'])
		#video_info = dict(zip(video_title,video_id))
	return video_id

# works up until here

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

######################################
#pyqt
# Not Sure how to get fav list info between classes without making it a global so...
# A list of stings with the title of the youtube channgles to be check.
fav_subs = []


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

		self.setLayout(layout)
		self.main_window_list = list()

	@pyqtSlot()
	def fav_window(self):
		fav_window = FavoriteWindow(self.youtube_info)
		self.main_window_list.append(fav_window)

	@pyqtSlot()
	def playlist_add(self):
		self.all_subs = get_subs(self.youtube_info)
		print(self.all_subs)
		print(fav_subs)
		self.fav_current = {key:value for key,value in self.all_subs.items() if key in fav_subs}
		self.video_list = find_videos(self.fav_current)
		print(self.video_list)
		msg = QMessageBox()
		msg.setText("Video's added " + str(self.video_list))
		msg.exec_()





class FavoriteWindow(QWidget):
	def __init__(self,youtube_info):
		super().__init__()
		
		self.youtube_info = youtube_info
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
			self.list.addItem(title)

	#Updates Favorite Subscriptions List
	@pyqtSlot()
	def save_list(self):
		global fav_subs
		fav_subs = []
		for index in range(len(self.list)):
			if self.list.item(index).checkState() == Qt.Checked:
				fav_subs.append(self.list.item(index).text())
		self.close()

	
if __name__ == "__main__":
	youtube = auth()
	

	sub_list = get_subs(youtube)

	app = QApplication(sys.argv)
	my_window = MainWindow(youtube)
	my_window.show()

	# print(str(sub_list))
	# video_list = find_videos(sub_list)
	# print(video_list)
	#create_playlist(youtube)
	sys.exit(app.exec_())