import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QTextEdit, QGroupBox, QComboBox, QDateEdit, QLineEdit, QMainWindow
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QIcon
import os
from tkinter import filedialog

from Códigos import api_validation
from xml_treatment import Xml_Treatment
from calTributos import CalTributos
from api_validation import Api_validation

path = os.getcwd()

def selecionar_arquivo():
    caminho = filedialog.askopenfilenames(
        title="Selecione um arquivo",
        filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
    )

    if caminho:
        print('_'*50)
        test(caminho)
        print('_'*50)

def test(path):
    # rodar em loop de acordo com o numero de notas
    cont = 0
    for i in path:
        caminho_nota = i #f'{caminho.split('Códigos')[0]}\\Notas\\Notas Novas\\{i}'
        # inicia a classe e pega os valores presentes na nota
        resultado = Xml_Treatment(caminho_nota)
        valores_notas = resultado.return_elements_taxes
        estado = resultado.state
        # chama a classe de calcular o tributo
        cal_trib = CalTributos(estado, valores_notas['BASE_CALC'])
        print(f'Valores da nota {cont + 1} do estado de {estado}: \n{valores_notas}\n\nValor dos impostos\n{cal_trib.calcular_json()}\n')
        cont +=1


class TelaPrincipal(QWidget):
    def __init__(self):
        self.validar_impostos_checked = False
        super().__init__()
        self.setWindowTitle("xmlScan")
        self.setFixedSize(1000, 700)
        self.setObjectName("janelaPrincipal")

        self.setStyleSheet("""
        #janelaPrincipal {
            background-color: #def1f0;
        }
        """)

        self.init_ui()

    def init_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # =====================================================
        # MENU LATERAL
        # =====================================================
        menu_lateral = QVBoxLayout()

        titulo = QLabel('<span style="color: white;"><b>xml</b>Scan</span>')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 40px; font-weight: bold;")
        titulo.setFixedHeight(70)

        self.btn_inicio = QPushButton("Página inicial")
        self.btn_inicio.setIcon(QIcon(os.path.join(path, 'assets', 'home_page.png')))
        self.btn_inicio.setIconSize(QSize(24, 24))

        self.btn_validar_impostos = QPushButton("Validar impostos")
        self.btn_validar_impostos.setIcon(QIcon(os.path.join(path, 'assets', 'validar_impostos.png')))
        self.btn_validar_impostos.setIconSize(QSize(24, 24))

        self.btn_validar_xml = QPushButton("Validar XML")
        self.btn_validar_xml.setIcon(QIcon(os.path.join(path, 'assets', 'validar_xml.png')))
        self.btn_validar_xml.setIconSize(QSize(24, 24))

        for btn in [self.btn_inicio, self.btn_validar_impostos, self.btn_validar_xml]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 15px;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: #34898a;
                }
            """)

        menu_lateral.addWidget(titulo)
        menu_lateral.addWidget(self.btn_inicio)
        menu_lateral.addWidget(self.btn_validar_impostos)
        menu_lateral.addWidget(self.btn_validar_xml)
        menu_lateral.addStretch()

        menu_widget = QWidget()
        menu_widget.setLayout(menu_lateral)
        menu_widget.setFixedWidth(220)

        menu_widget.setStyleSheet("""
            QWidget {
                background-color: #004d4d;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                color: white;
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 15px;
                font-size: 15px;
            }
        """)

        # =====================================================
        # ÁREA PRINCIPAL
        # =====================================================
        area_principal = QVBoxLayout()
        area_principal.setContentsMargins(30, 30, 30, 30)

        # label decorativas
        # label de decoracao (acima do log)
        self.fundo_label = QLabel(self)
        self.fundo_label.setStyleSheet("background-color: #1b6566;")
        self.fundo_label.setGeometry(220, 0, 780, 30)
        # self.fundo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.fundo_label_log = QLabel(self)
        self.fundo_label_log.setStyleSheet("background-color: #b9e7e4;")
        self.fundo_label_log.setGeometry(220, 30, 780, 50)
        # self.fundo_label_log.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.grupo_log = QGroupBox("Histórico e Log de atividades")
        self.grupo_log.setStyleSheet("""
        QGroupBox {
            border: none;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }

