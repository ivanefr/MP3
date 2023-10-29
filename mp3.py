import sys
from PyQt5.QtWidgets import QApplication, QPushButton, \
    QMainWindow, QFileDialog, QListWidgetItem, QBoxLayout, \
    QCheckBox, QLabel, QListWidget, QDialog, QDialogButtonBox, \
    QVBoxLayout
from PyQt5 import QtGui, QtCore, QtMultimedia
import eyed3
from ui import Ui_MainWindow
from PyQt5.QtWinExtras import QtWin
import os
from mutagen.mp3 import MP3
import sqlite3


class ConfirmDialog(QDialog):
    def __init__(self, append=True, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Подтверждение")

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        if append:
            text = "Добавить песню в \"Мне нравится\"?"
        else:
            text = "Удалить песню из \"Мне нравится\"?"
        label = QLabel(text)
        label.setWordWrap(True)
        self.layout.addWidget(label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
        self.setFixedSize(250, 150)
        cancel_button = self.button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")

        self.setStyleSheet("""
        QDialog {
            background-color: #2F2F2F;
        }
        QLabel {
            color: rgb(214, 214, 214);
            font-size: 20px;
        } 
        QPushButton {
            color: green;
            font-weight: bold;
        }
        QPushButton[text="Cancel"] {
            color: red;
        }
        """)


class Song:
    def __init__(self, path):
        audio = eyed3.load(path)
        self.__path = path
        self.__title = audio.tag.title
        self.__recording_date = audio.tag.recording_date
        self.__artist = audio.tag.artist
        self.__length = MP3(path).info.length
        images = audio.tag.images
        if not images:
            with open('images/cover_image.png', 'rb') as f:
                self.__image = f.read()
        else:
            self.__image = images[0].image_data

    @property
    def length(self):
        return self.__length

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
        try:
            return self.title == other.title
        except AttributeError:
            return False

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

        stylesheet_list_widget = """
            QListWidget::item {color: rgb(214, 214, 214);
                                border-width: 2px;
                                border-color: rgb(252, 252, 252);
                                margin-bottom: 5px
                                }
            QListWidget::item:selected {
                                        border: solid;
                                        border-color: white;
                                        border-width: 3px;                               
                                        }
            QListWidget {border-style: solid;
                         border-width: 1px;
                         border-color: rgb(252, 252, 252);
                         font-size: 20px}
                                
        """

        self.list_of_songs.setStyleSheet(stylesheet_list_widget)
        self.list_of_liked.setStyleSheet(stylesheet_list_widget)

        self.list_of_mp3 = {}
        self.list_of_liked_mp3 = {}
        self.liked_to_del = {}

        self.list_of_songs.itemClicked.connect(self.list_of_songs_click)
        self.list_of_songs.itemDoubleClicked.connect(self.list_of_songs_double_click)

        self.list_of_liked.itemClicked.connect(self.list_of_liked_click)
        self.list_of_liked.itemDoubleClicked.connect(self.list_of_liked_double_click)

        self.list_of_songs.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.list_of_liked.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setWindowIcon(QtGui.QIcon('images/icon.jpg'))
        self.player = False

        self.last_listening = None

        with sqlite3.connect("db.sqlite") as db:
            cur = db.cursor()
            cur.execute("""SELECT path FROM liked_music
                           ORDER BY -id""")
            arr = cur.fetchall()
            for path in arr:
                song = Song(path[0])
                item = QListWidgetItem(song.title)
                self.list_of_liked.addItem(item)
                self.list_of_liked_mp3.update({song.title: song})
                self.liked_to_del.update({song.title: item})

    def play(self):
        if not self.music_is_playing:
            self.music_is_playing = True
            self.play_button.setIcon(QtGui.QIcon('images/pause_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))
        else:
            self.media_player.pause()
            self.music_is_playing = False
            self.play_button.setIcon(QtGui.QIcon('images/play_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))
            self.music_is_playing = False
            return
        selected_lol = self.list_of_liked.selectedItems()
        selected_los = self.list_of_songs.selectedItems()
        if not selected_los and not selected_lol:
            if not self.list_of_mp3 and not self.list_of_liked_mp3:
                self.music_is_playing = False
                self.play_button.setIcon(QtGui.QIcon('images/play_button.png'))
                self.play_button.setIconSize(QtCore.QSize(100, 100))
                return
            elif self.list_of_mp3:
                self.list_of_songs.setCurrentRow(0)
                item = self.list_of_songs.currentItem()
                song: Song = self.list_of_mp3[item.text()]
            else:
                self.list_of_liked.setCurrentRow(0)
                item = self.list_of_liked.currentItem()
                song: Song = self.list_of_liked_mp3[item.text()]
            try:
                with open("images/cover.png", mode='wb') as f:
                    f.write(song.byte_image)
                self.cover.setPixmap(QtGui.QPixmap("images/cover.png"))
                os.remove("images/cover.png")
            finally:
                if os.path.exists("images/cover.png"):
                    os.remove("images/cover.png")
        elif selected_los:
            item = self.list_of_songs.currentItem()
            song: Song = self.list_of_mp3[item.text()]
        else:
            item = self.list_of_liked.currentItem()
            song: Song = self.list_of_liked_mp3[item.text()]
        if not self.player:
            content = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(str(song)))
            self.media_player = QtMultimedia.QMediaPlayer()
            self.media_player.setMedia(content)
            self.media_player.play()
            self.player = True

            self.media_player.positionChanged.connect(self.mediaplayer_pos_changed)
            self.media_player.durationChanged.connect(self.mediaplayer_duration_changed)
            self.media_player.mediaStatusChanged.connect(self.mediaplayer_status_changed)
        else:
            self.media_player.play()

    def mediaplayer_status_changed(self):
        if self.media_player.state() == QtMultimedia.QMediaPlayer.State.StoppedState:
            self.next_song()

    def mediaplayer_duration_changed(self, dur):
        self.song_slider.setMaximum(dur)

    def mediaplayer_pos_changed(self, pos):
        self.song_slider.setValue(pos)
        sec = pos // 1000
        m = sec // 60
        s = sec % 60
        self.current_time.setText(f"{m:0>2}:{s:0>2}")

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
        selected_lol = self.list_of_liked.selectedItems()
        selected_los = self.list_of_songs.selectedItems()

        if selected_lol or selected_los:
            if selected_los:
                index = self.list_of_songs.currentRow()
                if index + 1 >= self.list_of_songs.count():
                    index = -1
                self.list_of_songs.setCurrentRow(index + 1)
                self.list_of_songs_click()
            elif selected_lol:
                index = self.list_of_liked.currentRow()
                if index + 1 >= self.list_of_liked.count():
                    index = -1
                self.list_of_liked.setCurrentRow(index + 1)
                self.list_of_liked_click()

    def previous_song(self):
        selected_lol = self.list_of_liked.selectedItems()
        selected_los = self.list_of_songs.selectedItems()

        if selected_lol or selected_los:
            if selected_los:
                index = self.list_of_songs.currentRow()
                if index - 1 < 0:
                    index = self.list_of_songs.count()
                self.list_of_songs.setCurrentRow(index - 1)
                self.list_of_songs_click()
            elif selected_lol:
                index = self.list_of_liked.currentRow()
                if index - 1 < 0:
                    index = self.list_of_liked.count()
                self.list_of_liked.setCurrentRow(index - 1)
                self.list_of_liked_click()

    def slider(self, pos):
        self.media_player.setPosition(pos)
        sec = pos // 1000
        m = sec // 60
        s = sec % 60
        self.current_time.setText(f"{m:0>2}:{s:0>2}")

    def list_of_liked_click(self):
        self.list_of_songs.clearSelection()
        item = self.list_of_liked.currentItem()
        current_song: Song = self.list_of_liked_mp3[item.text()]
        self.count_of_listening_song(current_song)
        self.last_listening = current_song
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
                                          f"{current_song.name}</span></p></body></html>"))
        self.artist.setText(self._translate("MainWindow",
                                            "<html><head/><body><p align=\"center\"><span"
                                            " style=\" font-size:12pt; color:#d6d6d6;\">"
                                            f"{current_song.artist}</span></p></body></html>"))
        length = current_song.length
        m = int(length // 60)
        s = int(length % 60)
        self.length.setText(f"{m:0>2}:{s:0>2}")
        c = self.get_count_of_listening(current_song)
        text = f"Прослушана {c} раз"
        if c % 10 in (2, 3, 4) and c // 10 != 1:
            text += 'а'
        self.date.setText(self._translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span"
                                          " style=\" font-size:12pt; color:#d6d6d6;\">"
                                          f"{text}</span></p></body></html>"))

        content = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(str(current_song)))
        self.media_player = QtMultimedia.QMediaPlayer()
        self.media_player.setMedia(content)
        self.song_slider.setSliderPosition(0)

        if not self.music_is_playing:
            self.media_player.pause()
        else:
            self.media_player.play()
            self.play_button.setIcon(QtGui.QIcon('images/pause_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))
        self.player = True

        self.media_player.positionChanged.connect(self.mediaplayer_pos_changed)
        self.media_player.durationChanged.connect(self.mediaplayer_duration_changed)
        self.media_player.mediaStatusChanged.connect(self.mediaplayer_status_changed)

    def list_of_liked_double_click(self):
        item = self.list_of_liked.currentItem()
        current_song: Song = self.list_of_liked_mp3[item.text()]
        dialog = ConfirmDialog(append=False)
        if dialog.exec():
            self.next_song()
            index = self.list_of_liked.row(item)
            self.liked_to_del[current_song.title].setHidden(True)
            self.list_of_liked.takeItem(index)
            del self.list_of_liked_mp3[current_song.title]
            del self.liked_to_del[current_song.title]
            with sqlite3.connect("db.sqlite") as db:
                cur = db.cursor()
                cur.execute(f"""
                DELETE FROM liked_music 
                WHERE path = '{current_song}'
                """)
                db.commit()
            if not self.liked_to_del:
                self.cover.setPixmap(QtGui.QPixmap("images/cover_image.png"))
                self.length.setText("00:00")
                self.current_time.setText("00:00")
                del self.media_player
                self.song_slider.setSliderPosition(0)
                self.play_button.setIcon(QtGui.QIcon('images/play_button.png'))
                self.play_button.setIconSize(QtCore.QSize(100, 100))
                self.music_is_playing = False
                self.player = False

    def count_of_listening_song(self, song: Song):
        with sqlite3.connect("db.sqlite") as db:
            cur = db.cursor()
            if song != self.last_listening:
                cur.execute(f"""
                SELECT count FROM count_of_listening_music
                WHERE path = '{song}'
                """)
                if not cur.fetchall():
                    cur.execute(f"""
                    INSERT INTO count_of_listening_music (count, path)
                    VALUES (1, "{song}")
                    """)
                else:
                    cur.execute(f"""
                    SELECT count FROM count_of_listening_music
                    WHERE path = '{song}'
                    """)
                    c = cur.fetchall()[0][0]
                    c += 1
                    cur.execute(f"""
                    UPDATE count_of_listening_music SET count = {c} WHERE path = '{song}'
                    """)

                cur.execute(f"""
                SELECT count FROM count_of_listening_music
                WHERE path = '{song}'
                """)
                print(cur.fetchall())
            db.commit()

    def get_count_of_listening(self, song):
        with sqlite3.connect("db.sqlite") as db:
            cur = db.cursor()
            cur.execute(f"""
            SELECT count FROM count_of_listening_music
            WHERE path = '{song}'
            """)
            c = cur.fetchall()[0][0]
            db.commit()
        return c

    def list_of_songs_click(self):
        self.list_of_liked.clearSelection()
        item = self.list_of_songs.currentItem()
        current_song: Song = self.list_of_mp3[item.text()]
        self.count_of_listening_song(current_song)
        self.last_listening = current_song
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
                                          f"{current_song.name}</span></p></body></html>"))
        self.artist.setText(self._translate("MainWindow",
                                            "<html><head/><body><p align=\"center\"><span"
                                            " style=\" font-size:12pt; color:#d6d6d6;\">"
                                            f"{current_song.artist}</span></p></body></html>"))
        length = current_song.length
        m = int(length // 60)
        s = int(length % 60)
        self.length.setText(f"{m:0>2}:{s:0>2}")
        c = self.get_count_of_listening(current_song)
        text = f"Прослушана {c} раз"
        if c % 10 in (2, 3, 4) and c // 10 != 1:
            text += 'а'

        self.date.setText(self._translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span"
                                          " style=\" font-size:12pt; color:#d6d6d6;\">"
                                          f"{text}</span></p></body></html>"))

        content = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(str(current_song)))
        self.media_player = QtMultimedia.QMediaPlayer()
        self.media_player.setMedia(content)
        if not self.music_is_playing:
            self.media_player.pause()
        else:
            self.media_player.play()
            self.play_button.setIcon(QtGui.QIcon('images/pause_button.png'))
            self.play_button.setIconSize(QtCore.QSize(100, 100))
        self.song_slider.setSliderPosition(0)
        self.player = True

        self.media_player.positionChanged.connect(self.mediaplayer_pos_changed)
        self.media_player.durationChanged.connect(self.mediaplayer_duration_changed)
        self.media_player.mediaStatusChanged.connect(self.mediaplayer_status_changed)

    def list_of_songs_double_click(self):
        item = self.list_of_songs.currentItem()
        current_song: Song = self.list_of_mp3[item.text()]
        if current_song.title not in self.list_of_liked_mp3:
            dialog = ConfirmDialog()
            if dialog.exec():
                with sqlite3.connect("db.sqlite") as db:
                    cur = db.cursor()
                    cur.execute(f"""
                    INSERT INTO liked_music (path)
                    VALUES ("{current_song}")
                    """)
                    db.commit()

                self.list_of_liked_mp3.update({current_song.title: current_song})
                new_item = QListWidgetItem(current_song.title)
                self.list_of_liked.insertItem(0, new_item)
                self.liked_to_del.update({current_song.title: new_item})

        else:
            dialog = ConfirmDialog(append=False)
            if dialog.exec():
                self.liked_to_del[current_song.title].setHidden(True)
                del self.list_of_liked_mp3[current_song.title]
                del self.liked_to_del[current_song.title]
                with sqlite3.connect("db.sqlite") as db:
                    cur = db.cursor()
                    cur.execute(f"""
                    DELETE FROM liked_music 
                    WHERE path = '{current_song}'
                    """)
                    db.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    with sqlite3.connect("db.sqlite") as database:
        cursor = database.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS liked_music (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT)
                  """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS count_of_listening_music (
                   count INTEGER,
                   path TEXT
                   )
        """)
        database.commit()
    eyed3.log.setLevel("ERROR")
    app = QApplication(sys.argv)
    ex = Mp3()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
