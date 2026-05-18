import pymysql
import datetime
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mysqldb import MySQL 

app = Flask(__name__)

# Configurații bază de date
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'student'
app.config['MYSQL_DB'] = 'proiect_adapost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def adauga():
    with app.app_context():
        cur = mysql.connection.cursor()
        try:
            print("Se verifică existența adăpostului...")
            
            # 1. Încercăm să adăugăm adăpostul
            cur.execute("""
                INSERT IGNORE INTO Adapost (Nume_Adapost, Adresa, Capacitate) 
                VALUES (%s, %s, %s)
            """, ("Sanctuarul Codrii", "Soseaua de Centura KM 12", 30))
            
            id_adapost2 = cur.connection.insert_id()
            
            # Dacă id-ul e 0, înseamnă că adăpostul există deja, deci îl căutăm
            if id_adapost2 == 0:
                cur.execute("SELECT ID_Adapost FROM Adapost WHERE Nume_Adapost = %s", ("Sanctuarul Codrii",))
                rezultat = cur.fetchone()
                id_adapost2 = rezultat['ID_Adapost'] if rezultat else None

            if id_adapost2:
                print(f"Lucrăm cu adăpostul ID: {id_adapost2}")
                
                # 2. Gestionare Hrană Câini
                cur.execute("""
                    INSERT IGNORE INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) 
                    VALUES (%s, %s, %s)
                """, ("Conserve Vita Câini", 60.0, id_adapost2))
                id_hrana_caini = cur.connection.insert_id()
                
                if id_hrana_caini == 0:  # Dacă exista deja, îi aflăm ID-ul real
                    cur.execute("SELECT ID_Produs FROM Hrana WHERE Tip_Hrana = %s AND ID_Adapost = %s", ("Conserve Vita Câini", id_adapost2))
                    res_h = cur.fetchone()
                    id_hrana_caini = res_h['ID_Produs'] if res_h else None

                # 3. Gestionare Hrană Pisici
                cur.execute("""
                    INSERT IGNORE INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) 
                    VALUES (%s, %s, %s)
                """, ("Pliculețe Somon Pisici", 40.0, id_adapost2))
                id_hrana_pisici = cur.connection.insert_id()
                
                if id_hrana_pisici == 0:  # Dacă exista deja, îi aflăm ID-ul real
                    cur.execute("SELECT ID_Produs FROM Hrana WHERE Tip_Hrana = %s AND ID_Adapost = %s", ("Pliculețe Somon Pisici", id_adapost2))
                    res_p = cur.fetchone()
                    id_hrana_pisici = res_p['ID_Produs'] if res_p else None

                # 4. Adăugăm o listă mai mare de animale noi
                print("Se adaugă animalele noi...")
                animale_noi = [
                    # --- Animale inițiale ---
                    ('Thor', 'Caine', 4, id_adapost2, id_hrana_caini),
                    ('Misu', 'Pisica', 7, id_adapost2, id_hrana_pisici),
                    ('Oscar', 'Pisica', 1, id_adapost2, id_hrana_pisici),
                    ('Rocky', 'Caine', 2, id_adapost2, id_hrana_caini),
                    
                    # --- Animale noi adăugate pentru extindere ---
                    ('Ares', 'Caine', 3, id_adapost2, id_hrana_caini),
                    ('Freya', 'Caine', 1, id_adapost2, id_hrana_caini),
                    ('Loki', 'Pisica', 2, id_adapost2, id_hrana_pisici),
                    ('Cleo', 'Pisica', 5, id_adapost2, id_hrana_pisici),
                    ('Simba', 'Pisica', 1, id_adapost2, id_hrana_pisici),
                    ('Baloo', 'Caine', 6, id_adapost2, id_hrana_caini)
                ]
                
                cur.executemany("""
                    INSERT IGNORE INTO Animale (Nume, Specie, Varsta, ID_Adapost, ID_Produs) 
                    VALUES (%s, %s, %s, %s, %s)
                """, animale_noi)

                # 5. Adăugăm o donație doar dacă este o rulare nouă sau vrei să se cumuleze istoricul
                cur.execute("""
                    INSERT INTO Donatii (Suma, Data_Donatie, Scop_Donatie, ID_Adapost) 
                    VALUES (%s, %s, %s, %s)
                """, (150.00, datetime.date.today(), 'Alte cauze speciale', id_adapost2))

                mysql.connection.commit()
                print(f"Succes! Datele au fost actualizate pentru adăpostul: {id_adapost2}")
            else:
                print("Eroare: Nu s-a putut găsi sau crea adăpostul.")
            
        except Exception as e:
            print(f"Eroare: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    adauga()