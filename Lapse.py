import random
import json
import sys
import winsound
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer
import pygame
import os
import time


# Oyuncu adını al
oyuncu_adi = input("Lütfen isminizi girin: ").strip()

# Hikaye
Masal = f"""
Bir zamanlar, uzak diyarlarda dört temel gücün dengeyi sağladığı görkemli bir krallık vardı. 
Bu krallık, bilge bir hükümdar tarafından yönetiliyordu. 
Ancak zamanla krallığın üzerine karanlık gölgeler düştü. 
Salgın hastalıklar, savaş tehditleri, ekonomik krizler ve halkın memnuniyetsizliği büyümeye başladı. 
Hükümdarın önünde zorlu kararlar vardı. Vereceği her karar, krallığın kaderini belirleyecekti...

Krallığın güncel durumu: "Sağlık": 50; "Askeri": 50; "Ekonomi": 50; "Halk": 50.

Sayın {oyuncu_adi}, krallığın kaderi artık sizin ellerinizde!
"""

print(Masal)

# Oyunun temel boyutları
stats = {"Sağlık": 50, "Askeri": 50, "Ekonomi": 50, "Halk": 50}
oyun_geçmişi = []

# Soruları dosyadan oku
with open("sorular.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

random.shuffle(questions)

def play_game_over_sound():
    try:
        winsound.Beep(500, 500)
        winsound.Beep(400, 500)
    except Exception as e:
        print(f"Ses çalınırken hata oluştu: {e}")

def save_game_data(result):
    oyun_verisi = {
        "oyuncu": oyuncu_adi,
        "son_durum": stats,
        "oyun_sonucu": result,
        "tercihler": oyun_geçmişi
    }
    dosya_adi = f"{oyuncu_adi}.json"
    with open(dosya_adi, "w", encoding="utf-8") as file:
        json.dump(oyun_verisi, file, ensure_ascii=False, indent=4)
    print(f"Oyun verileri '{dosya_adi}' dosyasına kaydedildi!")


# Pygame başlatılması
pygame.mixer.init()

def play_music():
    music_path = "music/music.mp3"
    
    # Müzik dosyasının var olup olmadığını kontrol et
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Müzik sonsuz döngüde çalar
            print("Müzik çalmaya başladı.")
        except pygame.error as e:
            print(f"Pygame müzik yükleme hatası: {e}")
    else:
        print("Müzik dosyası bulunamadı!")


class KingdomGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_question = 0
        self.time_left = 30
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.ask_question()

        # Müzik çalmaya başla
        play_music()

    def initUI(self):
        self.setWindowTitle("Krallık Oyunu")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.label_soru = QLabel("Soru yükleniyor...")
        self.layout.addWidget(self.label_soru)
        
        self.label_timer = QLabel("Zaman: 10")
        self.layout.addWidget(self.label_timer)
        
        self.label_stats = QLabel(self.get_stats_text())
        self.layout.addWidget(self.label_stats)
        
        self.button_evet = QPushButton("Evet")
        self.button_evet.clicked.connect(lambda: self.answer_question("evet"))
        self.layout.addWidget(self.button_evet)
        
        self.button_hayir = QPushButton("Hayır")
        self.button_hayir.clicked.connect(lambda: self.answer_question("hayır"))
        self.layout.addWidget(self.button_hayir)
        
        self.setLayout(self.layout)

    def get_stats_text(self):
        return f"Sağlık: {stats['Sağlık']}  Askeri: {stats['Askeri']}  Ekonomi: {stats['Ekonomi']}  Halk: {stats['Halk']}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label_timer.setText(f"Zaman: {self.time_left}")
        else:
            self.timer.stop()
            QMessageBox.critical(self, "Zaman Doldu", "Zaman doldu! Oyunu kaybettin.")
            save_game_data("Kaybetti")
            sys.exit()
    
    def ask_question(self):
        if self.current_question < len(questions):
            self.time_left = 30
            self.label_timer.setText(f"Zaman: {self.time_left}")
            self.timer.start(1000)
            question = questions[self.current_question]
            self.label_soru.setText(question["soru"])
        else:
            QMessageBox.information(self, "Zafer", "Krallık gelişti, halk refah içinde! Oyunu kazandın.")
            fireworks_effect()
            save_game_data("Kazandı")
            sys.exit()

    def answer_question(self, user_answer):
        self.timer.stop()
        question = questions[self.current_question]
        etkiler = question[user_answer]
        oyun_geçmişi.append({"soru": question["soru"], "cevap": user_answer, "etkiler": etkiler})
        
        for key, value in etkiler.items():
            stats[key] += value
            stats[key] = max(0, stats[key])
        
        self.label_stats.setText(self.get_stats_text())
        self.current_question += 1
        self.check_game_over()
        self.ask_question()
    
    def check_game_over(self):
        if stats["Sağlık"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Salgın krallığı yok etti! Oyunu kaybettin.")
        elif stats["Askeri"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Düşmanlar ülkeyi ele geçirdi! Oyunu kaybettin.")
        elif stats["Ekonomi"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Krallık iflas etti! Oyunu kaybettin.")
        elif stats["Halk"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Halk isyan etti! Oyunu kaybettin.")
        else:
            return
        
        play_game_over_sound()
        save_game_data("Kaybetti")
        sys.exit()

class KingdomGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_question = 0
        self.time_left = 30
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.ask_question()

        # Müzik çalmaya başla
        play_music()

    def initUI(self):
        self.setWindowTitle("Krallık Oyunu")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.label_soru = QLabel("Soru yükleniyor...")
        self.layout.addWidget(self.label_soru)
        
        self.label_timer = QLabel("Zaman: 10")
        self.layout.addWidget(self.label_timer)
        
        self.label_stats = QLabel(self.get_stats_text())
        self.layout.addWidget(self.label_stats)
        
        self.button_evet = QPushButton("Evet")
        self.button_evet.clicked.connect(lambda: self.answer_question("evet"))
        self.layout.addWidget(self.button_evet)
        
        self.button_hayir = QPushButton("Hayır")
        self.button_hayir.clicked.connect(lambda: self.answer_question("hayır"))
        self.layout.addWidget(self.button_hayir)
        
        self.setLayout(self.layout)

    def get_stats_text(self):
        return f"Sağlık: {stats['Sağlık']}  Askeri: {stats['Askeri']}  Ekonomi: {stats['Ekonomi']}  Halk: {stats['Halk']}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label_timer.setText(f"Zaman: {self.time_left}")
        else:
            self.timer.stop()
            QMessageBox.critical(self, "Zaman Doldu", "Zaman doldu! Oyunu kaybettin.")
            save_game_data("Kaybetti")
            sys.exit()
    
    def ask_question(self):
        if self.current_question < len(questions):
            self.time_left = 30
            self.label_timer.setText(f"Zaman: {self.time_left}")
            self.timer.start(1000)
            question = questions[self.current_question]
            self.label_soru.setText(question["soru"])
        else:
            QMessageBox.information(self, "Zafer", "Krallık gelişti, halk refah içinde! Oyunu kazandın.")
            fireworks_effect()
            save_game_data("Kazandı")
            sys.exit()

    def answer_question(self, user_answer):
        self.timer.stop()
        question = questions[self.current_question]

        # Geçersiz cevap kontrolü
        if user_answer not in ['evet', 'hayır']:  # 'hayır' burada doğru yazılmalı
            QMessageBox.critical(self, "Hata", f"Geçersiz cevap: {user_answer}")
            return

        # JSON verisine bağlı olarak etkileri al
        etkiler = question.get(user_answer, {})
        if not etkiler:
            QMessageBox.critical(self, "Hata", "Bu cevap için geçerli etkiler bulunamadı!")
            return

        oyun_geçmişi.append({"soru": question["soru"], "cevap": user_answer, "etkiler": etkiler})

        # Etkileri işleme
        for key, value in etkiler.items():
            stats[key] += value
            stats[key] = max(0, stats[key])  # Statlar 0'ın altına düşmesin

        self.label_stats.setText(self.get_stats_text())
        self.current_question += 1
        self.check_game_over()
        self.ask_question()
    
    def check_game_over(self):
        if stats["Sağlık"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Salgın krallığı yok etti! Oyunu kaybettin.")
        elif stats["Askeri"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Düşmanlar ülkeyi ele geçirdi! Oyunu kaybettin.")
        elif stats["Ekonomi"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Krallık iflas etti! Oyunu kaybettin.")
        elif stats["Halk"] == 0:
            QMessageBox.critical(self, "Oyun Bitti", "Halk isyan etti! Oyunu kaybettin.")
        else:
            return

        # Oyun bittiğinde şarkıyı durdur
        pygame.mixer.music.stop()

        play_game_over_sound()
        save_game_data("Kaybetti")
        sys.exit()


# Oyunun sonucunu belirleme
def fireworks_effect():
    print("Havai fişekler patlıyor! 🎆🎇")
    # Oyunu kazanınca müziği kapat
    pygame.mixer.music.stop()

    for _ in range(5):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        .  *  .        ")
        print("      *   .   *   .    ")
        print("    .     *   *     .  ")
        print("  *   .   *  *   .  *  ")
        print("    .     *     .      ")
        print("      *     *   *      ")
        print("          |            ")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.2)


def answer_question(self, user_answer):
        self.timer.stop()
        question = questions[self.current_question]
        etkiler = question[user_answer]
        oyun_geçmişi.append({"soru": question["soru"], "cevap": user_answer, "etkiler": etkiler})
        
        for key, value in etkiler.items():
            stats[key] += value
            stats[key] = max(0, stats[key])
        
        self.label_stats.setText(self.get_stats_text())
        self.current_question += 1
        self.check_game_over()
        self.ask_question()

def check_game_over(self):
    if stats["Sağlık"] == 0:
        QMessageBox.critical(self, "Oyun Bitti", "Salgın krallığı yok etti! Oyunu kaybettin.")
    elif stats["Askeri"] == 0:
        QMessageBox.critical(self, "Oyun Bitti", "Düşmanlar ülkeyi ele geçirdi! Oyunu kaybettin.")
    elif stats["Ekonomi"] == 0:
        QMessageBox.critical(self, "Oyun Bitti", "Krallık iflas etti! Oyunu kaybettin.")
    elif stats["Halk"] == 0:
        QMessageBox.critical(self, "Oyun Bitti", "Halk isyan etti! Oyunu kaybettin.")
    else:
        return

    # Oyun bittiğinde şarkıyı durdur
    pygame.mixer.music.stop()

    play_game_over_sound()
    save_game_data("Kaybetti")
    sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = KingdomGame()
    game.show()
    sys.exit(app.exec_())