import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeyEvent 
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from login_info import login_info
from main_window_test import MainWindow


class Login(QWidget):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle("Daily Playlist Login")
		self.setGeometry(300, 300, 300, 300)

		layout = QGridLayout()

		title_label = QLabel('Daily Playlist')
		title_label.setFont(QFont("Times", 18, QFont.Bold))
		title_label.setMargin(0)
		layout.addWidget(title_label,0,1,1,3)

		
		email_label = QLabel('Email')
		self.email_edit = QLineEdit()
		self.email_edit.setPlaceholderText('Enter Email...')
		layout.addWidget(email_label, 1, 0)
		layout.addWidget(self.email_edit, 1, 1)

		password_label = QLabel('Password')
		self.password_edit = QLineEdit()
		self.password_edit.setPlaceholderText('Enter Password...')
		layout.addWidget(password_label, 2, 0)
		layout.addWidget(self.password_edit, 2, 1)

		login_button = QPushButton('Login')
		#add clicked event
		login_button.clicked.connect(self.login_check)
		layout.addWidget(login_button,3,0,1,2)
		layout.setVerticalSpacing(1)
		layout.setRowMinimumHeight(2,75)

		self.setLayout(layout)

		# Window Managment
		self.windows_list = list()


	def login_check(self):

		msg = QMessageBox()
		login_success = False

		for users in login_info:
			if users['email'] == self.email_edit.text().lower() and users['password'] == self.password_edit.text().lower():
				login_success = True
				msg.setText('Login Successful!\nOpening Application...')
				msg.exec_()
				self.open_main()

		if login_success == False: 
			msg.setText('Email/Password is incorrect')
			msg.exec_()


	def open_main(self):
		main_window = MainWindow()
		self.windows_list.append(main_window)
		main_window.show()


		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_window = Login()

	my_window.show()

	sys.exit(app.exec_())
