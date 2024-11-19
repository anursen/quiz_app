import json
import random
import time
import hashlib
import os
from datetime import datetime

class ExamApp:
    def __init__(self):
        self.current_user = None
        self.remaining_time = 600  # 10 dakika = 600 saniye
        self.create_required_files()

    def create_required_files(self):
        """Gerekli dosya ve klasörleri oluşturur."""
        try:
            # Klasörleri oluştur
            folders = ['user', 'questions', 'result', 'admin']
            for folder in folders:
                if not os.path.exists(folder):
                    os.makedirs(folder)

            # Varsayılan kullanıcı dosyasını oluştur
            if not os.path.exists('user/users.json'):
                admin_user = {
                    "admin": {
                        "name": "admin",
                        "surname": "admin",
                        "password": self.hash_password("12345"),
                        "exam_count": 0
                    }
                }
                with open('user/users.json', 'w') as f:
                    json.dump(admin_user, f, indent=4)

            # Örnek soru dosyalarını oluştur
            self.create_sample_questions()
        except Exception as e:
            print(f"Hata: Dosya oluşturma sırasında bir problem oluştu: {e}")

    def create_sample_questions(self):
        """Örnek soruları oluşturur."""
        questions = {
            "section1": [
                {"question": "Python bir programlama dilidir.", "answer": True, "points": 5} for _ in range(20)
            ],
            "section2": [
                {
                    "question": f"Soru {i}",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "points": 5
                } for i in range(1, 21)
            ],
            "section3": [
                {
                    "question": f"Çoklu seçim soru {i}",
                    "options": ["A", "B", "C", "D"],
                    "correct_answers": ["A", "B"],
                    "points": 10
                } for i in range(1, 21)
            ],
            "section4": [
                {
                    "question": f"Sıralama sorusu {i}",
                    "options": ["1", "2", "3", "4"],
                    "correct_order": ["1", "2", "3", "4"],
                    "points": 5
                } for i in range(1, 21)
            ]
        }
        
        if not os.path.exists('questions/questions.json'):
            with open('questions/questions.json', 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=4, ensure_ascii=False)

    def hash_password(self, password):
        """Şifreyi güvenli bir şekilde hashler."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_or_register(self):
        """Kullanıcı girişi veya kayıt işlemini gerçekleştirir."""
        try:
            print("\n=== Sınav Sistemine Hoş Geldiniz ===")
            print("1. Giriş Yap")
            print("2. Kayıt Ol")
            choice = input("Seçiminiz (1/2): ")

            if choice == "1":
                return self.login()
            elif choice == "2":
                return self.register()
            else:
                print("Geçersiz seçim!")
                return False
        except Exception as e:
            print(f"Hata: Giriş işlemi sırasında bir problem oluştu: {e}")
            return False

    def login(self):
        """Kullanıcı girişi yapar."""
        try:
            username = input("Kullanıcı adı: ")
            password = input("Şifre: ")

            with open('user/users.json', 'r') as f:
                users = json.load(f)

            if username in users and users[username]["password"] == self.hash_password(password):
                self.current_user = {
                    "username": username,
                    "name": users[username]["name"],
                    "surname": users[username]["surname"],
                    "exam_count": users[username]["exam_count"]
                }
                print(f"\nHoş geldiniz, {self.current_user['name']} {self.current_user['surname']}!")
                return True
            else:
                print("Hatalı kullanıcı adı veya şifre!")
                return False
        except Exception as e:
            print(f"Hata: Giriş yapılırken bir problem oluştu: {e}")
            return False
    def register(self):
        """Yeni kullanıcı kaydı oluşturur."""
        try:
            print("\n=== Yeni Kullanıcı Kaydı ===")
            username = input("Kullanıcı adı: ")
            name = input("Ad: ")
            surname = input("Soyad: ")
            password = input("Şifre: ")

        # Dosyanın boş olup olmadığını kontrol et
            if os.path.exists('user/users.json'):
                with open('user/users.json', 'r') as f:
                    try:
                       users = json.load(f)
                    except json.JSONDecodeError:
                       users = {}  # Boşsa yeni bir dictionary oluştur
            else:
                users = {}

            if username in users:
                print("Bu kullanıcı adı zaten kullanımda!")
                return False

            users[username] = {
                "name": name,
                "surname": surname,
                "password": self.hash_password(password),
                "exam_count": 0
            }

            with open('user/users.json', 'w') as f:
               json.dump(users, f, indent=4)

            self.current_user = {
                "username": username,
                "name": name,
                "surname": surname,
                "exam_count": 0
            }
            print("Kayıt başarıyla tamamlandı!")
            return True
        except Exception as e:
            print(f"Hata: Kayıt işlemi sırasında bir problem oluştu: {e}")
            return False
            
    
    """
    def register(self):
        #Yeni kullanıcı kaydı oluşturur.
        try:
            print("\n=== Yeni Kullanıcı Kaydı ===")
            username = input("Kullanıcı adı: ")
            name = input("Ad: ")
            surname = input("Soyad: ")
            password = input("Şifre: ")

            with open('user/users.json', 'r') as f:
                users = json.load(f)

            if username in users:
                print("Bu kullanıcı adı zaten kullanımda!")
                return False

            users[username] = {
                "name": name,
                "surname": surname,
                "password": self.hash_password(password),
                "exam_count": 0
            }

            with open('user/users.json', 'w') as f:
                json.dump(users, f, indent=4)

            self.current_user = {
                "username": username,
                "name": name,
                "surname": surname,
                "exam_count": 0
            }
            print("Kayıt başarıyla tamamlandı!")
            return True
        except Exception as e:
            print(f"Hata: Kayıt işlemi sırasında bir problem oluştu: {e}")
            return False
