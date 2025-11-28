# Profesyonel CV Oluşturucu (Python & Tkinter)

Bu proje, Python ve Tkinter kullanılarak geliştirilmiş, modern arayüze sahip bir **Masaüstü CV Hazırlama Uygulamasıdır**. 

Kullanıcı dostu arayüzü ile bilgilerinizi girmenizi, fotoğraf eklemenizi ve tek tıkla **Türkçe karakter uyumlu, profesyonel bir PDF** çıktısı almanızı sağlar.

![Ekran Görüntüsü](https://via.placeholder.com/800x500?text=Programin+Ekran+Goruntusunu+Buraya+Koy)
*(Buraya programın ekran görüntüsünü eklerseniz harika olur)*

## ✨ Özellikler

* **💾 Otomatik Kayıt:** Programı kapatsanız bile verileriniz (JSON formatında) saklanır, tekrar yazmak zorunda kalmazsınız.
* **🎨 Modern Arayüz:** `ttkbootstrap` ile geliştirilmiş Karanlık Mod (Dark Mode) tasarımı.
* **📝 Zengin Metin Editörü:** "Hakkımda" kısmında **Kalın**, *İtalik* yazabilir ve metni hizalayabilirsiniz (Sola, Ortaya, Sağa).
* **📄 PDF Çıktısı:** `FPDF2` kütüphanesi ile vektörel ve yüksek kaliteli çıktı.
* **🖼️ Fotoğraf Desteği:** Vesikalık fotoğrafınızı ekleyebilirsiniz.
* **🔗 Akıllı Linkler:** PDF üzerindeki LinkedIn ve Web Sitesi linkleri tıklanabilirdir.

## 🛠️ Kurulum (Geliştiriciler İçin)

Kaynak kodları çalıştırmak isterseniz:

1.  Repoyu klonlayın veya indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı başlatın:
    ```bash
    python cv_olustur.py
    ```

## 📦 EXE Olarak İndir (Kullanıcılar İçin)

Python kurmakla uğraşmadan, direkt programı indirip kullanmak için Releases kısmından exe dosyasını indirebilirsiniz.:


### ⚠️ Windows Defender Uyarısı Hakkında

Program open source olduğu ve geliştirici sertifikası ile imzalanmadığı için, Windows ilk açılışta **"Windows kişisel bilgisayarınızı korudu"** uyarısı verebilir.

> **Ek Bilgi > Yine de Çalıştır** seçeneğine tıklamanız yeterlidir.

---

Bu proje MIT Lisansı ile sunulmuştur. İstediğiniz gibi geliştirip kullanabilirsiniz.