import pymysql
pymysql.install_as_MySQLdb()
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
            print("Se verifică existența adăpostului...")
            
            # Pasul 1: Căutăm dacă există deja adăpostul în baza de date
            cur.execute("SELECT ID_Adapost FROM adapost WHERE Nume_Adapost = %s", ("Adapostul Speranta",))
            adapost_existent = cur.fetchone()
            
            if adapost_existent:
                # Dacă adăpostul există, îi luăm ID-ul direct din baza de date
                id_adapost = adapost_existent['ID_Adapost']
                print(f"Adăpostul există deja (ID: {id_adapost}). Nu îl vom recrea.")
                
                # Preluăm și ID-ul hranei existente pentru acest adăpost
                cur.execute("SELECT ID_Produs FROM hrana WHERE ID_Adapost = %s LIMIT 1", (id_adapost,))
                hrana_existenta = cur.fetchone()
                if hrana_existenta:
                    id_hrana = hrana_existenta['ID_Produs']
                else:
                    cur.execute("INSERT INTO hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                                ("Bobite Câini", 100.5, id_adapost))
                    id_hrana = cur.connection.insert_id()
            else:
                # Dacă NU există (e prima rulare), îl creăm acum împreună cu voluntarii
                print("Adăpostul nu a fost găsit. Se creează acum...")
                cur.execute("INSERT INTO adapost (Nume_Adapost, Adresa, Capacitate) VALUES (%s, %s, %s)", 
                            ("Adapostul Speranta", "Strada Veseliei 5", 50))
                id_adapost = cur.connection.insert_id()
                
                cur.execute("INSERT INTO hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                            ("Bobite Câini", 100.5, id_adapost))
                id_hrana = cur.connection.insert_id()
                
                voluntari_test = [
                    ('Andrei Ionescu', '0722111222', 'Asistent', '2024-01-01', id_adapost),
                    ('Maria Popa', '0733444555', 'Coordonator', '2024-02-15', id_adapost)
                ]
                cur.executemany("INSERT INTO voluntari (Nume, Telefon, Rol, Data_Alaturare, ID_Adapost) VALUES (%s, %s, %s, %s, %s)", voluntari_test)

            # Pasul 2: Lista extinsă de ANIMALE NOI (15 caractere noi)
            print("Se adaugă animalele noi...")
            animale_noi = [
                # --- CÂINI ---
                ('Rocky', 'Caine', 4, id_adapost, id_hrana),
                ('Bruno', 'Caine', 6, id_adapost, id_hrana),
                ('Toby', 'Caine', 2, id_adapost, id_hrana),
                ('Grivei', 'Caine', 1, id_adapost, id_hrana),
                ('Rexi', 'Caine', 8, id_adapost, id_hrana),
                ('Paco', 'Caine', 3, id_adapost, id_hrana),
                ('Azor', 'Caine', 5, id_adapost, id_hrana),
                ('Zoro', 'Caine', 2, id_adapost, id_hrana),
                
                # --- PISICI ---
                ('Oscar', 'Pisica', 1, id_adapost, id_hrana),
                ('Maya', 'Pisica', 3, id_adapost, id_hrana),
                ('Mitza', 'Pisica', 2, id_adapost, id_hrana),
                ('Pufu', 'Pisica', 1, id_adapost, id_hrana),
                ('Felix', 'Pisica', 4, id_adapost, id_hrana),
                ('Lili', 'Pisica', 7, id_adapost, id_hrana),
                ('Simba', 'Pisica', 1, id_adapost, id_hrana)
            ]
            
            # Corectat variabila de inserat: animale_noi
            cur.executemany("INSERT INTO animale (Nume, Specie, Varsta, ID_Adapost, ID_Produs) VALUES (%s, %s, %s, %s, %s)", animale_noi)
            
            mysql.connection.commit()
            print(f"Succes! Cele {len(animale_noi)} animale noi au fost adăugate în adăpost.")
            
        except Exception as e:
            print(f"Eroare întâmpinată: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    populate()