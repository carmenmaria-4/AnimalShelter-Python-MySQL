import pymysql
import datetime
# Linia de mai jos este critică pentru a face legătura între PyMySQL și Flask-MySQLdb
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'cheie_secreta_facultate_123'

# --- CONFIGURARE BAZĂ DE DATE ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'student'
app.config['MYSQL_DB'] = 'proiect_adapost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# --- 1. HOME ---
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    
    # 1. Luăm lista de adăposturi pentru carduri
    cur.execute("SELECT * FROM Adapost")
    adaposturi = cur.fetchall()
    
    # 2. Calculăm statisticile globale pentru contoarele animate
    cur.execute("SELECT COUNT(*) as total FROM Animale")
    total_salvati = cur.fetchone()['total'] or 0
    
    cur.execute("SELECT COUNT(*) as total FROM Animale WHERE Status = 'Disponibil'")
    in_adapost = cur.fetchone()['total'] or 0
    
    cur.execute("SELECT COUNT(*) as total FROM Animale WHERE Status = 'Adoptat'")
    adoptati = cur.fetchone()['total'] or 0
    
    stats_globale = {
        'salvati': total_salvati,
        'in_adapost': in_adapost,
        'adoptati': adoptati,
    }
    
    cur.close()
    return render_template('selecteaza_adapost.html', 
                           adaposturi=adaposturi, 
                           stats=stats_globale)

# --- 2. DESPRE NOI ---
@app.route('/despre-noi')
def despre_noi():
    return render_template('despre_noi.html')

# --- 3. DASHBOARD ADĂPOST ---
@app.route('/adapost/<int:id_adapost>')
def detalii_adapost(id_adapost):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Adapost WHERE ID_Adapost = %s", [id_adapost])
    info_adapost = cur.fetchone()

    cur.execute("""
        SELECT Specie, COUNT(*) as nr FROM Animale 
        WHERE ID_Adapost = %s AND Status = 'Disponibil'
        GROUP BY Specie
    """, [id_adapost])
    stats = cur.fetchall()
    
    cur.execute("""
        SELECT a.Nume as Animal, s.Nume as Stapan, ad.Data_Adoptie 
        FROM Adoptii ad
        JOIN Animale a ON ad.ID_Animal = a.ID_Animal
        JOIN Stapani s ON ad.ID_Stapan = s.ID_Stapan
        WHERE ad.ID_Adapost = %s
        ORDER BY ad.Data_Adoptie DESC LIMIT 3
    """, [id_adapost])
    recent = cur.fetchall()
    cur.close()
    return render_template('adapost.html', stats=stats, recent=recent, adapost=info_adapost)

# --- 4. LISTA ANIMALE ---
@app.route('/adapost/<int:id_adapost>/animale')
def animale(id_adapost):
    cur = mysql.connection.cursor()
    f_specie = request.args.get('specie', '')
    f_varsta = request.args.get('varsta', '')

    query = "SELECT * FROM Animale WHERE ID_Adapost = %s AND Status = 'Disponibil'"
    params = [id_adapost]

    if f_specie:
        query += " AND Specie = %s"
        params.append(f_specie)

    if f_varsta == 'pui':
        query += " AND Varsta <= 2"
    elif f_varsta == 'adult':
        query += " AND Varsta BETWEEN 3 AND 7"
    elif f_varsta == 'senior':
        query += " AND Varsta >= 8"

    cur.execute(query, params)
    lista = cur.fetchall()
    cur.close()
    return render_template('animale.html', animale=lista, id_adapost=id_adapost, f_specie=f_specie, f_varsta=f_varsta)

