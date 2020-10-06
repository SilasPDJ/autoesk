import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from PyQt5 import QtWidgets, QtGui, QtCore


class SeleniumManager(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):
        self.started.emit()

        link = "../Chromedriver/chromedriver.exe"
        browser = webdriver.Chrome(link)
        browser.get("https://twitter.com/login")
        time.sleep(1)
        # do more stuff in project instead i add more url
        browser.get("https://twitter.com/explore")
        time.sleep(1)
        browser.get("https://twitter.com/login")
        time.sleep(1)
        browser.close()
        time.sleep(1)
        self.finished.emit()


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint
        )

        self.label_animation = QtWidgets.QLabel(self)
        self.movie = QtGui.QMovie("loading.gif")
        self.label_animation.setMovie(self.movie)

    def startAnimation(self):
        self.movie.start()
        self.show()
        QtCore.QTimer.singleShot(2 * 1000, self.stopAnimation)

    def stopAnimation(self):
        self.movie.stop()
        self.hide()


class Demo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Overlay with Selenium Problem")
        self.resize(500, 500)
        self.center()
        self.twitter_icon = QtWidgets.QLabel("")
        self.twitter_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = QtGui.QPixmap("twitter.png")
        self.pixmap = self.pixmap.scaled(
            64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        self.twitter_icon.setPixmap(self.pixmap)
        self.twt_btn = QtWidgets.QPushButton("Twitter")

        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addStretch()
        v_box.addWidget(self.twitter_icon)
        v_box.addWidget(self.twt_btn)
        v_box.addStretch()

        self.loading = LoadingScreen()
        self._manager = SeleniumManager()

        self._manager.started.connect(self.loading.startAnimation)
        self._manager.finished.connect(self.loading.stopAnimation)
        self.twt_btn.clicked.connect(self._manager.start)
        self._manager.started.connect(self.hide)
        self._manager.finished.connect(self.show)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    dm = Demo()
    dm.show()
    app.exit((app.exec_()))