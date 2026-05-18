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
            print("Se adaugă datele adaptate pentru structura proiect_adapost...")
            
            # 1. Adapost
            cur.execute("INSERT INTO Adapost (Nume_Adapost, Adresa, Capacitate) VALUES (%s, %s, %s)", 
                        ("Centrul de Salvare Labute Fericite", "Bulevardul Primaverii Nr. 22", 40))
            id_adapost2 = cur.connection.insert_id()

            # 2. Hrana
            cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                        ("Hrana Uscata Caini", 150.0, id_adapost2))
            id_h_caini = cur.connection.insert_id()
            cur.execute("INSERT INTO Hrana (Tip_Hrana, Cantitate_Kg, ID_Adapost) VALUES (%s, %s, %s)", 
                        ("Conserve Pisici Adult", 75.0, id_adapost2))
            id_h_pisici = cur.connection.insert_id()

            # 3. Animale
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

            # 4. Voluntari
            cur.execute("INSERT INTO Voluntari (Nume, Telefon, Rol, Data_Alaturare, ID_Adapost) VALUES (%s, %s, %s, %s, %s)", 
                        ('Lucian Popescu', '0711222333', 'Ingrijitor Sef', '2024-05-20', id_adapost2))

            # 5. Donatii - MODIFICAT PENTRU STRUCTURA TA
            # Am scos Metoda_Plata și ID_Stapan, am adăugat ID_Adapost (care e NOT NULL în SQL)
            cur.execute("""
                INSERT INTO Donatii (Suma, Data_Donatie, Scop_Donatie, ID_Adapost) 
                VALUES (%s, %s, %s, %s)
            """, (850.00, datetime.datetime.now(), 'Modernizare custi', id_adapost2))

            mysql.connection.commit()
            print("SUCCES: Totul a fost populat corect!")

        except Exception as e:
            print(f"EROARE: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    adauga_adapost_2()