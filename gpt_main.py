import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QTimer
from PyQt5.QtWidgets import QLabel
from datetime import datetime
from cryptography.fernet import Fernet
import pickle
import openai
import setting
import pyperclip


def decrypt_api_key(encrypted_key, key):
    cipher_suite = Fernet(key)
    decrypted_key = cipher_suite.decrypt(encrypted_key)
    return decrypted_key.decode()


def load_key():
    try:
        with open("key.key", 'rb') as filekey:
            key = filekey.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", 'wb') as filekey:
            filekey.write(key)
    return key


settings = QSettings("settings.ini", QSettings.IniFormat)
wholeText = settings.value("history")
summary = ""


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(429, 489)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./assets/icon1.jpeg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.selection = QtWidgets.QTextEdit(Form)
        self.selection.setMaximumSize(QtCore.QSize(16777215, 85))
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(12)
        self.selection.setFont(font)
        self.selection.setAcceptDrops(True)
        self.selection.setStyleSheet("QTextEdit{\n"
                                     "    border: 2px solid #0d6efd;\n"
                                     "    border-radius: 5px;\n"
                                     "}")
        self.selection.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.selection.setObjectName("selection")
        self.gridLayout_2.addWidget(self.selection, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QTextEdit(Form)
        self.scrollArea.setMinimumSize(QtCore.QSize(300, 300))
        self.scrollArea.setStyleSheet("QTextEdit{\n"
                                      "    border: 2px solid #0d6efd;\n"
                                      "    border-radius: 5px;\n"
                                      "}")
        self.scrollArea.setFont(font)
        self.scrollArea.setAcceptDrops(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 407, 383))
        self.scrollArea.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 4)
        self.answer = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.answer.setFont(font)
        self.answer.setStyleSheet("")
        self.answer.setObjectName("answer")
        self.gridLayout_2.addWidget(self.answer, 1, 0, 1, 1)
        self.history_btn = QtWidgets.QPushButton(Form)
        self.history_btn.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.history_btn.setFont(font)
        self.history_btn.setStyleSheet("QPushButton {\n"
                                       "    border: none;\n"
                                       "    border-radius: 10px;\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: #e0e0eb;\n"
                                       "}\n"
                                       "QPushButton:pressed {\n"
                                       "    background-color: #b3b3cc;\n"
                                       "}")
        self.history_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./assets/file-plus-2.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.history_btn.setIcon(icon1)
        self.history_btn.setObjectName("history_btn")
        self.gridLayout_2.addWidget(self.history_btn, 1, 2, 1, 1)
        self.setting_btn = QtWidgets.QPushButton(Form)
        self.setting_btn.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.setting_btn.setFont(font)
        self.setting_btn.setStyleSheet("QPushButton {\n"
                                       "    border: none;\n"
                                       "    border-radius: 10px;\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: #e0e0eb;\n"
                                       "}\n"
                                       "QPushButton:pressed {\n"
                                       "    background-color: #b3b3cc;\n"
                                       "}")
        self.setting_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/settings.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setting_btn.setIcon(icon2)
        self.setting_btn.setObjectName("setting_btn")
        self.gridLayout_2.addWidget(self.setting_btn, 1, 3, 1, 1)
        self.send_btn = QtWidgets.QPushButton(Form)
        self.send_btn.setMinimumSize(QtCore.QSize(0, 28))
        self.send_btn.setMaximumSize(QtCore.QSize(60, 16777215))
        self.send_btn.setStyleSheet("QPushButton{\n"
                                    "    color: white;\n"
                                    "    background-color: #3399ff;\n"
                                    "    border-radius: 10px;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: #3385ff;\n"
                                    "}\n"
                                    "QPushButton:pressed {\n"
                                    "    background-color: #0d6efd;\n"
                                    "}\n"
                                    "")
        self.send_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./assets/send (2).png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_btn.setIcon(icon3)
        self.send_btn.setObjectName("send_btn")
        self.gridLayout_2.addWidget(self.send_btn, 2, 1, 1, 3)
        self.copy_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.copy_btn.setFont(font)
        self.copy_btn.setStyleSheet("QPushButton {\n"
                                    "    border: none;\n"
                                    "    border-radius: 10px;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: #e0e0eb;\n"
                                    "    border-radius: 10px;\n"
                                    "}\n"
                                    "QPushButton:pressed {\n"
                                    "    background-color: #b3b3cc;\n"
                                    "    border-radius: 10px;\n"
                                    "}")
        self.copy_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./assets/copy.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_btn.setIcon(icon4)
        self.copy_btn.setObjectName("copy_btn")
        self.gridLayout_2.addWidget(self.copy_btn, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        enc = open("encrypt", 'br')
        encrypted_key = enc.read()
        self.key = load_key()
        openai.api_key = decrypt_api_key(encrypted_key, self.key)

        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        self.selection.setText(self.settings.value("text"))
        self.scrollArea.setText(self.settings.value("history"))
        self.answer.currentIndexChanged.connect(self.send_answer)
        self.send_btn.clicked.connect(self.send_word)
        self.setting_btn.clicked.connect(Form.close)
        self.setting_btn.clicked.connect(self.open_setting)
        self.history_btn.clicked.connect(self.clean_history)
        self.copy_btn.clicked.connect(self.copy_answer)
        with open('prompts', 'rb') as file:
            prompts = pickle.load(file)
            keys = prompts.keys()
            for keys in prompts:
                self.answer.addItem(keys)

        self.copy_snackbar = QLabel(Form)
        self.copy_snackbar.setGeometry(QtCore.QRect(346, 337, 51, 20))

        self.copy_snackbar.hide()

        self.timer = QTimer()
        self.timer.setInterval(2000)  # 10 seconds
        self.timer.timeout.connect(self.hide_copy_snackbar)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "GPT"))

    def hide_copy_snackbar(self):
        # Hide the snackbar.
        self.copy_snackbar.hide()

    def copy_answer(self):
        global summary
        pyperclip.copy(summary)
        self.copy_snackbar.setGeometry(QtCore.QRect(
            self.copy_btn.pos().x() - 10, self.copy_btn.pos().y() - 30, 51, 20))

        self.copy_snackbar.setText("Copied!")
        self.copy_snackbar.show()
        # Start the timer.
        self.timer.start()

    def clean_history(self):
        global wholeText
        wholeText = ""
        self.settings.setValue("history", wholeText)
        self.scrollArea.setText("")

    def send_answer(self):
        with open('prompts', 'rb') as file:
            prompts = pickle.load(file)
            prompt = prompts[self.answer.currentText()]
            self.selection.setText(prompt)
        self.selection.append(self.settings.value("text"))

    def send_word(self):
        api_model = int(self.settings.value("number"))
        if api_model == 0:
            type_model = "gpt-3.5-turbo"
        else:
            type_model = "gpt-4"
        instructions_to_the_model = self.selection.toPlainText()
        response = openai.ChatCompletion.create(
            model=type_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": instructions_to_the_model},
            ]
        )
        global wholeText
        global summary
        summary = response['choices'][0]['message']['content']
        wholeText += datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\nQuestion: " + \
            self.selection.toPlainText() + "\n\n" + "Answer: " + summary + "\n \n"
        self.scrollArea.setText(wholeText)
        self.settings.setValue("history", wholeText)
        self.selection.setText("")

    def open_setting(self):
        SettingW = QtWidgets.QDialog()
        ui = setting.Ui_Form()
        ui.setupUi(SettingW)
        # SettingW.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        SettingW.exec_()


settings = QSettings("settings.ini", QSettings.IniFormat)
top = int(settings.value("top"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    print(top)
    Form.show()
    sys.exit(app.exec_())
