from PyQt5 import QtWidgets
from PyQt5.Qt import *


# интерфейс окна регистрации
class Ui_signUp(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        Dialog.setWindowTitle("Регистрация")

        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(200, 130, 200, 40))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.uname_lineEdit.setPlaceholderText("Логин")
        self.uname_lineEdit.setToolTip("Придумайте логин, чтобы авторизовываться под ним")

        self.email_lineEdit = QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QRect(200, 180, 200, 40))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.email_lineEdit.setPlaceholderText("Почта")
        self.email_lineEdit.setToolTip("Введите вашу почту, чтобы защитить учетную запись")

        self.password_lineEdit = QLineEdit(Dialog)
        self.password_lineEdit.setGeometry(QRect(200, 230, 200, 40))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText("Пароль")
        self.password_lineEdit.setToolTip("Придумайте надежный пароль, чтобы защитить учетную запись\nЗапомните его, "
                                          "восстановить будет нельзя")

        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(220, 290, 160, 30))
        self.signup_btn.setObjectName("signup_btn")
        self.signup_btn.setText("Зарегестрироваться")

        font = QFont()
        font.setPointSize(18)
        self.req_label = QLabel(Dialog)
        self.req_label.setFont(font)
        self.req_label.setGeometry(QRect(210, 40, 200, 40))
        self.req_label.setObjectName("req_label")
        self.req_label.setText("Регистрация")


# функционал регистрационного окна
class Dialog_signUp(QDialog, Ui_signUp):
    def __init__(self, parent=None):
        super(Dialog_signUp, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)

    # запись пользователя в базу данных
    def insertData(self):
        username = self.uname_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        if (not username) or (not email) or (not password):
            QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.parent.loginDatabase.conn.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        if result.fetchall():
            QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
        else:
            self.parent.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?)",
                                                   (username, email, password))
            self.parent.loginDatabase.conn.commit()
            self.parent.loginDatabase.conn.execute("INSERT INTO STYLE VALUES(?, ?)",
                                                   (username, '#F3C8F0'))
            self.parent.loginDatabase.conn.commit()
            self.close()
