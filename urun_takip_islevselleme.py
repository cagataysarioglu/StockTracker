# HH   Hh   cCCCc     sSSSs
# HH   HH  CC   CC   SS   SS
# HHhHhHH  CC        SSSs
# HHHhHHH  CC          SSSs
# HH   HH  CC   CC  SS   SSs
# HH   Hh   CCCCC    SSSSSS
# ***********************************
# Haluk Çağatay Sarıoğlu

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from urun_takip import Ui_MainWindow
from hakkinda import Ui_Dialog
import sqlite3

Uygulama = QApplication(sys.argv)
ana_pencere = QMainWindow()
arayuz = Ui_MainWindow()
arayuz.setupUi(ana_pencere)
ana_pencere.show()

hakkinda_penceresi = QDialog()
arayuz_iki = Ui_Dialog()
arayuz_iki.setupUi(hakkinda_penceresi)

baglanti = sqlite3.connect("veritabani.db")
imlec = baglanti.cursor()
sorgu_tablo_olustur = ("CREATE TABLE IF NOT EXISTS Urunler(Kimlik INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                       "UrunTuru TEXT NOT NULL, UrunModeli TEXT NOT NULL, UrunAdi TEXT NOT NULL, UrunNu INTEGER "
                       "NOT NULL, UrunRengi TEXT NOT NULL, UrunAdedi INTEGER NOT NULL)")
imlec.execute(sorgu_tablo_olustur)
baglanti.commit()

def kayitSayisiVer():
    imlec.execute("SELECT COUNT(*) FROM Urunler")
    kayit_sayisi = imlec.fetchone()
    arayuz.lblKayitSayisi.setText(str(kayit_sayisi[0]))

    imlec.execute("SELECT SUM(UrunAdedi) FROM Urunler")
    toplam_urun = imlec.fetchone()
    arayuz.lblToplamUrunSayisi.setText(str(toplam_urun[0]))

def urunEkle():
    urun_turu = arayuz.cmbUrunTuru.currentText()
    urun_modeli = arayuz.cmbUrunModeli.currentText()
    urun_adi = arayuz.lneUrunAdi.text()
    urun_nu = arayuz.cmbUrunNu.currentText()
    urun_rengi = arayuz.cmbUrunRengi.currentText()
    urun_adedi = arayuz.spnUrunAdedi.value()

    if urun_turu and urun_modeli and urun_nu != 0:
        imlec.execute("INSERT INTO Urunler(UrunTuru, UrunModeli, UrunAdi, UrunNu, UrunRengi, UrunAdedi) VALUES"
                      "(?, ?, ?, ?, ?, ?)", (urun_turu, urun_modeli, urun_adi, urun_nu, urun_rengi, urun_adedi))
        baglanti.commit()
        listeyeYansit()
        arayuz.durumcubugu.showMessage("Ürün kayıt işlemi başarıyla gerçekleşti.", 7000)

def listeyeYansit():
    arayuz.tblUrunTablosu.clear()
    arayuz.tblUrunTablosu.setHorizontalHeaderLabels(("Nu.", "Ürün Türü", "Ürün Modeli", "Ürün Adı", "Ürün Nu.",
                                                     "Ürün Rengi", "Ürün Adedi"))
    arayuz.tblUrunTablosu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    imlec.execute("SELECT * FROM Urunler")
    for satir_indisi, satir_verisi in enumerate(imlec):
        for sutun_indisi, sutun_verisi in enumerate(satir_verisi):
            arayuz.tblUrunTablosu.setItem(satir_indisi, sutun_indisi, QTableWidgetItem(str(sutun_verisi)))
    arayuz.cmbUrunTuru.setCurrentIndex(-1)
    arayuz.cmbUrunModeli.setCurrentIndex(-1)
    arayuz.lneUrunAdi.clear()
    arayuz.cmbUrunNu.setCurrentIndex(-1)
    arayuz.cmbUrunRengi.setCurrentIndex(-1)
    arayuz.spnUrunAdedi.setValue(0)

    kayitSayisiVer()

listeyeYansit()

def urunSil():
    yanit = QMessageBox.question(ana_pencere, "Silme", "Silmek mi istiyorunuz?", QMessageBox.Yes | QMessageBox.No)
    if yanit == QMessageBox.Yes:
        secili_urun = arayuz.tblUrunTablosu.selectedItems()
        silinecek_urun = secili_urun[3].text()
        try:
            imlec.execute("DELETE FROM Urunler WHERE UrunAdi='%s'" % silinecek_urun)
            baglanti.commit()
            listeyeYansit()
            arayuz.durumcubugu.showMessage("Kayıt silme işlemi başarıyla gerçekleşti.", 7000)
        except Exception as hata:
            arayuz.durumcubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
    else:
        arayuz.durumcubugu.showMessage("Silme işlemi iptal edildi.", 7000)

