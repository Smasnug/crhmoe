#!/usr/bin/env python
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtPrintSupport import *
import os
import sys
import platform

system = platform.system() + " " + platform.release()
qwebengver = "null"

class MainWindow(QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        def about_dialog():
            QMessageBox.about(self, f"Crhmoe", "Version v2023.05.29.1 running on {}".format(system))
 
        self.browser = QWebEngineView()
 
        self.browser.setUrl(QUrl("http://yahoo.com"))
 
        oldAgent = self.browser.page().profile().httpUserAgent()
        userAgent = oldAgent.replace("QtWebEngine/{}".format(qwebengver), "Crhmoe/2023.05.29")
        self.browser.page().profile().setHttpUserAgent(userAgent)

        self.browser.urlChanged.connect(self.update_urlbar)
 
        self.browser.loadFinished.connect(self.update_title)
 
        self.setCentralWidget(self.browser)
 
        self.status = QStatusBar()
 
        self.setStatusBar(self.status)
 
        navtb = QToolBar("Navigation")
 
        self.addToolBar(navtb)
 
        back_btn = QAction("Back", self)
 
        back_btn.setStatusTip("Back to previous page")
 
        back_btn.triggered.connect(self.browser.back)
 
        navtb.addAction(back_btn)
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
 
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)
 
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
 
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)
 
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        about_btn = QAction("About", self)
        about_btn.setStatusTip("AboutDialog")
        about_btn.triggered.connect(about_dialog)
        navtb.addAction(about_btn)

        navtb.addSeparator()
 
        self.urlbar = QLineEdit()
 
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        navtb.addWidget(self.urlbar)
 
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
 
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        self.show()
 
 
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Crhmoe" % title)
 
 
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://yahoo.com"))
 
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            full = "https://search.yahoo.com/search?p=" + self.urlbar.text()
            self.browser.setUrl(QUrl(full))
        else:
            self.browser.setUrl(q)
 
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
 
app = QApplication(sys.argv)
 
app.setApplicationName("Crhmoe")
 
window = MainWindow()
 
app.exec()