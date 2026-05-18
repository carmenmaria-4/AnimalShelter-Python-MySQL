import pymysql 
import datetime 
import random
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'student'
app.config['MYSQL_DB'] = 'proiect_adapost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def adauga_adapost_2():
    with app.app_context():
        cur = mysql.connection.cursor()
        try:
            print("Se verifică existența adăpostului secundar...")
            
            # Pasul 1: Căutăm dacă există deja acest adăpost specific
            cur.execute("SELECT ID_Adapost FROM Adapost WHERE Nume_Adapost = %s", ("Centrul de Salvare Labute Fericite",))
            adapost_existent = cur.fetchone()
            
            if adapost_existent:
                # Dacă adăpostul există, îi preluăm ID-ul direct
                id_adapost2 = adapost_existent['ID_Adapost']
                print(f"Adăpostul există deja (ID: {id_adapost2}). Se trece la verificarea hranei...")
                
                # Preluăm ID-ul pentru hrana de câini existentă
                cur.execute("SELECT ID_Produs FROM Hrana WHERE ID_Adapost = %s AND Tip_Hrana = %s LIMIT 1", (id_adapost2, "Hrana Uscata Caini"))
                h_caini_existenta = cur.fetchone()
                id_h_caini = h_caini_existenta['ID_Produs'] if h_caini_existenta else None
                
                # Preluăm ID-ul pentru hrana de pisici existentă
                cur.execute("SELECT ID_Produs FROM Hrana WHERE ID_Adapost = %s AND Tip_Hrana = %s LIMIT 1", (id_adapost2, "Conserve Pisici Adult"))
                h_pisici_existenta = cur.fetchone()
                id_h_pisici = h_pisici_existenta['ID_Produs'] if h_pisici_existenta else None
                
                # În cazul ideal în care baza de date e curată, ID-urile sunt deja găsite. 
                # Dacă lipsesc din vreun motiv, le generăm rapid ca siguranță:
                if not id_h_caini:
                    cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", ("Hrana Uscata Caini", 150.0, id_adapost2))
                    id_h_caini = cur.connection.insert_id()
                if not id_h_pisici:
                    cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", ("Conserve Pisici Adult", 75.0, id_adapost2))
                    id_h_pisici = cur.connection.insert_id()
            else:
                # Dacă NU există, creăm adăpostul și toate datele inițiale de bază (o singură dată)
                print("Adăpostul nu a fost găsit. Se creează acum structura de bază...")
                
                # 1. Creare Adapost
                cur.execute("INSERT INTO Adapost (Nume_Adapost, Adresa, Capacitate) VALUES (%s, %s, %s)", 
                            ("Centrul de Salvare Labute Fericite", "Bulevardul Primaverii Nr. 22", 40))
                id_adapost2 = cur.connection.insert_id()

                # 2. Creare Hrana
                cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                            ("Hrana Uscata Caini", 150.0, id_adapost2))
                id_h_caini = cur.connection.insert_id()
                
                cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                            ("Conserve Pisici Adult", 75.0, id_adapost2))
                id_h_pisici = cur.connection.insert_id()

                # 4. Creare Voluntar
                cur.execute("INSERT INTO Voluntari (Nume, Telefon, Rol, Data_Alaturare, ID_Adapost) VALUES (%s, %s, %s, %s, %s)", 
                            ('Lucian Popescu', '0711222333', 'Ingrijitor Sef', '2024-05-20', id_adapost2))

                # 5. Creare Donație inițială
                cur.execute("""
                    INSERT INTO Donatii (Suma, Data_Donatie, Scop_Donatie, ID_Adapost) 
                    VALUES (%s, %s, %s, %s)
                """, (850.00, datetime.datetime.now(), 'Modernizare custi', id_adapost2))

            # Pasul 2: Lista de ANIMALE NOI pe care le poți schimba la fiecare rulare
            print("Se adaugă o nouă serie de animale și istoricul lor medical...")
            animale_noi = [
                ('Rexi', 'Caine', 2, id_adapost2, id_h_caini),
                ('Grivei', 'Caine', 6, id_adapost2, id_h_caini),
                ('Miti', 'Pisica', 1, id_adapost2, id_h_pisici),
                ('Pufu', 'Pisica', 4, id_adapost2, id_h_pisici),
                ('Luna', 'Caine', 3, id_adapost2, id_h_caini),
                ('Max', 'Caine', 5, id_adapost2, id_h_caini),
                ('Bella', 'Pisica', 2, id_adapost2, id_h_pisici),
                ('Oscar', 'Caine', 8, id_adapost2, id_h_caini),
                ('Daisy', 'Caine', 1, id_adapost2, id_h_caini),
                ('Simba', 'Pisica', 3, id_adapost2, id_h_pisici),
                ('Rocky', 'Caine', 4, id_adapost2, id_h_caini),
                ('Milo', 'Pisica', 2, id_adapost2, id_h_pisici),
                ('Zoe', 'Caine', 7, id_adapost2, id_h_caini),
                ('Maya', 'Pisica', 5, id_adapost2, id_h_pisici),
                ('Bruno', 'Caine', 3, id_adapost2, id_h_caini)
            ]
            
            scenarii_medicale = [
                {"diag": "Vaccinare Anuala", "trat": "Schema polivalenta", "stat": "-"},
                {"diag": "Deparazitare", "trat": "Administrare tableta", "stat": "-"},
                {"diag": "Otita Bacteriana", "trat": "Picaturi otice 7 zile", "stat": "Vindecat"},
                {"diag": "Dermatita Alergica", "trat": "Unguent + Dieta speciala", "stat": "In curs"},
                {"diag": "Gastroenterita", "trat": "Regim alimentar + Hidratare", "stat": "Vindecat"},
                {"diag": "Fractura membru", "trat": "Imobilizare + Repaus", "stat": "Vindecat"},
                {"diag": "Control Post-Operator", "trat": "Monitorizare cicatrice", "stat": "Vindecat"},
                {"diag": "Consult General", "trat": "Examinare clinica completa", "stat": "-"}
            ]

            # Inserăm fiecare animal și generăm vizite medicale simulate
            for nume, specie, varsta, adap_id, prod_id in animale_noi:
                cur.execute("INSERT INTO Animale (Nume, Specie, Varsta, ID_Adapost, ID_Produs) VALUES (%s, %s, %s, %s, %s)", 
                            (nume, specie, varsta, adap_id, prod_id))
                id_animal = cur.connection.insert_id()

                nr_vizite = random.randint(2, varsta + 2)
                for _ in range(nr_vizite):
                    zile_urma = random.randint(15, (varsta * 365))
                    data_vizita = datetime.date.today() - datetime.timedelta(days=zile_urma)
                    scenariu = random.choice(scenarii_medicale)
                    
                    cur.execute("""
                        INSERT INTO Vizite_Veterinare (ID_Animal, Data_Vizita, Diagnostic, Tratament, Status_Vindecare) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (id_animal, data_vizita, scenariu['diag'], scenariu['trat'], scenariu['stat']))

            mysql.connection.commit()
            print(f"SUCCES: Au fost adăugate {len(animale_noi)} animale în adăpostul existent, împreună cu istoricul lor medical!")

        except Exception as e:
            print(f"EROARE: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    adauga_adapost_2()