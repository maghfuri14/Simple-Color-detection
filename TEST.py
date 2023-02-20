#import libraries
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
app = QApplication(sys.argv)
value = 0


def winodow():  # create Window

    wiget = QWidget()
    layout = QHBoxLayout(wiget)

    slider = QSlider(Qt.Orientation.Horizontal)

    slider.setValue(value)
    slider.setMaximum(255)
    slider.setMinimum(0)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.valueChanged.connect(lambda: onChange(2))
    layout.addWidget(slider)
    layout.addWidget(QLabel("HSV"))
    wiget.show()
    sys.exit(app.exec())


def clicked():
    print("oke")


def onChange(val):
    global value
    print(val)


if __name__ == '__main__':
    winodow()
