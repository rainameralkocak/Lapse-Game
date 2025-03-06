## Krallık Oyunu

Bu oyun, krallığın kaderini belirleyen kararlar almanızı gerektiren bir strateji oyunudur. Oyuncular, karşılarına çıkan sorulara verdikleri cevaplarla krallığın sağlık, askeri güç, ekonomi ve halk memnuniyeti gibi temel istatistiklerini etkiler. Amaç, dengeli ve sürdürülebilir bir yönetimle krallığı ayakta tutmak!

### İçindekiler
- Genel Bakış
- Özellikler
- Kurulum ve Gereksinimler
- Oyunun Çalıştırılması
- Oyun Kuralları ve Nasıl Oynanır?
- Dosya ve Veri Yönetimi
- Notlar ve İyileştirme Önerileri

### Genel Bakış
Bu Python/PyQt5 tabanlı oyun, oyunculara zaman sınırlamasıyla kritik kararlar alma deneyimi sunar. Verilen her karar, krallığın dört temel statüsünü (Sağlık, Askeri, Ekonomi, Halk) artırabilir ya da azaltabilir. Statülerden herhangi biri sıfıra düşerse oyun sona erer. 

### Özellikler
- **Hikaye Tabanlı Oynanış:** Oyuncular, kral rolünde olup hikaye bazlı sorulara cevap verir.
- **Zaman Sınırlı Kararlar:** Her soru için belirli bir süre içinde cevap verilmelidir.
- **Müzik ve Ses Efektleri:** Oyun sırasında arka plan müziği çalar, oyun bitişinde ses efekti eklenir.
- **Stat Takibi:** Krallığın sağlık, askeri güç, ekonomi ve halk memnuniyeti seviyeleri dinamik olarak güncellenir.
- **Oyun Verisi Kaydı:** Oyuncu adı, tercihleri ve oyun sonucu JSON formatında kaydedilir.

### Kurulum ve Gereksinimler
**Gereksinimler:**
- Python 3.11 veya üzeri
- PyQt5 (Grafik arayüz)
- Pygame (Müzik ve ses efektleri)
- winsound (Windows ses efektleri için)

**Python Kütüphaneleri:**
```bash
pip install pyqt5 pygame
```

**İşletim Sistemi Uyumluluğu:**
- Windows: Tüm özellikler kullanılabilir.
- Linux/macOS: winsound yerine alternatif ses modülleri kullanılabilir.

### Oyunun Çalıştırılması
1. **Python'u Kurun:** Python 3.11 yüklü değilse [Python resmi sitesi](https://www.python.org) üzerinden indirin.
2. **Proje Dosyalarını İndirin:**
   - `krallik_oyunu.py`: Ana oyun dosyası
   - `sorular.json`: Oyunda sorulacak sorular
   - `music/music.mp3`: Arka plan müziği
3. **Terminali Açın:** Kodun bulunduğu dizine geçin.
4. **Oyunu Başlatın:**
```bash
python krallik_oyunu.py
```

### Oyun Kuralları ve Nasıl Oynanır?
- **Oyuncu Adı:** Oyun başında oyuncu adı alınır.
- **Soru Akışı:** Sorular ekranda gösterilir ve "Evet" veya "Hayır" butonlarıyla cevap verilir.
- **Zaman Sınırı:** Her soruya 30 saniye içinde cevap verilmezse oyun kaybedilir.
- **Stat Değişimi:** Verilen cevaplar, JSON dosyasında tanımlanan etkilere göre krallık istatistiklerini değiştirir.
- **Oyun Sonu:**
  - Statlerden biri sıfıra düşerse oyun kaybedilir.
  - Tüm sorular başarıyla geçilirse krallık refaha ulaşır ve oyun kazanılır.

### Dosya ve Veri Yönetimi
- **Oyun Kaydı:** Her oyunun sonunda, oyuncunun ismi, kararları ve oyun sonucu `{oyuncu_adi}.json` formatında kaydedilir.
- **Skor Analizi:** Kayıtlı veriler daha sonra analiz edilebilir.

### Notlar ve İyileştirme Önerileri
- **Platform Desteği:** Windows dışındaki platformlarda `winsound` yerine `pygame.mixer.Sound` gibi alternatifler eklenebilir.
- **Soru Çeşitliliği:** `sorular.json` dosyasına yeni sorular ekleyerek oyun genişletilebilir.
- **Zorluk Seviyesi:** İleri seviyede zorluk modları eklenebilir (örn. daha kısa zaman limiti).

