import sys
from PyQt5.QtWidgets import QApplication, QPushButton, \
    QMainWindow, QFileDialog, QListWidgetItem, QBoxLayout, \
    QCheckBox, QLabel
from PyQt5 import QtGui, QtCore, QtMultimedia
import eyed3
from ui import Ui_MainWindow
from PyQt5.QtWinExtras import QtWin
import os


class Song:
    def __init__(self, path):
        audio = eyed3.load(path)
        self.__path = path
        self.__title = audio.tag.title
        self.__recording_date = audio.tag.recording_date
        self.__artist = audio.tag.artist
        images = audio.tag.images
        if not images:
            with open('images/cover_image.png', 'rb') as f:
                self.__image = f.read()
                self.have_image = False
        else:
            self.__image = images[0].image_data
            self.have_image = True

    @property
    def date(self):
        return self.__recording_date

    @property
    def name(self):
        return self.__title

    @property
    def artist(self):
        return self.__artist

    @property
    def byte_image(self):
        return self.__image

    def __str__(self):
        return self.__path

    def __eq__(self, other):
        return self.title == other.title

    def __ne__(self, other):
        return not self == other

    @property
    def title(self):
        return f"{self.name} - {self.artist}"


class Mp3(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self._translate = QtCore.QCoreApplication.translate
        my_app_id = 'mycompany.myproduct.subproduct.version'
        QtWin.setCurrentProcessExplicitAppUserModelID(my_app_id)

        self.setWindowTitle('MP3-Плеер')
        self.setFixedSize(self.size())

        self.play_button.setIcon(QtGui.QIcon('images/play_button.png'))
        self.play_button.setIconSize(QtCore.QSize(100, 100))

        self.previous_song_button.setIcon(QtGui.QIcon('images/previous_song_button.png'))
        self.previous_song_button.setIconSize(QtCore.QSize(60, 60))

        self.next_song_button.setIcon(QtGui.QIcon('images/next_song_button.png'))
        self.next_song_button.setIconSize(QtCore.QSize(60, 60))

        self.song_slider.sliderMoved.connect(self.slider)
        self.song_slider.setStyleSheet("""
            QSlider{
                background: #2F2F2F;
            }
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 8px;
            }
            QSlider::sub-page:qlineargradient {
                background: #3B99FC;
                border-radius: 5px;
            }
        """)

        self.play_button.clicked.connect(self.play)
        self.music_is_playing = False

        self.load_button.clicked.connect(self.load)

        self.next_song_button.clicked.connect(self.next_song)

        self.previous_song_button.clicked.connect(self.previous_song)

        self.list_of_songs.setStyleSheet("""
            QListWidget::item {color: rgb(214, 214, 214);
                               font-size: 30px;
                               border-style: solid;
                                border-width: 1px;
                                border-color: rgb(252, 252, 252);}
            QListWidget::item:selected {
                                        border-color: red;
                                        }
            QListWidget {border-style: solid;
                         border-width: 1px;
                         border-color: rgb(252, 252, 252);}
                                
        """)
        self.list_of_mp3 = {}
        self.list_of_songs.itemClicked.connect(self.list_of_songs_click)

        self.setWindowIcon(QtGui.QIcon('images/icon.jpg'))
        pass

    def play(self):
        if not self.music_is_playing:
            self.music_is_playing = True
            self.play_button.setIcon(QtGui.QIcon('images/pause_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))
        else:
            self.music_is_playing = False
            self.play_button.setIcon(QtGui.QIcon('images/play_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))

    def load(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.list_of_songs.clear()
        for filename in os.listdir(dirlist):
            if filename.endswith('.mp3'):
                song = Song(os.path.join(dirlist, filename))
                if song.title not in self.list_of_mp3:
                    self.list_of_mp3.update({song.title: song})
        for title in self.list_of_mp3:
            self.list_of_songs.addItem(QListWidgetItem(title))

    def next_song(self):
        ...

    def previous_song(self):
        ...

    def slider(self):
        ...

    def list_of_songs_click(self):
        item = self.list_of_songs.currentItem()
        current_song: Song = self.list_of_mp3[item.text()]
        if current_song.have_image:
            try:
                with open("images/cover.png", mode='wb') as f:
                    f.write(current_song.byte_image)
                self.cover.setPixmap(QtGui.QPixmap("images/cover.png"))
                os.remove("images/cover.png")
            finally:
                if os.path.exists("images/cover.png"):
                    os.remove("images/cover.png")
        self.name.setText(self._translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span"
                                          " style=\" font-size:12pt; color:#d6d6d6;\">"
                                          f"Название: {current_song.name}</span></p></body></html>"))
        self.artist.setText(self._translate("MainWindow",
                                            "<html><head/><body><p align=\"center\"><span"
                                            " style=\" font-size:12pt; color:#d6d6d6;\">"
                                            f"Исполнитель: {current_song.artist}</span></p></body></html>"))
        self.date.setText(self._translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span"
                                          " style=\" font-size:12pt; color:#d6d6d6;\">"
                                          f"Год выпуска: {current_song.date}</span></p></body></html>"))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    eyed3.log.setLevel("ERROR")
    app = QApplication(sys.argv)
    ex = Mp3()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