"""
    def start_exam(self):
        """Sınavı başlatır ve yönetir."""
        try:
            if self.current_user["exam_count"] >= 2:
                print("Maksimum sınav hakkınızı kullandınız!")
                return

            print("\n=== Sınav Başlıyor ===")
            print("Toplam süre: 10 dakika")
            print("Her bölümden rastgele sorular gelecektir.")
            input("Başlamak için ENTER'a basın...")

            # Soruları yükle
            with open('questions/questions.json', 'r', encoding='utf-8') as f:
                all_questions = json.load(f)

            # Her sectiondan rastgele sorular seç
            selected_questions = []
            for section in ["section1", "section2", "section3", "section4"]:
                section_questions = random.sample(all_questions[section], 2)
                for q in section_questions:
                    q["section"] = section
                selected_questions.extend(section_questions)

            random.shuffle(selected_questions)
            
            answers = []
            start_time = time.time()
            current_question = 0

            while current_question < len(selected_questions):
                remaining_time = 600 - int(time.time() - start_time)
                
                if remaining_time <= 0:
                    print("\nSüre doldu!")
                    break
                
                if remaining_time <= 60:
                    print("\n!!! SON 1 DAKİKA !!!")

                question = selected_questions[current_question]
                print(f"\nSoru {current_question + 1}/10 (Kalan süre: {remaining_time//60} dakika)")
                
                if question["section"] == "section1":
                    answer = self.ask_true_false_question(question)
                elif question["section"] == "section2":
                    answer = self.ask_multiple_choice_question(question)
                elif question["section"] == "section3":
                    answer = self.ask_multiple_answer_question(question)
                else:
                    answer = self.ask_ordering_question(question)

                answers.append({
                    "question": question,
                    "answer": answer
                })

                print("\n1. Sonraki soru")
                print("2. Önceki soru")
                choice = input("Seçiminiz (1/2): ")

                if choice == "2" and current_question > 0:
                    current_question -= 1
                else:
                    current_question += 1

            self.calculate_and_save_results(answers)

        except Exception as e:
            print(f"Hata: Sınav sırasında bir problem oluştu: {e}")

    def ask_true_false_question(self, question):
        """Doğru/Yanlış sorusu sorar."""
        print(f"\nSoru: {question['question']}")
        print("1. Doğru")
        print("2. Yanlış")
        while True:
            try:
                answer = input("Cevabınız (1/2): ")
                return answer == "1"
            except:
                print("Geçersiz cevap! Tekrar deneyin.")

    def ask_multiple_choice_question(self, question):
        """Çoktan seçmeli soru sorar."""
        print(f"\nSoru: {question['question']}")
        for i, option in enumerate(question['options']):
            print(f"{i+1}. {option}")
        while True:
            try:
                answer = input("Cevabınız (1-4): ")
                return question['options'][int(answer)-1]
            except:
                print("Geçersiz cevap! Tekrar deneyin.")

    def ask_multiple_answer_question(self, question):
        """İki doğru cevaplı soru sorar."""
        print(f"\nSoru: {question['question']}")
        for i, option in enumerate(question['options']):
            print(f"{i+1}. {option}")
        while True:
            try:
                print("İki cevap seçin (örn: 1,2)")
                answers = input("Cevaplarınız: ").split(',')
                return [question['options'][int(a)-1] for a in answers]
            except:
                print("Geçersiz cevap! Tekrar deneyin.")

    def ask_ordering_question(self, question):
        """Sıralama sorusu sorar."""
        print(f"\nSoru: {question['question']}")
        options = question['options'].copy()
        random.shuffle(options)
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        while True:
            try:
                print("Sıralamayı girin (örn: 1,2,3,4)")
                answers = input("Sıralama: ").split(',')
                return [options[int(i)-1] for i in answers]
            except:
                print("Geçersiz cevap! Tekrar deneyin.")

    def calculate_and_save_results(self, answers):
        """Sınav sonuçlarını hesaplar ve kaydeder."""
        try:
            results = {
                "section1": {"correct": 0, "total": 0, "points": 0},
                "section2": {"correct": 0, "total": 0, "points": 0},
                "section3": {"correct": 0, "total": 0, "points": 0},
                "section4": {"correct": 0, "total": 0, "points": 0}
            }

            for ans in answers:
                question = ans["question"]
                section = question["section"]
                results[section]["total"] += 1

                if section == "section1":
                    if ans["answer"] == question["answer"]:
                        results[section]["correct"] += 1
                        results[section]["points"] += question["points"]
                elif section == "section2":
                    if ans["answer"] == question["correct_answer"]:
                        results[section]["correct"] += 1
                        results[section]["points"] += question["points"]
                elif section == "section3":
                    if sorted(ans["answer"]) == sorted(question["correct_answers"]):
                        results[section]["correct"] += 1
                        results[section]["points"] += question["points"]
                else:  # section4
                    if ans["answer"] == question["correct_order"]:
                        results[section]["correct"] += 1
                        results[section]["points"] += question["points"]

            total_points = sum(section["points"] for section in results.values())
            max_points = sum(results[section]["total"] * (10 if section == "section3" else 5) 
                           for section in results.keys())
            percentage = (total_points / max_points) * 100

            # Sonuçları kaydet
            result_data = {
                "user": self.current_user["username"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": results,
                "total_points": total_points,
                "percentage": percentage,
                "passed": percentage >= 75
            }

            results_file = f"result/{self.current_user['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(result_data, f, indent=4)

            # Kullanıcının sınav sayısını güncelle
            with open('user/users.json', 'r') as f:
                users = json.load(f)
            users[self.current_user["username"]]["exam_count"] += 1
            with open('user/users.json', 'w') as f:
                json.dump(users, f, indent=4)

            self.display_results(result_data)

        except Exception as e:
            print(f"Hata: Sonuçlar hesaplanırken bir problem oluştu: {e}")

    def display_results(self, results):
        """Sınav sonuçlarını gösterir."""
        print("\n=== SINAV SONUÇLARI ===")
        for section, data in results["results"].items():
            print(f"\n{section.upper()}:")
            print(f"Doğru: {data['correct']}/{data['total']}")
            print(f"Puan: {data['points']}")

        print(f"\nToplam Puan: {results['total_points']}")
        print(f"Başarı Yüzdesi: {results['percentage']:.2f}%")
        print(f"Sonuç: {'BAŞARILI' if results['passed'] else 'BAŞARISIZ'}")
        def admin_menu(self):
         """Admin menüsünü gösterir ve yönetir."""
        try:
            while True:
                print("\n=== Admin Paneli ===")
                print("1. Kullanıcı Listesi")
                print("2. Sınav Sonuçlarını Görüntüle")
                print("3. Şifrelenmiş Kullanıcı Bilgileri")
                print("4. Çıkış")
                
                choice = input("Seçiminiz: ")
                
                if choice == "1":
                    self.display_user_list()
                elif choice == "2":
                    self.display_exam_results()
                elif choice == "3":
                    self.display_encrypted_passwords()
                elif choice == "4":
                    break
                else:
                    print("Geçersiz seçim!")

        except Exception as e:
            print(f"Hata: Admin menüsünde bir problem oluştu: {e}")

    def display_user_list(self):
        """Kayıtlı kullanıcıların listesini gösterir."""
        try:
            with open('user/users.json', 'r') as f:
                users = json.load(f)
            
            print("\n=== Kullanıcı Listesi ===")
            for i, (username, data) in enumerate(users.items(), 1):
                if username != "admin":
                    print(f"{i}. {data['name']} {data['surname']} ({username})")
                    print(f"   Sınav Sayısı: {data['exam_count']}")
                    print("-" * 30)

        except Exception as e:
            print(f"Hata: Kullanıcı listesi görüntülenirken bir problem oluştu: {e}")

    def view_exam_results(self):
          #Sınav sonuçlarını görüntüler.
        try:
           # Sınav sonuçları dosyasını kontrol et
            if os.path.exists('exam_results.json'):
                with open('exam_results.json', 'r') as f:
                    try:
                       results = json.load(f)
                    except json.JSONDecodeError:
                       results = {}  # Dosya bozuksa boş bir dictionary oluştur
            else:
                results = {}

            if not results:
                print("Henüz hiçbir sınav sonucu kaydedilmemiş.")
                return

            # Admin olup olmadığını kontrol et
            is_admin = self.current_user.get("username") == "admin"

            if is_admin:
            # Admin tüm sınav sonuçlarını ve katılımcıları görebilir
                print("\n=== Tüm Sınav Sonuçları ===")
                for username, exams in results.items():
                    print(f"\nKullanıcı: {username}")
                    for exam in exams:
                        print(f"  Sınav: {exam['exam_name']}, Sonuç: {exam['score']}")
            else:
            # Normal kullanıcı sadece kendi sınav sonuçlarını görebilir
                username = self.current_user.get("username")
                if username in results:
                    print(f"\n=== {username} Kullanıcısının Sınav Sonuçları ===")
                    for exam in results[username]:
                        print(f"Sınav: {exam['exam_name']}, Sonuç: {exam['score']}")
                else:
                    print("Henüz sınav sonuçlarınız bulunmuyor.")
        except Exception as e:
            print(f"Hata: Sınav sonuçları görüntülenirken bir problem oluştu: {e}")

    """
    def display_exam_results(self):
      #Seçili kullanıcının sınav sonuçlarını gösterir.
        try:
            user_results = []
            for filename in os.listdir('result'):
                if filename.endswith('.json'):
                    with open(f'result/{filename}', 'r') as f:
                        result = json.load(f)
                        user_results.append({
                            'filename': filename,
                            'user': result['user'],
                            'date': result['date']
                        })

            if not user_results:
                print("Henüz hiç sınav sonucu bulunmuyor.")
                return

            print("\n=== Sınav Sonuçları ===")
            for i, result in enumerate(user_results, 1):
                print(f"{i}. {result['user']} - {result['date']}")

            choice = input("\nGörüntülemek istediğiniz sonucun numarasını girin: ")
            try:
                selected = user_results[int(choice)-1]
                with open(f"result/{selected['filename']}", 'r') as f:
                    result_data = json.load(f)
                self.display_results(result_data)
            except:
                print("Geçersiz seçim!")

        except Exception as e:
            print(f"Hata: Sınav sonuçları görüntülenirken bir problem oluştu: {e}")
        """       
    def display_encrypted_passwords(self):
        """Şifrelenmiş kullanıcı bilgilerini gösterir."""
        try:
            with open('user/users.json', 'r') as f:
                users = json.load(f)
            
            print("\n=== Şifrelenmiş Kullanıcı Bilgileri ===")
            for username, data in users.items():
                if username != "admin":
                    print(f"Kullanıcı: {username}")
                    print(f"Ad Soyad: {data['name']} {data['surname']}")
                    print(f"Şifre Hash: {data['password']}")
                    print("-" * 50)

        except Exception as e:
            print(f"Hata: Şifrelenmiş bilgiler görüntülenirken bir problem oluştu: {e}")

    def main_menu(self):
        """Ana menüyü gösterir ve program akışını yönetir."""
        try:
            while True:
                if not self.current_user:
                    if not self.login_or_register():
                        continue

                if self.current_user["username"] == "admin":
                    self.admin_menu()
                    self.current_user = None
                    continue

                print("\n=== Ana Menü ===")
                print(f"Kullanıcı: {self.current_user['name']} {self.current_user['surname']}")
                print(f"Kalan Sınav Hakkı: {2 - self.current_user['exam_count']}")
                print("\n1. Sınava Başla")
                print("2. Önceki Sınav Sonuçlarım")
                print("3. Çıkış")

                choice = input("Seçiminiz: ")

                if choice == "1":
                    if self.current_user["exam_count"] < 2:
                        self.start_exam()
                    else:
                        print("Sınav hakkınız kalmadı!")
                elif choice == "2":
                    self.display_user_results()
                elif choice == "3":
                    self.current_user = None
                    print("Çıkış yapıldı.")
                    break
                else:
                    print("Geçersiz seçim!")

        except Exception as e:
            print(f"Hata: Ana menüde bir problem oluştu: {e}")

    def display_user_results(self):
        """Kullanıcının kendi sınav sonuçlarını gösterir."""
        try:
            user_results = []
            for filename in os.listdir('result'):
                if filename.startswith(f"{self.current_user['username']}_") and filename.endswith('.json'):
                    with open(f'result/{filename}', 'r') as f:
                        result = json.load(f)
                        self.display_results(result)
                        print("\n" + "="*50 + "\n")

            if not user_results:
                print("Henüz hiç sınav sonucunuz bulunmuyor.")

        except Exception as e:
            print(f"Hata: Kullanıcı sonuçları görüntülenirken bir problem oluştu: {e}")

if __name__ == "__main__":
    app = ExamApp()
    app.main_menu()