import sqlite3
import random
import time


db = sqlite3.connect('Dərs 11/atm.db')
sql = db.cursor()

sql.execute('''
   CREATE TABLE IF NOT EXISTS users(
       id INTEGER PRIMARY KEY,
       username TEXT,
       password INTEGER,
       balance REAL
   )         
''')

sql.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        timestamp TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

db.commit()

def register():
    username = input("Isdifadəçi adını daxil et: ")
    password = int(input("Parlolunuzu daxil edin: "))
    balance = 0.0
    
    #sql.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, ?)', (username, password, balance))
    sql.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, ?)', (username, password, balance))

    db.commit()
    print("Loading...")
    time.sleep(3)
    print("Qeydiyyat uğurla başa çatdı.")

def login():
    username = input("Isdifadəçi adınzı daxil edin: ")
    password = int(input("Parolunuzu daxil edin: "))
    
    sql.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user_id = sql.fetchone()
    
    if user_id is not None:  # Kullanıcı kimliği bulunduysa
        print(f"Xoş gəldiniz, {username}!")
        return user_id[0]
    else:
        print("Yalnış isdifdəçi adı və ya PIN daxil etmisiniz.")
        return None


# def login():
#     username = input("Isdifadəçi adınzı daxil edin: ")
#     password = int(input("Parolunuzu daxil edin: "))
    
#     sql.execute('SELECT id FROM users WHERE username = ? AND password = ?',(username, password))
#     user_id = sql.fetchone()
    
#     if user_id:
#         print(f"Xoş gəldiniz, {username}!")
#         return user_id[0]
#     else:
#         print("Yalnış isdifdəçi adı və ya PIN daxil etmisiniz.")
#         return None

def check_balance(user_id):
    sql.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    balance = sql.fetchone()[0]
    print("Sizin hesab balansınız: ${:.2f}".format(balance))

def deposit(user_id):
    amount = float(input("Daxil etmək isdədiyiniz məbləği daxil edin: "))
    sql.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
    db.commit()
    print("${:.2f} hesabınıza əlavə edildi.".format(amount))
    
def withdraw(user_id):
    amount = float(input("Çıxarmaq isdədiyiniz məbləği daxil et: "))
    sql.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    balance = sql.fetchone()[0]
    
    if amount > balance:
        print("Balansınızda kifayət qədər pul yoxdur. ")
        
    else:
        sql.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
        db.commit()
        print("${:.2f} pul hesabınızdan çıxarıldı.".format(amount))
        
def manage_account(user_id):
    print("""
Hesab əməliyyatları:
    1. PIN kodu dəyiş
    2. Hesab məlumatları
        """)
    choice = input("Seçiminizi daxil edin: ")
    
    if choice == '1':
        new_pin = int(input("Yeni PIN kodu daxil edin: "))
        confirm_pin = int(input("Yeni PIN kodu təsdiq edin: "))
        
        if new_pin == confirm_pin:
            sql.execute("UPDATE users SET pin = ? WHERE id = ?", (new_pin, user_id))
            db.commit()
            print("PIN kodunuz dəyişdirildi.")
        else:
            print("PIN kodunuz uyğunlaşmır. Yenidən cəhd edin.")
    elif choice == '2':
        sql.execute('SELECT username, balance FROM users WHERE id = ?', (user_id,))
        user_info = sql.fetchone()
        print("Isdifadəçi adı: {}".format(user_info[0]))
        print("Hesab balansı: ${:.2f}".format(user_info[1]))
    else:
        print("Yanlış seçim. Zəhmət olmasa yenidən seçin.")
          
    
def start_game(user_id):
    while True:
        print("""
    0. Oyuna başla
    1. Hesab balansınız
    2. Hesaba pul əlavə edin
    3. Hesabdan pul cıxardın
    4. Hesab əməliyyatları 
    5. Çıxış
              """)
        choice = input("Seçdiyiniz nömrəni daxil et: ")
        if choice == '0':
            play_game(user_id)
        elif choice == '1':
            check_balance(user_id)
        elif choice == '2':
            deposit(user_id)
        elif choice == '3':
            withdraw(user_id)
        elif choice == '4':
            manage_account(user_id)
        elif choice == '5':
            break
        else:
            print("Yalnış seçim. Zəhmət olmasa yenidən seçin")

def play_game(user_id):
    print("Oyun başladı!")
    starting_balance = float(input("Oyun üçün başlanğıc məbləğini daxil edin: "))
    sql.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    result = sql.fetchone()
    if result is None:
        print("Balansınızı yoxlayarkən bir sorun oluştu. Lütfen daha sonra tekrar deneyin.")
        return
    
    balance = result[0]
    
    if starting_balance > balance:
        print("Balansınızda kifayət qədər pul yoxdur. Zəhmət olmasa balansınızı yoxlayın :D")
        return

    guess = int(input("Bir rəqəm seçin (0-9 arası): "))
    random_number = random.randint(0, 9)

    if guess == random_number:
        doubled_balance = starting_balance * 2
        sql.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (doubled_balance, user_id))
        db.commit()
        print("Təbriklər! Siz texmin etdiyiniz rəqəmi düzgün bildiniz.")
        print("${:.2f} hesabınıza əlavə edildi.".format(doubled_balance))
    else:
        amount = starting_balance
        sql.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
        db.commit()
        print("${:.2f} pul hesabınızdan çıxarıldı.".format(amount))

    sql.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    balance = sql.fetchone()[0]
    print("Toplam balansınız: ${:.2f}".format(balance))


        
def main():
    print("""
    Kazino oyununa xoş gəlmisiniz. İlk öncə programda login və ya register etməlisiniz.
    1. Qeydiyyat
    2. Daxil ol
    3. Çıxış
    """)
    
    while True:
        choice = input("Seçiminizi daxil edin: ")
        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            start_game(user_id)
            
        elif choice == '3':
            print("Çıxış edir...")
            break
        else:
            print("Yanlış seçim. Zəhmət olmasa yenidən seçin.")

if __name__ == "__main__":
    main()

