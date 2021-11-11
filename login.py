from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *
from main import GuideWindowFunctional
from signup import Dialog_signUp
from changepass import Dialog_Changepass
import sqlite3
import sys

# стиль интерфейса
StyleSheet = '''
QTabBar::tab {
    border: 2px solid #C4C4C3;
    border-bottom-color: #C2C7CB;
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    min-width: 16ex;
    padding: 2px;
}
 
QTabBar::tab:selected, QTabBar::tab:hover {
    background: #FFFFFF;
}
 
QTabBar::tab:selected {
    border-bottom-color: #FFFFFF;
}
 
QTabBar::tab:!selected {
    margin-top: 2px;
}
QMainWindow {
    background-color: #E6CAF0;
}
QTextEdit {
    background-color: white;
}
QDialog {
    background-color: #E6CAF0;
}
QLineEdit {
    spacing: 5px;
    font-size:14px;     
    background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: Open Sans 14px;
    min-width: 10em;
    padding: 1px;
}
QPushButton {
    font-size:14px;     
    font: Open Sans 14px;
}
'''


# интерфейс окна авторизации
class Ui_login(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        Dialog.setWindowTitle("Авторизация")

        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(200, 120, 200, 40))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.uname_lineEdit.setPlaceholderText("Логин")
        self.uname_lineEdit.setToolTip("Введите логин, под которым вы регистрировались")

        self.pass_lineEdit = QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QRect(200, 180, 200, 40))
        self.pass_lineEdit.setObjectName("password_lineEdit")
        self.pass_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_lineEdit.setPlaceholderText("Пароль")
        self.pass_lineEdit.setToolTip("Введите пароль, который вы ввели при регистрации")

        self.login_btn = QPushButton(Dialog)
        self.login_btn.setGeometry(QRect(200, 230, 100, 30))
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setText("Авторизация")

        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(300, 230, 100, 30))
        self.signup_btn.setObjectName("signup_btn")
        self.signup_btn.setText("Регистрация")

        self.changepass_btn = QPushButton(Dialog)
        self.changepass_btn.setGeometry(QRect(220, 270, 160, 30))
        self.changepass_btn.setObjectName("signup_btn")
        self.changepass_btn.setText("Сменить пароль")

        font = QFont()
        font.setPointSize(18)
        self.req_label = QLabel(Dialog)
        self.req_label.setFont(font)
        self.req_label.setGeometry(QRect(210, 40, 200, 40))
        self.req_label.setObjectName("req_label")
        self.req_label.setText("Авторизация")


# создание базы данных
class LoginDatabase():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def is_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True


# авторизация пользователя
class _login_login(QDialog, Ui_login):
    def __init__(self, parent=None):
        super(_login_login, self).__init__(parent)
        self.setupUi(self)

        self.loginDatabase = LoginDatabase('login.db')
        # проверка, есть ли таблица в базе данных, если нет - создается таблица и заносится запись admin
        if self.loginDatabase.is_table('USERS'):
            pass
        else:
            self.loginDatabase.conn.execute("CREATE TABLE USERS(USERNAME TEXT NOT NULL, EMAIL TEXT, PASSWORD TEXT)")
            self.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?)", ('admin', 'admin', 'admin'))
            self.loginDatabase.conn.commit()
        if self.loginDatabase.is_table('STYLE'):
            pass
        else:
            self.loginDatabase.conn.execute("CREATE TABLE STYLE(USERNAME TEXT NOT NULL, STYLES TEXT NOT NULL)")
            self.loginDatabase.conn.execute("INSERT INTO STYLE VALUES(?, ?)", ('admin', '#E6CAF0'))
            self.loginDatabase.conn.commit()

        self.login_btn.clicked.connect(self.loginCheck)
        self.changepass_btn.clicked.connect(self.changePassword)
        self.signup_btn.clicked.connect(self.signUpCheck)

    # сообщение при авторизации
    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    # получение размера монитора
    def get_size_of_desktop(self):
        return int(QDesktopWidget().screenGeometry().width() * 0.6 // 1), \
               int(QDesktopWidget().screenGeometry().height() * 0.6 // 1)

    # открытие справочника
    def GuideWindowShow(self, username):
        self.welcomeWindow = GuideWindowFunctional(username)
        w, h = self.get_size_of_desktop()
        self.welcomeWindow.resize(w, h)
        style = self.loginDatabase.conn.execute("SELECT STYLES FROM STYLE WHERE USERNAME = ?", (username,))
        style = "QMainWindow {background-color: " + style.fetchall()[0][0] + "}"
        self.loginDatabase.conn.close()
        style = StyleSheet + style
        self.welcomeWindow.setStyleSheet(style)
        self.welcomeWindow.show()

    # открытие окна регистрации
    def signUpShow(self):
        self.signUpWindow = Dialog_signUp(self)
        self.signUpWindow.setStyleSheet(StyleSheet)
        self.signUpWindow.show()

    # открытие окна смены пароля
    def changePassword(self):
        self.signUpWindow = Dialog_Changepass(self)
        self.signUpWindow.setStyleSheet(StyleSheet)
        self.signUpWindow.show()

    # проверка авторизации
    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()
        if (not username) or (not password):
            QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.loginDatabase.conn.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                                                 (username, password))
        if len(result.fetchall()):
            self.GuideWindowShow(username)
            self.hide()
            self.loginDatabase.conn.close()
        else:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')

    def signUpCheck(self):
        self.signUpShow()


# запуск программы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = _login_login()
    w.setWindowIcon(QtGui.QIcon('log.ico'))
    w.setStyleSheet(StyleSheet)
    w.show()
    sys.exit(app.exec_())