# Starts application?
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from login_window import Login
if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_window = Login()

	my_window.show()

	sys.exit(app.exec_())
