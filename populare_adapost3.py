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
            print("Se adaugă date noi în baza de date (folosind INSERT IGNORE)...")
            
            # 1. Adăugăm un al doilea adăpost
            cur.execute("""
                INSERT IGNORE INTO Adapost (Nume_Adapost, Adresa, Capacitate) 
                VALUES (%s, %s, %s)
            """, ("Sanctuarul Codrii", "Soseaua de Centura KM 12", 30))
            
            # Recuperăm ID-ul
            id_adapost2 = cur.connection.insert_id()
            
            # Dacă id-ul e 0, înseamnă că adăpostul există deja
            if id_adapost2 == 0:
                cur.execute("SELECT ID_Adapost FROM Adapost WHERE Nume_Adapost = %s", ("Sanctuarul Codrii",))
                rezultat = cur.fetchone()
                # Accesăm rezultatul ca dicționar (deoarece avem DictCursor)
                id_adapost2 = rezultat['ID_Adapost'] if rezultat else None

            if id_adapost2:
                # 2. Adăugăm Hrană specifică
                cur.execute("""
                    INSERT IGNORE INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) 
                    VALUES (%s, %s, %s)
                """, ("Conserve Vita Câini", 60.0, id_adapost2))
                id_hrana_caini = cur.connection.insert_id()
                
                cur.execute("""
                    INSERT IGNORE INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) 
                    VALUES (%s, %s, %s)
                """, ("Pliculețe Somon Pisici", 40.0, id_adapost2))
                id_hrana_pisici = cur.connection.insert_id()

                # 3. Adăugăm Animale noi
                animale_noi = [
                    ('Thor', 'Caine', 4, id_adapost2, id_hrana_caini if id_hrana_caini > 0 else None),
                    ('Misu', 'Pisica', 7, id_adapost2, id_hrana_pisici if id_hrana_pisici > 0 else None),
                    ('Oscar', 'Pisica', 1, id_adapost2, id_hrana_pisici if id_hrana_pisici > 0 else None),
                    ('Rocky', 'Caine', 2, id_adapost2, id_hrana_caini if id_hrana_caini > 0 else None)
                ]
                cur.executemany("""
                    INSERT IGNORE INTO Animale (Nume, Specie, Varsta, ID_Adapost, ID_Produs) 
                    VALUES (%s, %s, %s, %s, %s)
                """, animale_noi)

                # 4. Adăugăm o donație nouă - MODIFICAT PENTRU STRUCTURA TA
                # Am scos Metoda_Plata și ID_Stapan, am adăugat Scop_Donatie și ID_Adapost
                cur.execute("""
                    INSERT INTO Donatii (Suma, Data_Donatie, Scop_Donatie, ID_Adapost) 
                    VALUES (%s, %s, %s, %s)
                """, (150.00, '2024-05-15', 'Hrana speciala', id_adapost2))

                mysql.connection.commit()
                print(f"Operațiune finalizată cu succes pentru adăpostul: {id_adapost2}")
            else:
                print("Eroare: Nu s-a putut găsi sau crea adăpostul.")
            
        except Exception as e:
            print(f"Eroare: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    adauga()