# --- 5. PROCES ADOPȚIE ---
@app.route('/adopta/<int:id_animal>', methods=['GET', 'POST'])
def proces_adoptie(id_animal):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Animale WHERE ID_Animal = %s", [id_animal])
    animal = cur.fetchone()
    
    if not animal:
        cur.close()
        return redirect(url_for('home'))
        
    id_adapost = animal['ID_Adapost']

    if request.method == 'POST':
        nume_stapan = request.form['nume_stapan']
        tel = request.form['telefon']
        email = request.form['email']
        data_azi = datetime.date.today()

        try:
            cur.execute("SET SQL_SAFE_UPDATES = 0;")
            
            cur.execute("INSERT INTO Stapani (Nume, Telefon, Email) VALUES (%s, %s, %s)", (nume_stapan, tel, email))
            id_stapan = cur.lastrowid
            
            cur.execute("INSERT INTO Adoptii (Data_Adoptie, ID_Animal, ID_Stapan, ID_Adapost) VALUES (%s, %s, %s, %s)", 
                        (data_azi, id_animal, id_stapan, id_adapost))
            
            cur.execute("UPDATE Animale SET Status = 'Adoptat' WHERE ID_Animal = %s", [id_animal])
            
            mysql.connection.commit()
            flash(f'Felicitări! {animal["Nume"]} a fost adoptat.')
            cur.close()
            return redirect(url_for('animale', id_adapost=id_adapost))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Eroare la procesarea adopției: {str(e)}')
            cur.close()
        
    return render_template('formular_adoptie.html', animal=animal)

# --- 6. DONAȚII ---
@app.route('/donatii')
def donatii():
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(Suma) as total FROM Donatii")
    res = cur.fetchone()
    total_suma = res['total'] if res['total'] else 0

    cur.execute("""
        SELECT d.Nume_Donator, d.Suma, d.Data_Donatie, d.Scop_Donatie, a.Nume_Adapost 
        FROM Donatii d 
        JOIN Adapost a ON d.ID_Adapost = a.ID_Adapost 
        ORDER BY d.Data_Donatie DESC
    """)
    lista_donatii = cur.fetchall()
    cur.close()
    return render_template('donatii.html', donatii=lista_donatii, total=total_suma)

