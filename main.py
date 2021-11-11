import os
import shutil
import sqlite3
from os import listdir
import syntax
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *


# интерфейс окна справочника
class GuideWindow(QMainWindow):
    def setupUi(self, MainWindow, username):
        self.username = username
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 1440)
        MainWindow.setWindowTitle("PyGuide")
        MainWindow.setWindowIcon(QtGui.QIcon('guide.ico'))
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.tab = QTabWidget(self.centralwidget)
        self.tab.resize(1440, 1440)

        self.btnSave = QPushButton('Сохранить')
        self.btnSave.clicked.connect(self.save)
        self.statusBar().addWidget(self.btnSave)

        self.btnClose = QPushButton('Закрыть')
        self.btnClose.clicked.connect(self.closed)
        self.statusBar().addWidget(self.btnClose)

        self.btn_add = QPushButton('Добавить файл')
        self.btn_add.clicked.connect(self.addfile)
        self.statusBar().addWidget(self.btn_add)

        self.btn_add_name = QLineEdit('Имя файла')
        self.statusBar().addWidget(self.btn_add_name)

        self.combo = QComboBox(self)
        self.combo.addItem(".txt")
        self.combo.addItem(".jpg")
        self.statusBar().addWidget(self.combo)

        self.btn_del = QPushButton('Удалить файл')
        self.btn_del.clicked.connect(self.delete_file)
        self.statusBar().addWidget(self.btn_del)

        self.btn_color = QPushButton('Сменить цвет фона')
        self.btn_color.clicked.connect(self.changeColor)
        self.statusBar().addWidget(self.btn_color)


