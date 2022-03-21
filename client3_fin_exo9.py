from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        self.label = QLabel("hostname", self)
        self.text = QLineEdit(self)
        self.text.move(10, 30)
        self.label.move(10,10)
        self.label4 = QLabel("ip", self)
        self.text4 = QLineEdit(self)
        self.text4.move(10, 80)
        self.label4.move(10,60)
        self.label3 = QLabel("api_key", self)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 130)
        self.label3.move(10,110)
        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 180)
        self.button = QPushButton("Send", self)
        self.button.move(10, 220)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text.text()
        api_key = self.text4.text()
        ip = self.text3.text()


        if hostname == "" or api_key == "" or ip =="" :
            QMessageBox.about(self, "Error", "Please fill the field")
            
        else:
            res = self.__query(hostname,api_key,ip)
            if res:
                self.label2.setText(str(res))
                self.label2.adjustSize()
                print(res)
                latitude = res["latitude"]
                longitude = res["longitude"]
                QDesktopServices.openUrl(QUrl("https://www.openstreetmap.org/?mlat="+str(latitude)+"&mlon="+str(longitude)+"#map=12"))
                self.show()

    def __query(self, hostname,api_key,ip):
        url = "http://%s/ip/%s?key=%s" % (hostname,api_key,ip)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
