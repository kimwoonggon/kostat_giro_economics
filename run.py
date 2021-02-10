import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import datetime
from gunseol_crawl_ui import Ui_MainWindow
#form_class = uic.loadUiType("건설경기동향조사_수집프로그램.ui")[0]

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # 1. 건설 명부 로드하기
        # 2. 설정 파일 경로 설정하기
        # self.SearchBusinessName -> 기업체 리스트 : ['포스코건설', '현대건설', ]
        # self.SearchPerson -> 담당자 리스트 : ['김웅곤', ]
        self.pushButton_3.clicked.connect(self.ReadGunseolList)
        self.pushButton_2.clicked.connect(self.DataCrawl)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    
    app.exec_()