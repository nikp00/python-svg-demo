from random import randint
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtCore import *

from lxml import etree


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(500, 500)

        self.bg = QFrame()
        self.bg.setStyleSheet("background-color: #ababab")
        self.bg_layout = QVBoxLayout(self.bg)

        # Configure SVG widget
        self.svg_widget = QSvgWidget()
        self.bg_layout.addWidget(self.svg_widget, Qt.Alignment())

        # Configure button
        self.color_button = QPushButton("Randomize", self)
        self.color_button.setStyleSheet("background-color: #fff")
        self.color_button.clicked.connect(self.update_svg)
        self.bg_layout.addWidget(self.color_button)

        self.setCentralWidget(self.bg)
        self.show()

        self.load_svg("example.svg")
        self.update_svg_widget()

    def load_svg(self, svg_path):
        self.svg_data = etree.parse(svg_path)

    def update_svg_widget(self):
        self.svg_widget.load(etree.tounicode(self.svg_data.getroot()).encode())

    def update_svg(self):
        root = self.svg_data.getroot()

        for node in root.findall("{http://www.w3.org/2000/svg}g"):
            for path in node.findall("{http://www.w3.org/2000/svg}path"):
                path.attrib["style"] = f"fill: rgb({','.join(self.random_color())})"

        self.update_svg_widget()

    @staticmethod
    def random_color():
        return [str(randint(0, 255)) for _ in range(3)]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
