import sys
from PyQt5.QtWidgets import QApplication,QHBoxLayout, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel, QSlider, QFormLayout, QGridLayout,QLineEdit,QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory
import math as m
# import maths as m

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Test Menu')
        self.setGeometry(100, 100, 300, 100)

        layout = QGridLayout()

        self.reactor_dropdown = QComboBox()
        self.reactor_dropdown.addItem('MCF')
        self.reactor_dropdown.addItem('ICF')
        self.reactor_dropdown.addItem('MTF')
        self.reactor_dropdown.setCurrentText('MCF')

        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setMinimum(1)
        self.radius_slider.setMaximum(5)
        self.radius_slider.setValue(3)
        self.radius_slider.setTickPosition(QSlider.TicksBelow)
        self.radius_slider.setTickInterval(1)

        tick_values_layout = QHBoxLayout()
        num_ticks = self.radius_slider.maximum() - self.radius_slider.minimum() + 1

        for i in range(num_ticks):
            if i > 0:
                # Add stretch before each label (except the first one) to distribute the space evenly
                tick_values_layout.addStretch()
            tick_label = QLabel(str(i + self.radius_slider.minimum()))
            tick_label.setAlignment(Qt.AlignCenter)
            tick_values_layout.addWidget(tick_label)

        # tick_values_layout.addStretch()

        self.Decimal_places = QSpinBox()
        self.Decimal_places.setMinimum(1)
        self.Decimal_places.setMaximum(10)

        self.maths_button = QPushButton('Calculate (&M)')
        self.maths_button.clicked.connect(self.calculate)
        

        self.display_label = QLabel(f"Current reactor: {self.reactor_dropdown.currentText()} ")
        self.volume_label = QLabel("Volume: ")
        self.reactor_dropdown.currentTextChanged.connect(self.show_option)
        self.reactor_dropdown.currentTextChanged.connect(self.calculate)
        self.radius_slider.valueChanged.connect(self.calculate)
        self.Decimal_places.valueChanged.connect(self.calculate)

        layout.addWidget(self.display_label, 0,0)
        layout.addWidget(self.reactor_dropdown,0,1)
        layout.addWidget(self.radius_slider,1,0,1,2)
        layout.addLayout(tick_values_layout,2,0,1,2)
        layout.addWidget(self.Decimal_places,3,1)
        layout.addWidget(self.maths_button,3,0)
        layout.addWidget(self.volume_label,4,0,1,2)

        # layout.addRow(self.maths_button, self.radius_slider)
        # layout.addRow(self.display_label,self.volume_label)
        # # display_layout.addWidget(self.display_label)
        # layout.addWidget(self.volume_label)
        # layout.addWidget(self.radius_slider)
        # # layout.addLayout(tick_values_layout)
        # layout.addWidget(self.maths_button)
       
       

        self.setLayout(layout)
        # self.setLayout(display_layout)
    def show_option(self):
        selected_option = self.reactor_dropdown.currentText()
        self.display_label.setText(f"Current reactor: {selected_option}")

    def calculate(self,Decimal_places):
        radius = self.radius_slider.value()
        if self.reactor_dropdown.currentText() == 'MCF':
            volume = 4/3 * 3.141592 * radius**3
        elif self.reactor_dropdown.currentText() == 'ICF':
            volume = 10/3 * 3.141592 * radius**3
        elif self.reactor_dropdown.currentText() == 'MTF':
            volume = 20/3 * 3.141592 * radius**3
        volume = round(volume, Decimal_places)
        self.volume_label.setText(f"Volume: {volume}")
    


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()