import pymysql
import random
from datetime import datetime, timedelta
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

def populate_medical_safe():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        try:
            # PASUL 1: Extragem ID-urile care EXISTĂ cu adevărat în tabela Animale
            print("Se extrag ID-urile reale din tabela animale...")
            cur.execute("SELECT ID_Animal FROM animale")
            animale_din_db = cur.fetchall()
            
            if not animale_din_db:
                print("⚠️ Eroare: Tabela 'animale' este complet goală! Populează mai întâi animalele.")
                return

            print(f"S-au găsit {len(animale_din_db)} animale reale în baza de date. Se pregătește popularea...")

            # Șabloane construite STRICT pe cuvintele cheie din funcția ta SQL
            # Ramura 1: URGENTA (contine: fractura, parvo, urgent, hemoragie)
            sabloane_urgenta = [
                ("Animalul a suferit o fractura la membrul stâng", "Imobilizare și radiografie", "Nevindecat"),
                ("Simptome severe de parvo detectate", "Izolare și tratament perfuzabil", "Nevindecat"),
                ("Caz urgent - stare critică la sosire", "Intervenție chirurgicală imediată", "Nevindecat"),
                ("Prezintă hemoragie internă în urma unui accident", "Stabilizare și monitorizare semne vitale", "Nevindecat")
            ]
            
            # Ramura 2: RUTINA (contine: control, consult, rutina)
            sabloane_rutina = [
                ("Control medical periodic obligatoriu", "Evaluare generală stare de sănătate", "Vindecat"),
                ("Consult amănunțit pentru schema de vaccinare", "Administrare vaccin anual", "Vindecat"),
                ("Procedură de rutina - deparazitare internă", "Administrare pastilă deparazitare", "Vindecat")
            ]
            
            # Ramura 3: MONITORIZARE (orice altceva ce nu declanșează IF sau ELSEIF)
            sabloane_monitorizare = [
                ("Ușoară iritație la nivelul pielii", "Aplicat unguent calmant", "Nevindecat"),
                ("Se recomandă toaleta urechilor din cauza mizeriei", "Curățare cu soluție specială", "Nevindecat"),
                ("Animalul prezintă o ușoară apatie sezonieră", "Administrare vitamine în hrană", "Vindecat")
            ]
            
            vizite_de_introdus = []
            data_baza = datetime.now()
            
            # PASUL 2: Generăm fișe doar pentru ID-urile valide găsite
            for index, anim in enumerate(animale_din_db):
                id_an = anim['ID_Animal']  # Luăm ID-ul extras direct din DB
                
                # Împărțim cazurile uniform
                if index % 3 == 0:
                    diag, trat, status = random.choice(sabloane_urgenta)
                elif index % 3 == 1:
                    diag, trat, status = random.choice(sabloane_rutina)
                else:
                    diag, trat, status = random.choice(sabloane_monitorizare)
                
                data_vizita = (data_baza - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
                vizite_de_introdus.append((id_an, data_vizita, diag, trat, status))
            
            # PASUL 3: Inserare în masă
            cur.executemany("""
                INSERT INTO vizite_veterinare (ID_Animal, Data_Vizita, Diagnostic, Tratament, Status_Vindecare) 
                VALUES (%s, %s, %s, %s, %s)
            """, vizite_de_introdus)
            
            mysql.connection.commit()
            print(f"🚀 Succes total! S-au adăugat {len(vizite_de_introdus)} vizite veterinare corelate perfect cu ID-urile reale.")
            
        except Exception as e:
            print(f"Eroare întâmpinată la inserare: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

if __name__ == '__main__':
    populate_medical_safe()