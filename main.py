from abc import ABC, abstractmethod
from time import sleep
from random import choice
import threading

# Trafik Işığı Durumları
TRAFIK_DURUM = ["Kırmızı", "Sarı", "Yeşil"]

class TrafikIsigi:
    def __init__(self, konum):
        self.konum = konum  # Trafik ışığının bulunduğu yer
        self.durum = "Kırmızı"  # Trafik ışığının başlangıç durumu
        self.gozlemciler = []  # Trafik ışığını gözlemleyenlerin listesi

    def gozlemci_ekle(self, gozlemci):
        self.gozlemciler.append(gozlemci)  # Yeni bir gözlemci ekle

    def gozlemci_cikar(self, gozlemci):
        self.gozlemciler.remove(gozlemci)  # Mevcut bir gözlemciyi çıkar

    def gozlemcilere_bildirim(self):
        for gozlemci in self.gozlemciler:
            gozlemci.guncelle(self.konum, self.durum)  # Gözlemcilere bildirim gönder

    def durum_degistir(self, durum):
        self.durum = durum  # Trafik ışığının durumunu değiştir
        self.gozlemcilere_bildirim()  # Gözlemcilere yeni durumu bildir

class TrafikGozlemcisi:
    def __init__(self, ad):
        self.ad = ad  # Gözlemcinin adı

    def guncelle(self, konum, durum):
        print(f"{self.ad}, {konum} konumundan güncelleme aldı: Trafik ışığı {durum}")  # Güncelleme bildirimi

class TrafikYonetimStratejisi(ABC):
    @abstractmethod
    def trafik_yonet(self, trafik_isigi):
        pass

class NormalTrafikStratejisi(TrafikYonetimStratejisi):
    def trafik_yonet(self, trafik_isigi):
        for durum in TRAFIK_DURUM:
            trafik_isigi.durum_degistir(durum)
            sleep(1)

class YogunTrafikStratejisi(TrafikYonetimStratejisi):
    def trafik_yonet(self, trafik_isigi):
        for durum in ["Yeşil", "Sarı", "Kırmızı", "Yeşil", "Sarı", "Kırmızı"]:
            trafik_isigi.durum_degistir(durum)
            sleep(1)

class AcilDurumYonetimMerkezi:
    _instance = None  # Singleton örneği

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AcilDurumYonetimMerkezi, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.acil_durum_araclari = []  # Acil durum araçlarının listesi
            self.initialized = True

    def arac_ekle(self, arac):
        self.acil_durum_araclari.append(arac)  # Yeni acil durum aracı ekle
        print(f"{arac} acil durum filosuna eklendi")

    def arac_gonder(self, konum):
        if self.acil_durum_araclari:
            arac = self.acil_durum_araclari.pop(0)  # Mevcut araçlardan birini gönder
            print(f"{arac}, {konum} konumuna gönderiliyor")
        else:
            print("Acil durum aracı yok")

class VeriIzleme:
    def __init__(self):
        self.trafik_isiklari = []

    def trafik_isigi_ekle(self, trafik_isigi):
        self.trafik_isiklari.append(trafik_isigi)

    def durum_guncelle(self):
        for trafik_isigi in self.trafik_isiklari:
            yeni_durum = choice(TRAFIK_DURUM)
            trafik_isigi.durum_degistir(yeni_durum)
            sleep(2)

class BildirimSistemi:
    def __init__(self):
        self.uyarilar = []

    def yeni_uyari(self, mesaj):
        self.uyarilar.append(mesaj)
        print(f"UYARI: {mesaj}")

class RaporlamaSistemi:
    def __init__(self):
        self.raporlar = []

    def rapor_ekle(self, rapor):
        self.raporlar.append(rapor)

    def raporlari_goster(self):
        for rapor in self.raporlar:
            print(f"RAPOR: {rapor}")

