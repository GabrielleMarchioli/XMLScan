import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import Qt


class Janela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch com PyQt6")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Switch desligado")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.switch = QCheckBox("Modo")
        self.switch.setCursor(Qt.CursorShape.PointingHandCursor)

        self.switch.setStyleSheet("""
            QCheckBox {
                font-size: 18px;
                spacing: 10px;
            }

            QCheckBox::indicator {
                width: 50px;
                height: 25px;
                border-radius: 12px;
                background-color: #999;
            }

            QCheckBox::indicator:checked {
                background-color: #4CAF50;
            }
        """)

        self.switch.toggled.connect(self.verificar_switch)

        layout.addWidget(self.label)
        layout.addWidget(self.switch, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def verificar_switch(self, estado):
        if estado:
            self.funcao_ligado()
        else:
            self.funcao_desligado()

    def funcao_ligado(self):
        self.label.setText("Switch ligado")
        print("Função ligada acionada")

    def funcao_desligado(self):
        self.label.setText("Switch desligado")
        print("Função desligada acionada")


app = QApplication(sys.argv)

janela = Janela()
janela.show()

sys.exit(app.exec())