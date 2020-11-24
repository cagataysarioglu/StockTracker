import sys 
from PyQt5 import QtWidgets, QtGui, QtCore
from ustu import Ui_AnaPencere # Bu, Qt Designer'da oluşturulan başka bir dosyadır.

class Uygulama(QtWidgets.QMainWindow):
    def __init__(self):
        super(Uygulama, self).__init__()

        self.arayuz = Ui_AnaPencere()
        self.arayuz.setupUi(self)

        self.urunleriYukle()
        self.arayuz.dgmEkle.clicked.connect(self.urunEkle)
        self.arayuz.dgmDuzenle.clicked.connect(self.urunDuzenle)
        self.arayuz.dgmSil.clicked.connect(self.urunSil)
        self.arayuz.tabloStok.doubleClicked.connect(self.ciftTiklanan)
        self.arayuz.dgmKapat.clicked.connect(self.uygKapat)

    def urunleriYukle(self):
        urunler = [
            {"kimlik": "6789", "ad": "aaa", "fiyat": 7000},
            {"kimlik": "2345", "ad": "bbb", "fiyat": 7000},
            {"kimlik": "1234", "ad": "ccc", "fiyat": 7000},
            {"kimlik": "4567", "ad": "ddd", "fiyat": 7000}
        ]

        self.arayuz.tabloStok.setRowCount(len(urunler))
        self.arayuz.tabloStok.setColumnCount(3)
        self.arayuz.tabloStok.setHorizontalHeaderLabels(("Kimlik", "Ad", "Fiyat"))

        satirIndisi = 0
        for urun in urunler:
            self.arayuz.tabloStok.setItem(satirIndisi, 0, QtWidgets.QTableWidgetItem(str(urun["kimlik"])))
            self.arayuz.tabloStok.setItem(satirIndisi, 1, QtWidgets.QTableWidgetItem(urun["ad"]))
            self.arayuz.tabloStok.setItem(satirIndisi, 2, QtWidgets.QTableWidgetItem(str(urun["fiyat"])))
            satirIndisi += 1

    def urunEkle(self):
        kimlik = self.arayuz.grdUrunKimlik.text()
        ad = self.arayuz.grdUrunAdi.text()
        fiyat = self.arayuz.grdUrunFiyati.text()

        if kimlik and ad and fiyat is not None:
            satirSayaci = self.arayuz.tabloStok.rowCount()
            self.arayuz.tabloStok.insertRow(satirSayaci)
            self.arayuz.tabloStok.setItem(satirSayaci, 0, QtWidgets.QTableWidgetItem(kimlik))
            self.arayuz.tabloStok.setItem(satirSayaci, 1, QtWidgets.QTableWidgetItem(ad))
            self.arayuz.tabloStok.setItem(satirSayaci, 2, QtWidgets.QTableWidgetItem(fiyat))

    def urunDuzenle(self):
        self.arayuz.tabloStok.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)

    def urunSil(self):
        satir = self.arayuz.tabloStok.currentRow()
        soru = QtWidgets.QMessageBox.question(self, "Kaldır", "Seçtiğiniz ürünü silmek istiyor musunuz?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if soru == QtWidgets.QMessageBox.Yes:
            self.arayuz.tabloStok.removeRow(satir)

    def ciftTiklanan(self):
        self.arayuz.tabloStok.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def uygKapat(self):
        quit()

def uygulama():
    uyg = QtWidgets.QApplication(sys.argv)
    pencere = Uygulama()
    pencere.setWindowTitle("Ürün Stoğu Takip Uygulaması")
    pencere.show()
    sys.exit(uyg.exec_())
uygulama()
