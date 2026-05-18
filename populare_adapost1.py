import pymysql
pymysql.install_as_MySQLdb()
import pymysql
from flask import Flask
from flask_mysqldb import MySQL 

app = Flask(__name__)

# --- CONFIGURARE BAZĂ DE DATE ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'student'
app.config['MYSQL_DB'] = 'proiect_adapost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
def populate():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        try:
            print("Se populează baza de date...")
            
            # 1. Adăugăm un Adăpost
            cur.execute("INSERT INTO adapost (Nume_Adapost, Adresa, Capacitate) VALUES (%s, %s, %s)", 
                        ("Adapostul Speranta", "Strada Veseliei 5", 50))
            id_adapost = cur.connection.insert_id()
            
            # 2. Adăugăm câteva tipuri de Hrană
            cur.execute("INSERT INTO hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                        ("Bobite Câini", 100.5, id_adapost))
            id_hrana = cur.connection.insert_id()
            
            # 3. Adăugăm Animale
            animale_test = [
                ('Rex', 'Caine', 3, id_adapost, id_hrana),
                ('Luna', 'Pisica', 2, id_adapost, id_hrana),
                ('Max', 'Caine', 5, id_adapost, id_hrana),
                ('Bella', 'Pisica', 1, id_adapost, id_hrana),
                ('Stacy', 'Caine', 10, id_adapost, id_hrana)
            ]
            cur.executemany("INSERT INTO animale (Nume, Specie, Varsta, ID_Adapost, ID_Produs) VALUES (%s, %s, %s, %s, %s)", animale_test)
            
            # 4. Adăugăm Voluntari
            voluntari_test = [
                ('Andrei Ionescu', '0722111222', 'Asistent', '2024-01-01', id_adapost),
                ('Maria Popa', '0733444555', 'Coordonator', '2024-02-15', id_adapost)
            ]
            cur.executemany("INSERT INTO voluntari (Nume, Telefon, Rol, Data_Alaturare, ID_Adapost) VALUES (%s, %s, %s, %s, %s)", voluntari_test)
            
            mysql.connection.commit()
            print("Succes! Baza de date a fost populată cu date de test.")
            
        except Exception as e:
            print(f"Eroare: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    populate()