QGroupBox::title { subcontrol-origin: margin; left: 230px; color: #196464; padding: 15px 0px 0px 15px;; }
        """)

        #botao logout
        self.btn_logout = QPushButton("Log Out", self.grupo_log)
        self.btn_logout.setGeometry(620, 10, 100, 24)
        self.btn_logout.setIcon(QIcon(os.path.join(path, 'assets', 'logout.png')))
        self.btn_logout.setIconSize(QSize(24, 24))
        self.btn_logout.setStyleSheet("""
            color: black;
            background-color: #b9e7e4;
        """)
        # =========================
        # LINHA DE FILTROS
        # =========================

        # =========================
        # FILTRO NF-e
        # =========================
        self.filtro_numnfe = QLineEdit(self.grupo_log)
        self.filtro_numnfe.setPlaceholderText("Número NF-e")
        self.filtro_numnfe.setGeometry(0, 60, 194, 25)
        self.filtro_numnfe.setStyleSheet("""
            color: black;
            background-color: #dff2f0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
        """)

        # =========================
        # FILTRO DATA
        # =========================
        self.filtro_data = QDateEdit(self.grupo_log)
        self.filtro_data.setCalendarPopup(True)
        self.filtro_data.setDate(QDate.currentDate())
        self.filtro_data.setGeometry(210, 60, 150, 25)
        self.filtro_data.setStyleSheet("""
            QDateEdit {
                color: black;
                background-color: #dff2f0;
                border: 3px solid #9bc8c7;
                border-radius: 6px;
                font-size: 11px;
                padding-left: 5px;
            }

            /* Calendário popup */
            QCalendarWidget QWidget {
                background-color: white;
                color: black;
            }

            QCalendarWidget QToolButton {
                background-color: #196464;
                color: white;
                border: none;
                padding: 5px;
            }

            QCalendarWidget QMenu {
                background-color: white;
                color: black;
            }

            QCalendarWidget QSpinBox {
                background-color: white;
                color: black;
            }

            QCalendarWidget QAbstractItemView:enabled {
                background-color: white;
                color: black;
                selection-background-color: #1b6566;
                selection-color: white;
            }
        """)

        # =========================
        # FILTRO TIPO
        # =========================
        self.filtro_tipo = QComboBox(self.grupo_log)
        self.filtro_tipo.addItems(["Todos", "Validação XML", "Validação Impostos", "Erro"])
        self.filtro_tipo.setGeometry(380, 60, 200, 25)
        self.filtro_tipo.setStyleSheet("""
            background-color: #dff2f0;
            color: black;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
        """)

        # =========================
        # Selecionar Notas Area para o botao validar impostos
        # =========================
        self.btn_select_arq = QPushButton("Selecionar Notas", self.grupo_log)
        self.btn_select_arq.setGeometry(1, 60, 720, 25)
        self.btn_select_arq.setStyleSheet("""
            color: #1b6566;
            background-color: #90c1c0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
        """)

        # =========================
        # Selecionar Notas Area para o botao validar xml
        # =========================
        self.btn_select_xml = QPushButton("Selecionar Notas", self.grupo_log)
        self.btn_select_xml.setGeometry(1, 60, 720, 25)
        self.btn_select_xml.setStyleSheet("""
            color: #1b6566;
            background-color: #90c1c0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
        """)

        # =========================
        # BOTÃO BUSCAR
        # =========================
        self.btn_filtrar = QPushButton("Buscar", self.grupo_log)
        self.btn_filtrar.setGeometry(600, 60, 120, 25)
        self.btn_filtrar.setStyleSheet("""
        color: black;
            background-color: #90c1c0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
        """)

        # =========================
        # ÁREA DE LOG
        # =========================
        self.area_log = QTextEdit(self.grupo_log)
        self.area_log.setReadOnly(True)
        self.area_log.setStyleSheet("""
            color: black;
            background-color: #dff2f0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 16px;
        """)
        self.area_log.setGeometry(0, 100, 720, 540)

        area_principal.addWidget(self.grupo_log)

        # =====================================================
        # FINAL
        # =====================================================
        #remove os botoes secundarios das func
        self.btn_select_arq.hide()
        self.btn_select_xml.hide()

        layout_principal.addWidget(menu_widget)
        layout_principal.addLayout(area_principal)

        # =====================================================
        # CONEXÕES
        # =====================================================

        # filtrar na pagina inicial
        self.btn_filtrar.clicked.connect(self.filtrar_log)
        #botao de logout
        self.btn_logout.clicked.connect(self.logout)

        # validar os impostos
        self.btn_validar_impostos.clicked.connect(self.validar_impostos)
        #valida xml
        self.btn_validar_xml.clicked.connect(self.validar_xml)
        #mostra a pag inicial (banco de dados)
        self.btn_inicio.clicked.connect(self.pag_inicial)
        self.btn_select_arq.clicked.connect(self.selecionar_arquivo)
        self.btn_select_xml.clicked.connect(self.selecionar_arquivo)

    # =====================================================
    # FUNÇÃO DO BOTÃO
    # =====================================================
    def filtrar_log(self):
        data = self.filtro_data.date().toString("dd/MM/yyyy")
        tipo = self.filtro_tipo.currentText()
        num_nfe = self.filtro_numnfe.text()

        self.area_log.append(f"Filtro aplicado -> Data: {data} | Tipo: {tipo} | Num NFe: {num_nfe}" if num_nfe else f"Filtro aplicado -> Data: {data} | Tipo: {tipo}")

    def logout(self):
        self.hide()
        self.tela_login = Tela_Login()
        self.tela_login.show()

    def validar_impostos(self):
        self.validar_impostos_checked = True
        self.grupo_log.setTitle("Validar Impostos")
        self.grupo_log.setStyleSheet("""
        QGroupBox {
            border: none;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }

QGroupBox::title { subcontrol-origin: margin; left: 250px; color: #196464; padding: 15px 0px 0px 15px;; }
        """)
        self.area_log.clear()
        self.filtro_numnfe.hide()
        self.filtro_data.hide()
        self.filtro_tipo.hide()
        self.btn_filtrar.hide()
        self.btn_select_arq.show()

        #conectar com o back aqui

        #pega quantas notas serão analisadas
        # num_notas = 20
        # #dados da nota
        # numero = 1
        # valor = 100.00
        # status = 0
        #
        # self.adicionar_resultado(num_notas, numero, valor, status)


    def validar_xml(self):
        self.validar_impostos_checked = False
        self.btn_select_arq.hide()
        self.area_log.clear()
        self.filtro_numnfe.hide()
        self.filtro_data.hide()
        self.filtro_tipo.hide()
        self.btn_filtrar.hide()
        self.btn_select_xml.show()
        self.grupo_log.setTitle("Validar XML")
        self.grupo_log.setStyleSheet("""
                QGroupBox {
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    margin-top: 10px;
                }

        QGroupBox::title { subcontrol-origin: margin; left: 250px; color: #196464; padding: 15px 0px 0px 15px;; }
                """)
        self.area_log.clear()
        # self.area_log.append(f'Em desenvolvimento. Pronto na Sprint 2')

    def pag_inicial(self):
        self.grupo_log.setTitle("Histórico e Log de atividades")
        self.btn_select_arq.hide()
        self.filtro_numnfe.show()
        self.filtro_data.show()
        self.filtro_tipo.show()
        self.btn_filtrar.show()
        self.area_log.clear()
        self.area_log.append(f'Em desenvolvimento. Pronto na Sprint 3')

    def adicionar_resultado_api(self, nome_nota, response, status_code):
        bloco = f"""
        <div style="
            background-color: #e8f5f4;
            border: 2px solid #9bc8c7;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        ">
            <div><b>Nota:</b> {nome_nota}</div>
            <div><b>Validação XML:</b> {response}</div>
            <div><b>Status API:</b> {status_code}</div>
        """
        self.area_log.append(bloco + '<div style="height: 120px;"></div>')

    #faz blocos no textedit
    def adicionar_resultado(self, nota_nova, numero, valor, status):
        if nota_nova:
            status_imp = 'OK'
            for tipo_imposto in ['IBS', 'CBS', 'IS']:
                if valor[tipo_imposto] != status[tipo_imposto]:
                    status_imp = 'NOK'
                    break
                else:
                    continue

            bloco = f"""
            <div style="
                background-color: #e8f5f4;
                border: 2px solid #9bc8c7;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            ">
                <div><b>Nota:</b> {numero}</div>
                <div><b>Tipo Nota:</b> Nova</div>
                <div><b>Estado Nota:</b> {status['estado']}</div>
                <div><b>Valor Total Nota:</b> R${valor['BASE_CALC']}</div>
                <div><b>Valor Imposto Nota IBS/CBS/IS:</b> R${valor['IBS']}/ R${valor['CBS']}/ R${valor['IS']}</div>
                <div><b>Valor Calculado IBS/CBS/IS:</b> R${status['IBS']}/ R${status['CBS']}/ R${status['IS']}</div>
                <div><b>Total Impostos:</b> {status['total_impostos']}</div>
                <div><b>Status:</b> {status_imp}</div>
            </div>
            """
        else:
            bloco = f"""
            <div style="
                background-color: #e8f5f4;
                border: 2px solid #9bc8c7;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            ">
                <div><b>Nota:</b> {numero}</div>
                <div><b>Tipo Nota:</b> Antiga</div>
                <div><b>Estado Nota:</b> {status['estado']}</div>
                <div><b>Valor Total Nota:</b> R${valor['BASE_CALC']}</div>
                <div><b>Valor Simulado IBS/CBS/IS:</b> R${status['IBS']}/ R${status['CBS']}/ R${status['IS']}</div>
                <div><b>Total Impostos:</b> {status['total_impostos']}</div>
            </div>
            """

        self.area_log.append(bloco + '<div style="height: 120px;"></div>')

    def selecionar_arquivo(self):
        self.area_log.clear()
        caminho = filedialog.askopenfilenames(
            title="Selecione um arquivo",
            filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
        )

        if caminho:
            self.treatment(caminho)



    def treatment(self, path):
        # rodar em loop de acordo com o numero de notas
        if self.validar_impostos_checked:
            # self.validar_impostos_checked = False
            cont = 0
            for i in path:
                caminho_nota = i
                # inicia a classe e pega os valores presentes na nota
                resultado = Xml_Treatment(caminho_nota)
                nota_nova, valores_notas = resultado.return_elements_taxes
                estado = resultado.state
                nome_nota = i.split('/')[-1]
                cal_trib = CalTributos(estado, valores_notas['BASE_CALC'])
                self.adicionar_resultado(nota_nova, nome_nota, valores_notas, cal_trib.calcular_json())
                cont += 1
        else:
            cont = 0
            for i in path:
                caminho_nota = i
                # inicia a classe e pega os valores presentes na nota
                resultado = Xml_Treatment(caminho_nota)
                string_xml = resultado.return_string_invoice
                nome_nota = i.split('/')[-1]
                xml_validation = Api_validation(string_xml)
                self.adicionar_resultado_api(nome_nota, xml_validation.response, xml_validation.status_code)
                cont += 1

class Tela_Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("xmlScan")
        self.setFixedSize(1000, 700)
        self.init_ui()

    def init_ui(self):
        # fundo da tela
        self.fundo_label = QLabel(self)
        self.fundo_label.setStyleSheet("background-color: #1b6566;")
        self.fundo_label.setGeometry(0, 0, 1000, 700)
        self.fundo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        #fundo login
        self.fundo_label = QLabel(self)
        self.fundo_label.setStyleSheet("background-color: #619f9d;")
        self.fundo_label.setGeometry(300, 240, 400, 200)
        self.fundo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # titulo tela
        titulo = QLabel("xmlScan", self)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            color: white;
            font-size: 40px;
            font-weight: bold;
        """)
        titulo.setGeometry(200, 80, 600, 80)

        #titulo login
        titulo_login = QLabel("Login", self)
        titulo_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_login.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        titulo_login.setGeometry(200, 220, 600, 80)

        #titulo senha
        titulo_senha = QLabel("Senha", self)
        titulo_senha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_senha.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        titulo_senha.setGeometry(200, 310, 600, 80)

        # campo user
        self.user = QLineEdit(self)
        self.user.setPlaceholderText("Usuário")
        self.user.setGeometry(394, 290, 220, 25)
        self.user.setStyleSheet("""
            background-color: #dff2f0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            color: black;
            font-size: 11px;
        """)

        # campo senha
        self.senha = QLineEdit(self)
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha.setGeometry(394, 380, 220, 25)
        self.senha.setStyleSheet("""
            background-color: #dff2f0;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            color: black;
            font-size: 11px;
        """)

        # botao login
        self.btn_login = QPushButton("Log In", self)
        self.btn_login.setGeometry(300, 450, 400, 25)
        self.btn_login.setStyleSheet("""
            color: black;
            background-color: #b9e8e4;
            border: 3px solid #9bc8c7;
            border-radius: 6px;
            font-size: 11px;
                            QPushButton:hover {
                    background-color: #34898a;
                }
        """)

        # area de log (quando tiver login e senha, verificar user e/ou conexao com a internet)
        self.label_erro = QLabel("", self)
        self.label_erro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_erro.setGeometry(300, 480, 400, 40)
        self.label_erro.setStyleSheet("""
            color: white;
            font-size: 21px;
            font-weight: bold;
        """)

        # #conexao dos botoes
        self.btn_login.clicked.connect(self.open_home_page)


    def open_home_page(self):
        usuario = self.user.text()
        senha = self.senha.text()
        if usuario == "admin" and senha == "admin":
            self.label_erro.setText("")
            self.hide()
            self.home_page = TelaPrincipal()
            self.home_page.show()
        else:
            self.label_erro.setText("Usuário ou senha inválidos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()#Tela_Login() #TelaPrincipal()
    janela.show()
    sys.exit(app.exec())