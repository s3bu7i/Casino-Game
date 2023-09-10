import sqlite3

db = sqlite3.connect("./Dərs 10/test.db")
sql = db.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS data(ad TEXT, soyad TEXT, yas INT)")

sql.execute("INSERT INTO data (ad, soyad, yas) VALUES ('Elovset', 'Ziyabala', 222)")

sql.execute("UPDATE data SET ad = 'Maaaahireedhsdsiufsidufsai'")

print(sql.fetchone())
ad =input("Ad daxil et qaqaaa: ")
soyad = "ZKXJNjznjkxs"
yas = 33

for _ in range(330):
    sql.execute(f"INSERT INTO data (ad,soyad,yas) VALUES ('{ad}', '{soyad}', '{yas}')")


sql.execute(f"INSERT INTO data (ad,soyad,yas) VALUES ('{ad}', '{soyad}', '{yas}')")
sql.execute("DELETE FROM data WHERE ad =='elovseeet'")


db.commit()


