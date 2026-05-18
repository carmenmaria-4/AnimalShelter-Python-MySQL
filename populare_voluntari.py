import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurația bazei de date (asigură-te că e identică cu cea din app.py)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'student'  # Pune parola ta aici
app.config['MYSQL_DB'] = 'proiect_adapost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def populare_voluntari():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Lista de voluntari pe care vrei să îi adaugi
        # Notă: ID_Adapost trebuie să existe în tabela Adapost (ex: 1)
        voluntari_noi = [
            ('Lucian Popescu', 'Ingrijitor Sef', 1),
            ('Elena Dumitru', 'Asistent Medical', 1),
            ('Andrei Ionescu', 'Dresor', 1),
            ('Maria Vasilescu', 'Coordonator Adopții', 1),
            ('Robert Stan', 'Îngrijitor', 1),
            ('Anca Marinescu', 'Specialist Comportament', 1),
            ('Marius Popa', 'Asistent Medical', 1),
            ('Simona Ionescu', 'Dresor', 1),
            ('George Enache', 'Coordonator Voluntari', 1),
            ('Claudia Sava', 'Îngrijitor', 1)
        ]
        
        try:
            print("Se inserează voluntarii...")
            cur.executemany(
                "INSERT INTO Voluntari (Nume, Rol, ID_Adapost) VALUES (%s, %s, %s)", 
                voluntari_noi
            )
            mysql.connection.commit()
            print(f"Succes! Au fost adăugați {len(voluntari_noi)} voluntari.")
        except Exception as e:
            mysql.connection.rollback()
            print(f"A apărut o eroare: {e}")
        finally:
            cur.close()

if __name__ == '__main__':
    populare_voluntari()