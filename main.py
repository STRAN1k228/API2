import sys
import requests
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

api_key = '7cbc0f3a-0c4a-4166-b742-3d178ae6fb40'

class MainWindow(QMainWindow):
    f: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('task.ui', self)

        self.map_zoom = 17
        self.map_ll = [30.302348, 59.991619]
        self.map_theme = 'map'
        self.toggle_theme_button = self.findChild(QPushButton, 'toggleThemeButton')
        self.toggle_theme_button.clicked.connect(self.toggle_theme)

        self.refresh_map()

    def toggle_theme(self):

        if self.map_theme == 'map':
            self.map_theme = 'dark'
        else:
            self.map_theme = 'map'
        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_PageUp:
            if self.map_zoom < 21:
                self.map_zoom += 1
        if event.key() == QtCore.Qt.Key.Key_PageDown:
            if self.map_zoom > 0:
                self.map_zoom -= 1
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.map_ll[0] -= 0.001
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.map_ll[0] += 0.001
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.map_ll[1] += 0.0007
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.map_ll[1] -= 0.0007

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'l': self .map_theme,  # Добавляем параметр темы
            'apikey': api_key
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        response = session.get('https://static-maps.yandex.ru/v1?', params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.f.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())