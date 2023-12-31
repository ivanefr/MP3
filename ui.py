# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class MyListWidget(QtWidgets.QListWidget):
    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        QtWidgets.QListWidget.mousePressEvent(self, event)
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1321, 839)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background-color: #2F2F2F;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.next_song_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_song_button.setGeometry(QtCore.QRect(750, 690, 60, 60))
        self.next_song_button.setStyleSheet("border:0;")
        self.next_song_button.setText("")
        self.next_song_button.setObjectName("next_song_button")
        self.song_slider = QtWidgets.QSlider(self.centralwidget)
        self.song_slider.setGeometry(QtCore.QRect(130, 595, 1061, 22))
        self.song_slider.setMaximum(100)
        self.song_slider.setProperty("value", 0)
        self.song_slider.setTracking(True)
        self.song_slider.setOrientation(QtCore.Qt.Horizontal)
        self.song_slider.setInvertedAppearance(False)
        self.song_slider.setInvertedControls(False)
        self.song_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.song_slider.setObjectName("song_slider")
        self.current_time = QtWidgets.QLabel(self.centralwidget)
        self.current_time.setGeometry(QtCore.QRect(80, 590, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.current_time.setFont(font)
        self.current_time.setObjectName("current_time")
        self.cover = QtWidgets.QLabel(self.centralwidget)
        self.cover.setGeometry(QtCore.QRect(380, 50, 500, 500))
        self.cover.setText("")
        self.cover.setPixmap(QtGui.QPixmap("images/cover_image.png"))
        self.cover.setScaledContents(True)
        self.cover.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.cover.setObjectName("cover")
        self.list_of_songs = MyListWidget(self.centralwidget)
        self.list_of_songs.setGeometry(QtCore.QRect(915, 301, 371, 251))
        self.list_of_songs.setStyleSheet("")
        self.list_of_songs.setObjectName("list_of_songs")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 49, 331, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.name.setStyleSheet("border-style: solid;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(252, 252, 252);")
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.artist = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.artist.setStyleSheet("border-style: solid;\n"
                                  "border-width: 1px;\n"
                                  "border-color: rgb(252, 252, 252);")
        self.artist.setObjectName("artist")
        self.verticalLayout.addWidget(self.artist)
        self.date = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.date.setStyleSheet("border-style: solid;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(252, 252, 252);")
        self.date.setObjectName("date")
        self.verticalLayout.addWidget(self.date)
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setGeometry(QtCore.QRect(1005, 140, 191, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.load_button.setFont(font)
        self.load_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.load_button.setMouseTracking(False)
        self.load_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.load_button.setAutoFillBackground(False)
        self.load_button.setStyleSheet("background-color: rgb(76, 76, 77);\n"
                                       "color: rgb(214, 214, 214);\n"
                                       "border-radius: 30px;")
        self.load_button.setObjectName("load_button")
        self.length = QtWidgets.QLabel(self.centralwidget)
        self.length.setGeometry(QtCore.QRect(1202, 590, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.length.setFont(font)
        self.length.setObjectName("length")
        self.list_of_liked = MyListWidget(self.centralwidget)
        self.list_of_liked.setGeometry(QtCore.QRect(30, 340, 331, 211))
        self.list_of_liked.setStyleSheet("border-style: solid;\n"
                                         "border-width: 1px;\n"
                                         "border-color: rgb(252, 252, 252)\n"
                                         "")
        self.list_of_liked.setObjectName("list_of_liked")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 290, 311, 41))
        self.label.setStyleSheet("background-color: rgb(76, 76, 77);")
        self.label.setObjectName("label")
        self.previous_song_button = QtWidgets.QPushButton(self.centralwidget)
        self.previous_song_button.setGeometry(QtCore.QRect(510, 690, 60, 60))
        self.previous_song_button.setStyleSheet("border:0;")
        self.previous_song_button.setText("")
        self.previous_song_button.setObjectName("previous_song_button")
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(610, 670, 100, 100))
        self.play_button.setStyleSheet("border:0;")
        self.play_button.setText("")
        self.play_button.setObjectName("play_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.current_time.setText(_translate("MainWindow", "00.00"))
        self.name.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; color:#d6d6d6;\">Название</span></p></body></html>"))
        self.artist.setText(_translate("MainWindow",
                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; color:#d6d6d6;\">Исполнитель</span></p></body></html>"))
        self.date.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; color:#d6d6d6;\">Количество прослушиваний</span></p></body></html>"))
        self.load_button.setText(_translate("MainWindow", "ЗАГРУЗИТЬ"))
        self.length.setText(_translate("MainWindow", "00.00"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#d6d6d6;\">&quot;Мне нравится&quot;</span></p></body></html>"))