def doldur():
    secili_satir = arayuz.tblUrunTablosu.selectedItems()
    if len(secili_satir) != 0:
        arayuz.cmbUrunTuru.setCurrentText(secili_satir[1].text())
        arayuz.cmbUrunModeli.setCurrentText(secili_satir[2].text())
        arayuz.lneUrunAdi.setText(secili_satir[3].text())
        arayuz.cmbUrunNu.setCurrentText(secili_satir[4].text())
        arayuz.cmbUrunRengi.setCurrentText(secili_satir[5].text())
        arayuz.spnUrunAdedi.setValue(int(secili_satir[6].text()))
    else:
        arayuz.durumcubugu.showMessage("Seçilen hücre veya satır boştur.", 3000)

def urunGuncelle():
    yanit = QMessageBox.question(ana_pencere, "Güncelleme", "Kayıt güncellensin mi?", QMessageBox.Yes | QMessageBox.No)
    if yanit == QMessageBox.Yes:
        try:
            secili_urun = arayuz.tblUrunTablosu.selectedItems()
            nu = int(secili_urun[0].text())
            urun_turu = arayuz.cmbUrunTuru.currentText()
            urun_modeli = arayuz.cmbUrunModeli.currentText()
            urun_adi = arayuz.lneUrunAdi.text()
            urun_nu = arayuz.cmbUrunNu.currentText()
            urun_rengi = arayuz.cmbUrunRengi.currentText()
            urun_adedi = arayuz.spnUrunAdedi.value()

            imlec.execute("UPDATE Urunler SET UrunTuru=?, UrunModeli=?, UrunAdi=?, UrunNu=?, UrunRengi=?, UrunAdedi=? "
                          "WHERE Kimlik=?", (urun_turu, urun_modeli, urun_adi, urun_nu, urun_rengi, urun_adedi, nu))
            baglanti.commit()
            listeyeYansit()
            arayuz.durumcubugu.showMessage("Güncelleme işlemi başarıyla gerçekleşti.", 7000)
        except Exception as hata:
            arayuz.durumcubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
    else:
        arayuz.durumcubugu.showMessage("Güncelleme işlemi iptal edildi.", 7000)

def urunAra():
    aranan = arayuz.lneAra.text()
    try:
        imlec.execute("SELECT * FROM Urunler WHERE UrunTuru=? OR UrunModeli=? OR UrunAdi=? OR UrunNu=? OR UrunRengi=?",
                      (aranan, aranan, aranan, aranan, aranan))
        baglanti.commit()
        arayuz.durumcubugu.showMessage("Arama sonuçları bulundu ve gösterildi.", 5000)
    except Exception as hata:
        arayuz.durumcubugu.showMessage(str(hata) + "adlı bir hata ile karşılaşıldı.", 5000)
    arayuz.tblUrunTablosu.clear()
    for satir_indisi, satir_verisi in enumerate(imlec):
        for sutun_indisi, sutun_verisi in enumerate(satir_verisi):
            arayuz.tblUrunTablosu.setItem(satir_indisi, sutun_indisi, QTableWidgetItem(str(sutun_verisi)))

def temizle():
    arayuz.lneAra.clear()
    listeyeYansit()

def uygulamadanCik():
    yanit = QMessageBox.question(ana_pencere, "Çıkış", "Çıkmak istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
    if yanit == QMessageBox.Yes:
        baglanti.close()
        sys.exit(Uygulama.exec_())
    else:
        ana_pencere.show()

def hakkinda():
    hakkinda_penceresi.show()

arayuz.tblUrunTablosu.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
arayuz.dgmEkle.clicked.connect(urunEkle)
arayuz.dgmSil.clicked.connect(urunSil)
arayuz.tblUrunTablosu.itemSelectionChanged.connect(doldur)
arayuz.dgmGuncelle.clicked.connect(urunGuncelle)
arayuz.dgmAra.clicked.connect(urunAra)
arayuz.dgmTemizle.clicked.connect(temizle)
arayuz.dgmCik.clicked.connect(uygulamadanCik)
arayuz.menuHakkinda.triggered.connect(hakkinda)

sys.exit(Uygulama.exec_())
