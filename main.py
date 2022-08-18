from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow import Ui_MainWindow
import subprocess, platform
from coppelia_driver import *
from mult_matrix import *
from mqtt_config import *
import numpy as np

ht = HomogeneousTransformation()


def isnumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True


class MainWin:
    def __init__(self):
        self.status_con = 0
        self.m1x = 0.0
        self.m1y = 0.0
        self.m1z = 0.0
        self.m2x = 0.0
        self.m2y = 0.0
        self.m2z = 0.0
        self.m3x = 0.0
        self.m3y = 0.0
        self.m3z = 0.0
        self.theta1 = 0.0
        self.theta2 = 0.0
        self.broker_status = 0
        self.broker_client = 0

        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        self.ui.btn_virtual.clicked.connect(self.show_virtual)
        self.ui.btn_fisico.clicked.connect(self.show_fisico)
        self.ui.pushButton_voltar.clicked.connect(self.show_home)
        self.ui.pushButton_voltar_2.clicked.connect(self.show_home)

        self.ui.pushButton_carregar_cena.clicked.connect(self.load_scene1)
        self.ui.pushButton_carregar_cena_3.clicked.connect(self.load_scene2)
        self.ui.pushButton_conectar_cena.clicked.connect(self.connect_scene)
        self.ui.pushButton_conectar_cena_3.clicked.connect(self.connect_scene)

        self.ui.pushButton_posicionar.clicked.connect(self.init_position)
        self.ui.pushButton_executar_translacao.clicked.connect(self.translation)
        self.ui.pushButton_executar_rotacao.clicked.connect(self.rotation)
        self.ui.pushButton_executar_cinematica.clicked.connect(self.kinematic)
        self.ui.pushButton.clicked.connect(self.load_help)

        self.ui.pushButton_connect_broker.clicked.connect(self.connect_broker)
        self.ui.horizontalSlider_m0.valueChanged.connect(self.slider_m0_change_value)
        self.ui.horizontalSlider_m1.valueChanged.connect(self.slider_m1_change_value)
        self.ui.horizontalSlider_m2.valueChanged.connect(self.slider_m2_change_value)
        self.ui.horizontalSlider_m3.valueChanged.connect(self.slider_m3_change_value)
        self.ui.horizontalSlider_m4.valueChanged.connect(self.slider_m4_change_value)

    def show(self):
        self.main_win.show()

    def show_virtual(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_virtual)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_virtual)

    def show_fisico(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_fisico)

    def show_home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

    def connect_broker(self):
        mqtt_init()
        self.broker_status = mqtt_get_status_conenction()
        if self.broker_status:
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : lime")
        else:
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")

    def slider_m0_change_value(self):
        if not self.broker_status:
            self.msg_box("Erro", "Necessário conectar com broker!", QMessageBox.Critical)
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")
        else:
            m0_value = self.ui.horizontalSlider_m0.value()
            self.ui.label_slider_m0.setText(str(m0_value))
            mqtt_publish(0, m0_value)

    def slider_m1_change_value(self):
        if not self.broker_status:
            self.msg_box("Erro", "Necessário conectar com broker!", QMessageBox.Critical)
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")
        else:
            m1_value = self.ui.horizontalSlider_m1.value()
            self.ui.label_slider_m1.setText(str(m1_value))
            mqtt_publish(1, m1_value)

    def slider_m2_change_value(self):
        if not self.broker_status:
            self.msg_box("Erro", "Necessário conectar com broker!", QMessageBox.Critical)
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")
        else:
            m2_value = self.ui.horizontalSlider_m2.value()
            self.ui.label_slider_m2.setText(str(m2_value))
            mqtt_publish(2, m2_value)

    def slider_m3_change_value(self):
        if not self.broker_status:
            self.msg_box("Erro", "Necessário conectar com broker!", QMessageBox.Critical)
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")
        else:
            m3_value = self.ui.horizontalSlider_m3.value()
            self.ui.label_slider_m3.setText(str(m3_value))
            mqtt_publish(3, m3_value)

    def slider_m4_change_value(self):
        if not self.broker_status:
            self.msg_box("Erro", "Necessário conectar com broker!", QMessageBox.Critical)
            self.ui.pushButton_connect_broker.setStyleSheet("background-color : red")
        else:
            m4_value = self.ui.horizontalSlider_m4.value()
            self.ui.label_slider_m4.setText(str(m4_value))
            mqtt_publish(4, m4_value)

    def load_scene1(self):
        self.load_scene('./coppelia_files/scenes/simple_cuboid.ttt', 1)

    def load_scene2(self):
        self.load_scene('./coppelia_files/scenes/simple_rr.ttt', 2)

    def load_scene(self, filepath, scene_num):
        if platform.system() == 'Darwin':  # macOS
            try:
                e = subprocess.call(('open', filepath))
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : lime")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : lime")
            except e:
                print(sys.stderr, "Execution failed:", e)
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : red")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : red")
        elif platform.system() == 'Windows':  # Windows
            try:
                e = subprocess.call(('start', filepath), shell=True)
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : lime")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : lime")
            except e:
                print(sys.stderr, "Execution failed:", e)
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : red")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : red")
        else:  # linux variants
            try:
                e = subprocess.call(('xdg-open', filepath))
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : lime")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : lime")
            except e:
                print(sys.stderr, "Execution failed:", e)
                if scene_num == 1:
                    self.ui.pushButton_carregar_cena.setStyleSheet("background-color : red")
                elif scene_num == 2:
                    self.ui.pushButton_carregar_cena_3.setStyleSheet("background-color : red")

    def translation(self):
        if self.status_con != 1:
            self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : red")
        else:
            self.read_m1()
            self.read_m2()
            ht.set_m1(self.m1x, self.m1y, self.m1z)
            ht.set_m2(self.m2x, self.m2y, self.m2z)
            rt = ht.get_translation()
            self.ui.label_resultado_translacao.setText("(" + str(rt[0]) + ", " + str(rt[1]) + ", " + str(rt[2]) + ")")
            coppelia_set_position(rt[0], rt[1], rt[2])

    def connect_scene(self):
        ret = coppelia_connect()
        if ret == -1:
            self.msg_box("Erro", "Falha na conexão!", QMessageBox.Critical)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : red")
            self.ui.pushButton_conectar_cena_3.setStyleSheet("background-color : red")
        else:
            self.msg_box("Sucesso", "Conectado com sucesso!", QMessageBox.Information)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : lime")
            self.ui.pushButton_conectar_cena_3.setStyleSheet("background-color : lime")
            self.status_con = 1

    def msg_box(self, title, message, box_type):
        msg = QMessageBox()
        msg.setStyleSheet("QMessageBox{height: 300px; min-height: 300px; max-height: 300px;}")
        msg.setIcon(box_type)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def init_position(self):
        if self.status_con != 1:
            self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : red")
        else:
            self.read_m1()
            coppelia_set_position(self.m1x, self.m1y, self.m1z)

    def rotation(self):
        if self.status_con != 1:
            self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : red")
        else:
            self.read_m3()

            init_pos = coppelia_get_position()
            ht.set_m1(init_pos[0], init_pos[1], init_pos[2])
            res_r = ht.get_rotation_x(self.m3x)
            coppelia_set_position(res_r[0], res_r[1], res_r[2])

            init_pos = coppelia_get_position()
            ht.set_m1(init_pos[0], init_pos[1], init_pos[2])
            res_r = ht.get_rotation_y(self.m3y)
            coppelia_set_position(res_r[0], res_r[1], res_r[2])

            init_pos = coppelia_get_position()
            ht.set_m1(init_pos[0], init_pos[1], init_pos[2])
            res_r = ht.get_rotation_z(self.m3z)
            coppelia_set_position(res_r[0], res_r[1], res_r[2])

            res_r[0] = np.format_float_positional(res_r[0], precision=2)
            res_r[1] = np.format_float_positional(res_r[1], precision=2)
            res_r[2] = np.format_float_positional(res_r[2], precision=2)

            self.ui.label_resultado_rotacao.setText(
                "(" + str(res_r[0]) + ", " + str(res_r[1]) + ", " + str(res_r[2]) + ")")

    def kinematic(self):
        if self.status_con != 1:
            self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)
            self.ui.pushButton_conectar_cena.setStyleSheet("background-color : red")
        else:
            self.read_theta()
            if self.theta1 > 160 or self.theta1 < -160 or self.theta2 > 160 or self.theta2 < -160:
                self.load_help()
            else:
                if coppelia_set_joint1_position(self.theta1) == -1:
                    self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)

                if coppelia_set_joint2_position(self.theta2) == -1:
                    self.msg_box("Erro", "Necessário conectar com a cena!", QMessageBox.Critical)

                x_pos, y_pos = coppelia_get_xy_position(self.theta1, self.theta2)

                self.ui.label_cinx_result.setText(str(x_pos))
                self.ui.label_ciny_result.setText(str(y_pos))

    def load_help(self):
        self.msg_box("Ajuda", "θ1 e θ2 devem estar no range (-160° a 160°)", QMessageBox.Information)

    def read_m1(self):
        if isnumber(self.ui.lineEdit_m1x.text()):
            self.m1x = float(self.ui.lineEdit_m1x.text())
        else:
            self.m1x = 0.0
            self.ui.lineEdit_m1x.setText(str(self.m1x))

        if isnumber(self.ui.lineEdit_m1y.text()):
            self.m1y = float(self.ui.lineEdit_m1y.text())
        else:
            self.m1y = 0.0
            self.ui.lineEdit_m1y.setText(str(self.m1y))

        if isnumber(self.ui.lineEdit_m1z.text()):
            self.m1z = float(self.ui.lineEdit_m1z.text())
        else:
            self.m1z = 0.0
            self.ui.lineEdit_m1z.setText(str(self.m1z))

        print("M1", self.m1x, self.m1y, self.m1z)

    def read_m2(self):
        if isnumber(self.ui.lineEdit_m2x.text()):
            self.m2x = float(self.ui.lineEdit_m2x.text())
        else:
            self.m2x = 0.0
            self.ui.lineEdit_m1x.setText(str(self.m2x))

        if isnumber(self.ui.lineEdit_m2y.text()):
            self.m2y = float(self.ui.lineEdit_m2y.text())
        else:
            self.m2y = 0.0
            self.ui.lineEdit_m1y.setText(str(self.m2y))

        if isnumber(self.ui.lineEdit_m2z.text()):
            self.m2z = float(self.ui.lineEdit_m2z.text())
        else:
            self.m2z = 0.0
            self.ui.lineEdit_m1z.setText(str(self.m2z))

        print("M2", self.m2x, self.m2y, self.m2z)

    def read_m3(self):
        if isnumber(self.ui.lineEdit_m3x.text()):
            self.m3x = float(self.ui.lineEdit_m3x.text())
        else:
            self.m3x = 0.0
            self.ui.lineEdit_m3x.setText(str(self.m3x))

        if isnumber(self.ui.lineEdit_m3y.text()):
            self.m3y = float(self.ui.lineEdit_m3y.text())
        else:
            self.m3y = 0.0
            self.ui.lineEdit_m3y.setText(str(self.m3y))

        if isnumber(self.ui.lineEdit_m3z.text()):
            self.m3z = float(self.ui.lineEdit_m3z.text())
        else:
            self.m3z = 0.0
            self.ui.lineEdit_m3z.setText(str(self.m3z))

        print("M3", self.m3x, self.m3y, self.m3z)

    def read_theta(self):
        if isnumber(self.ui.lineEdit_theta1.text()):
            self.theta1 = float(self.ui.lineEdit_theta1.text())
        else:
            self.theta1 = 0.0
            self.ui.lineEdit_theta1.setText(str(self.theta1))

        if isnumber(self.ui.lineEdit_theta2.text()):
            self.theta2 = float(self.ui.lineEdit_theta2.text())
        else:
            self.theta2 = 0.0
            self.ui.lineEdit_theta2.setText(str(self.theta2))

        print("Theta", self.theta1, self.theta2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())