class YonetimOnerileriSistemi:
    def __init__(self):
        self.oneriler = []

    def yeni_oneri(self, oneri):
        self.oneriler.append(oneri)

    def onerileri_goster(self):
        for oneri in self.oneriler:
            print(f"ÖNERİ: {oneri}")

class MobilUygulama:
    def __init__(self):
        print("Mobil Uygulama Başlatıldı")

    def kullanici_giris(self, kullanici, sifre):
        print(f"Kullanıcı {kullanici} giriş yaptı")

class WebUygulama:
    def __init__(self):
        print("Web Uygulama Başlatıldı")

    def kullanici_giris(self, kullanici, sifre):
        print(f"Kullanıcı {kullanici} giriş yaptı")

def main():
    # Trafik ışıklarını oluştur
    ana_cadde_isigi = TrafikIsigi("Ana Cadde")
    ikinci_cadde_isigi = TrafikIsigi("İkinci Cadde")

    # Gözlemcileri oluştur
    arac = TrafikGozlemcisi("Araç")
    yaya = TrafikGozlemcisi("Yaya")

    # Gözlemcileri trafik ışıklarına ekle
    ana_cadde_isigi.gozlemci_ekle(arac)
    ana_cadde_isigi.gozlemci_ekle(yaya)
    ikinci_cadde_isigi.gozlemci_ekle(arac)

    # Trafik yönetimi stratejileri oluştur
    normal_trafik = NormalTrafikStratejisi()
    yogun_trafik = YogunTrafikStratejisi()

    # Trafik ışıklarına stratejileri uygula
    print("Normal trafik yönetimi:")
    threading.Thread(target=normal_trafik.trafik_yonet, args=(ana_cadde_isigi,)).start()

    print("\nYoğun trafik yönetimi:")
    threading.Thread(target=yogun_trafik.trafik_yonet, args=(ikinci_cadde_isigi,)).start()

    # Singleton acil durum yönetim merkezi
    acil_merkez = AcilDurumYonetimMerkezi()
    acil_merkez.arac_ekle("Ambulans")
    acil_merkez.arac_ekle("İtfaiye Aracı")

    # Acil durum araçlarını gönder
    print("\nAcil durum araç gönderimi:")
    acil_merkez.arac_gonder("Ana Cadde")
    acil_merkez.arac_gonder("İkinci Cadde")
    acil_merkez.arac_gonder("Üçüncü Cadde")

    # Veri izleme ve bildirim sistemi
    veri_izleme = VeriIzleme()
    veri_izleme.trafik_isigi_ekle(ana_cadde_isigi)
    veri_izleme.trafik_isigi_ekle(ikinci_cadde_isigi)

    bildirim_sistemi = BildirimSistemi()

    # Veri izlemeyi başlat
    threading.Thread(target=veri_izleme.durum_guncelle).start()

    # Raporlama ve öneri sistemi
    raporlama_sistemi = RaporlamaSistemi()
    yonetim_onerileri_sistemi = YonetimOnerileriSistemi()

    # Rapor ekleme
    raporlama_sistemi.rapor_ekle("Günlük trafik raporu")
    raporlama_sistemi.rapor_ekle("Haftalık trafik raporu")

    # Öneri ekleme
    yonetim_onerileri_sistemi.yeni_oneri("Ana caddede trafik yoğunluğu artıyor, yeşil ışık süreleri artırılmalı.")
    yonetim_onerileri_sistemi.yeni_oneri("Yoğun saatlerde ikinci cadde için alternatif yollar önerilmeli.")

    # Raporları ve önerileri göster
    print("\nRaporlar:")
    raporlama_sistemi.raporlari_goster()

    print("\nYönetim Önerileri:")
    yonetim_onerileri_sistemi.onerileri_goster()

    # Mobil ve web uygulaması simülasyonu
    mobil_uygulama = MobilUygulama()
    mobil_uygulama.kullanici_giris("user1", "password123")

    web_uygulama = WebUygulama()
    web_uygulama.kullanici_giris("user1", "password123")

if __name__ == "__main__":
    main()
