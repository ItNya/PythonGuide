from PyQt5 import QtWidgets
from PyQt5.Qt import *


# открытие окна смены пароля
class Ui_changePass(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        Dialog.setWindowTitle("Смена пароля")

        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(200, 130, 200, 40))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.uname_lineEdit.setPlaceholderText("Логин")
        self.uname_lineEdit.setToolTip("Если не помните - пишите на почту поддержки\nadmin@gmail.com")

        self.email_lineEdit = QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QRect(200, 180, 200, 40))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.email_lineEdit.setPlaceholderText("Почта")
        self.email_lineEdit.setToolTip("Если не помните - пишите на почту поддержки\nadmin@gmail.com")

        self.password_lineEdit = QLineEdit(Dialog)
        self.password_lineEdit.setGeometry(QRect(200, 230, 200, 40))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText("Старый пароль")
        self.password_lineEdit.setToolTip("Если не помните - пишите на почту поддержки\nadmin@gmail.com")

        self.new_password_lineEdit = QLineEdit(Dialog)
        self.new_password_lineEdit.setGeometry(QRect(200, 280, 200, 40))
        self.new_password_lineEdit.setObjectName("password_lineEdit")
        self.new_password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_lineEdit.setPlaceholderText("Новый пароль")
        self.new_password_lineEdit.setToolTip("Придумайте пароль по надежнее старого\nПароли совпадать не должны")

        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(220, 340, 160, 30))
        self.signup_btn.setObjectName("signup_btn")
        self.signup_btn.setText("Сменить пароль")

        font = QFont()
        font.setPointSize(18)
        self.req_label = QLabel(Dialog)
        self.req_label.setFont(font)
        self.req_label.setGeometry(QRect(210, 40, 200, 40))
        self.req_label.setObjectName("req_label")
        self.req_label.setText("Смена пароля")


# функционал окна смены пароля
class Dialog_Changepass(QDialog, Ui_changePass):
    def __init__(self, parent=None):
        super(Dialog_Changepass, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)

    # меняем старый пароль на новый в базе данных
    def insertData(self):
        username = self.uname_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()
        new_password = self.new_password_lineEdit.text()

        if (not username) or (not email) or (not password) or (not new_password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        if password == new_password:
            QMessageBox.information(self, 'Внимание!', 'Новый пароль не может совпадать со старым.')
        else:
            result = self.parent.loginDatabase.conn.execute("SELECT * FROM USERS WHERE USERNAME = ? and EMAIL = ? and PASSWORD = ?", (username, email, password))
            if result.fetchall():
                self.parent.loginDatabase.conn.execute("UPDATE USERS SET PASSWORD = ? WHERE USERNAME = ?", (new_password, username))
                self.parent.loginDatabase.conn.commit()
                self.close()
            else:
                QMessageBox.information(self, 'Внимание!', 'Неверные данные')

