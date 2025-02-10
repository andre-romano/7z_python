# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 300)
        self.label = QLabel(MainWindow)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 381, 16))
        self.progress_bar = QProgressBar(MainWindow)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setGeometry(QRect(10, 90, 381, 23))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.log_output = QTextEdit(MainWindow)
        self.log_output.setObjectName(u"log_output")
        self.log_output.setGeometry(QRect(10, 120, 381, 171))
        self.log_output.setReadOnly(True)
        self.compress_button = QPushButton(MainWindow)
        self.compress_button.setObjectName(u"compress_button")
        self.compress_button.setGeometry(QRect(10, 30, 381, 24))
        self.decompress_button = QPushButton(MainWindow)
        self.decompress_button.setObjectName(u"decompress_button")
        self.decompress_button.setGeometry(QRect(10, 60, 381, 24))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"7-Zip Python Frontend", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.compress_button.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.decompress_button.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