# функционал окна справочника
class GuideWindowFunctional(GuideWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self, username)
        self.username = username

        self.widget = QWidget()
        self.vbox = QVBoxLayout(self.widget)
        self.vbox.setSpacing(5)
        self.x = 300

        # создаем папку с именем пользователя для хранения его записей
        try:
            os.makedirs(f'{username}')
        except:
            pass

        self.add_widgets()

        self.scroll = QScrollArea(self.tab)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(QRect(600, 100, 150, 400))

        self.grid = QGridLayout(self.centralwidget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.tab, 1, 0, 1, 1)
        self.grid.addWidget(self.scroll, 1, 1, 2, 2)
        self.opened = []

        self.conn = sqlite3.connect('login.db')

    # удаление виджетов справочника
    def del_widgets(self):
        for i in reversed(range(self.vbox.count())):
            widgetToRemove = self.vbox.itemAt(i).widget()
            self.vbox.removeWidget(widgetToRemove)

    # добавление виджетов справочника
    def add_widgets(self):
        i = QLabel(self.tab)
        i.setText(f"Справочник")
        self.vbox.addWidget(i)
        for i in sorted(listdir('info')):
            self.i = QPushButton(self.tab)
            self.i.setGeometry(QRect(700, self.x, 100, 20))
            self.i.clicked.connect(self.open)
            self.i.setObjectName(f'info//{str(i)}')
            self.i.setText(str(i[:-4]))
            self.x += 10
            self.vbox.addWidget(self.i)
        self.i = QLabel(self.tab)
        self.i.setGeometry(QRect(700, self.x, 100, 20))
        self.i.setText(f"Справочник {self.username}'a")
        self.x += 10
        self.vbox.addWidget(self.i)
        for i in sorted(listdir(f'{self.username}')):
            self.i = QPushButton(self.tab)
            self.i.setGeometry(QRect(700, self.x, 100, 20))
            self.i.clicked.connect(self.open)
            self.i.setObjectName(f'{self.username}//{str(i)}')
            if str(i)[-4:] == ".jpg":
                self.i.setIcon(QIcon(self.i.objectName()))
            self.i.setText(str(i[:-4]))
            self.x += 10
            self.vbox.addWidget(self.i)

    # открытие записи
    def open(self):
        try:
            file_name = self.sender().objectName()
            if not file_name:
                return
            if file_name not in self.opened:
                if file_name[-4:] == '.txt':
                    with open(f'{file_name}', encoding="utf-8") as f:
                        txt = f.read()
                    idx = self.tab.addTab(QTextEdit(), file_name)
                    syntax.PythonHighlighter(self.tab.widget(idx))
                    self.tab.widget(idx).setPlainText(txt)
                    self.tab.widget(idx).setFont(QFont('Open Sans', 13))
                    self.tab.widget(idx).setObjectName(f'{file_name}')
                    self.tab.setCurrentIndex(idx)
                    self.opened.append(file_name)
                    if file_name[:6] == 'info//':
                        self.tab.widget(idx).setReadOnly(True)
                elif file_name[-4:] == '.jpg':
                    width = self.size().width() * 0.85
                    height = self.size().height() * 0.85
                    pixmap = QPixmap(file_name)
                    smaller_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
                    image = QLabel(self)
                    image.resize(50, 50)
                    image.move(80, 80)
                    image.setPixmap(smaller_pixmap)
                    idx = self.tab.addTab(image, file_name)
                    self.tab.widget(idx).setObjectName(f'{file_name}')
                    self.tab.setCurrentIndex(idx)
                    self.opened.append(file_name)
                else:
                    QMessageBox.information(self, 'Внимание!', 'Поддерживаются только txt и jpg.')
            else:
                QMessageBox.information(self, 'Внимание!', 'Файл уже открыт.')
        except:
            pass

    # сохранение записи
    def save(self):
        try:
            file_name = self.tab.currentWidget().objectName()
            if not file_name:
                return
            txt = self.tab.currentWidget().toPlainText()
            with open(f'{file_name}', 'w', encoding="utf-8") as f:
                f.write(txt)
        except:
            pass

    # закрытие записи
    def closed(self):
        try:
            file_name = self.tab.currentWidget().objectName()
            self.opened.remove(file_name)
            idx = self.tab.currentIndex()
            wgt = self.tab.widget(idx)
            self.tab.removeTab(idx)
            del wgt
        except:
            pass

    # создание записи или фотографии в папке пользователя
    def addfile(self):
        if self.combo.currentText() == '.txt':
            file = self.btn_add_name.text() + '.txt'
            if not os.path.isfile(f'{self.username}//{file}'):
                try:
                    f = open(f'{self.username}//{file}', 'w', encoding="utf-8")
                    f.close()
                    self.i = QPushButton(self.tab)
                    self.i.setGeometry(QRect(700, self.x, 100, 20))
                    self.i.clicked.connect(self.open)
                    self.i.setObjectName(f'{self.username}//{file}')
                    self.i.setText(file)
                    self.x += 10
                    self.vbox.addWidget(self.i)
                    self.del_widgets()
                    self.add_widgets()
                except:
                    QMessageBox.information(self, 'Внимание!', 'Вы ввели неверное значение')
            else:
                QMessageBox.information(self, 'Внимание!', 'Такой файл уже существует')
        elif self.combo.currentText() == '.jpg':
            if not os.path.isfile(f"{self.username}//{self.btn_add_name.text() + '.jpg'}"):
                try:
                    file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", '/', '*jpg')[0]
                    shutil.copy(os.path.join(file),
                                os.path.join(f"{self.username}//{self.btn_add_name.text() + '.jpg'}"))
                    self.del_widgets()
                    self.add_widgets()
                except:
                    QMessageBox.information(self, 'Внимание!', 'Неизвестная ошибка')
            else:
                QMessageBox.information(self, 'Внимание!', 'Такой файл уже существует')

    # удаление записи или скриншота из папки пользователя
    def delete_file(self):
        try:
            file_name = self.tab.currentWidget().objectName()
            if file_name[:6] != 'info//':
                self.opened.remove(file_name)
                if not file_name:
                    return
                os.remove(f'{file_name}')
                idx = self.tab.currentIndex()
                wgt = self.tab.widget(idx)
                self.tab.removeTab(idx)
                del wgt
                self.del_widgets()
                self.add_widgets()
            else:
                QMessageBox.information(self, 'Внимание!', 'Вы не можете удалить базовые функции')
        except:
            pass

    # меняем цвет фона
    def changeColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            style = "QMainWindow {background-color: " + color.name() + "}"
            self.setStyleSheet(style)
            self.conn.execute("UPDATE STYLE SET STYLES = ? WHERE USERNAME = ?", (color.name(), self.username))
            self.conn.commit()