@app.route('/inregistreaza-donatie', methods=['POST'])
def inregistreaza_donatie():
    suma = request.form.get('suma')
    id_adapost = request.form.get('id_adapost') or 1
    nume_introdus = request.form.get('nume_donator')
    scop_ales = request.form.get('scop') or 'Susținerea adăpostului (General)'
    
    if not nume_introdus or nume_introdus.strip() == "":
        nume_final = "Donator Anonim"
    else:
        nume_final = nume_introdus.strip()
        
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO Donatii (Nume_Donator, Suma, ID_Adapost, Scop_Donatie) 
            VALUES (%s, %s, %s, %s)
        """, (nume_final, suma, id_adapost, scop_ales))
        mysql.connection.commit()
        flash("Donație înregistrată cu succes!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Eroare la salvare: {str(e)}")
    finally:
        cur.close()
    
    return redirect(url_for('donatii'))

# --- 7. FIȘA MEDICALĂ ȘI VIEW ---
@app.route('/animal/<int:id_animal>/medical')
def fisa_medicala(id_animal):
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_Animal, Nume, Specie, ID_Adapost FROM Animale WHERE ID_Animal = %s", [id_animal])
    animal = cur.fetchone()
    
    if not animal:
        cur.close()
        return "Animalul nu a fost găsit", 404

    cur.execute("""
        SELECT ID_Vizita, Data_Vizita, Diagnostic, Tratament, Status_Vindecare,
               DeterminUrgenta(Diagnostic) AS Nivel_Alerta
        FROM Vizite_Veterinare 
        WHERE ID_Animal = %s 
        ORDER BY Data_Vizita DESC
    """, [id_animal])
    vizite = cur.fetchall()

    # Folosim View-ul Urgente_Medicale cerut în barem
    cur.execute("""
        SELECT Nume, Specie 
        FROM Urgente_Medicale 
        WHERE ID_Adapost = %s AND Nume != %s 
        LIMIT 3
    """, [animal['ID_Adapost'], animal['Nume']])
    
    colegi_urgenti = cur.fetchall()
    cur.close()
    
    return render_template('fisa_medicala.html', 
                           animal=animal, 
                           vizite=vizite, 
                           id_animal=id_animal, 
                           colegi=colegi_urgenti)

# --- 7.1 NOU: DASHBOARD MEDICAL (MIX FUNCȚIE SCALARĂ + AGREGAT) ---
@app.route('/dashboard-medical')
def dashboard_medical():
    cur = mysql.connection.cursor()
    try:
        # QUERY-UL CRITIC: Combină funcția scalară cu funcția agregat COUNT(*)
        cur.execute("""
            SELECT 
                DeterminUrgenta(Diagnostic) AS Tip_Alerta,
                COUNT(*) AS Numar_Cazuri
            FROM Vizite_Veterinare
            GROUP BY DeterminUrgenta(Diagnostic);
        """)
        statistici = cur.fetchall()
        
        cur.close()
        return render_template('dashboard_medical.html', date_statistice=statistici)
    except Exception as e:
        if cur:
            cur.close()
        return f"Eroare la generarea statisticilor medicale avansate: {str(e)}", 500

# --- 8. AFIȘARE ȘI ADĂUGARE VOLUNTARI ---
@app.route('/voluntari', methods=['GET', 'POST'])
def lista_voluntari():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nume = request.form['nume']
        rol = request.form['rol']
        id_adapost = request.form['id_adapost']
        try:
            cur.execute("INSERT INTO Voluntari (Nume, Rol, ID_Adapost) VALUES (%s, %s, %s)", (nume, rol, id_adapost))
            mysql.connection.commit()
            flash("Voluntar adăugat!")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Eroare: {str(e)}")
        return redirect(url_for('lista_voluntari'))

    cur.execute("SELECT * FROM Adapost")
    adaposturi = cur.fetchall()
    cur.execute("""
        SELECT v.ID_Voluntar, v.Nume, v.Rol, a.Nume_Adapost 
        FROM Voluntari v
        JOIN Adapost a ON v.ID_Adapost = a.ID_Adapost
    """)
    voluntari_data = cur.fetchall()
    cur.close()
    return render_template('voluntari.html', voluntari=voluntari_data, adaposturi=adaposturi)

# --- 9. ȘTERGERE VOLUNTAR ---
@app.route('/sterge-voluntar/<int:id_voluntar>')
def sterge_voluntar(id_voluntar):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SET SQL_SAFE_UPDATES = 0;")
        cur.execute("DELETE FROM Voluntari WHERE ID_Voluntar = %s", [id_voluntar])
        mysql.connection.commit()
        flash("Voluntar eliminat!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Eroare la ștergere: {str(e)}")
    finally:
        cur.close()
        
    return redirect(url_for('lista_voluntari'))

# --- 9.1 ACTUALIZARE VOLUNTAR ---
@app.route('/editeaza-voluntar/<int:id_voluntar>', methods=['GET', 'POST'])
def editeaza_voluntar(id_voluntar):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        nou_rol = request.form['rol']
        try:
            cur.execute("SET SQL_SAFE_UPDATES = 0;")
            cur.execute("UPDATE Voluntari SET Rol = %s WHERE ID_Voluntar = %s", (nou_rol, id_voluntar))
            mysql.connection.commit()
            flash("Rolul voluntarului a fost actualizat cu succes!")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Eroare la actualizare: {str(e)}")
        finally:
            cur.close()
            return redirect(url_for('lista_voluntari'))
            
    cur.execute("SELECT * FROM Voluntari WHERE ID_Voluntar = %s", [id_voluntar])
    voluntar = cur.fetchone()
    cur.close()
    
    return render_template('editeaza_voluntar.html', voluntar=voluntar)

if __name__ == '__main__':
    app.run(debug=True)