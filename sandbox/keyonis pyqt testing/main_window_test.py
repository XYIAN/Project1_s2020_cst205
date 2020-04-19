#Main Window after login
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeyEvent 
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Daily Playlist")
		self.setGeometry(800, 400, 200, 300)
		layout = QGridLayout()

		title_label = QLabel("Daily Playlist")
		title_label.setFont(QFont("Times", 18, QFont.Black))
		layout.addWidget(title_label,0,1,1,2)

		self.playlist_button = QPushButton("Check New Videos!")
		#add event handler
		layout.addWidget(self.playlist_button,1,1,1,2)

		self.settings_button =  QPushButton("Settings")
		#add event handler
		layout.addWidget(self.settings_button,2,1,1,2)

		self.setLayout(layout)
