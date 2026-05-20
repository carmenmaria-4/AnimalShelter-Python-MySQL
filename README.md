# 🐾 ShelterConnect - Sistem Integrat de Gestiune a Adăposturilor de Animale

**ShelterConnect** este o soluție digitală completă, dezvoltată pentru a eficientiza managementul zilnic al adăposturilor de animale. Proiectul centralizează fluxurile de lucru esențiale — de la evidența medicală și triajul automat al urgențelor, până la gestionarea adopțiilor, a voluntarilor și a resurselor financiare provenite din donații.

Aplicația este construită pe o arhitectură robustă, utilizând **Python (Flask)** pentru logica de business și **MySQL** pentru o stocare securizată, garantând integritatea datelor prin motorul **InnoDB**.

---
### Demo Proiect
<video src="./demo_video.mp4" width="100%" controls></video>

## 🌟 Funcționalități și Module Principale

### 1. Panoul Medical și Triaj Inteligent
Sistemul monitorizează starea de sănătate a fiecărui animal. Folosind o **funcție scalară SQL**, aplicația analizează diagnosticele veterinare și clasifică automat vizitele în:
* **URGENȚĂ:** Pentru cazuri critice (fracturi, hemoragii, boli infecțioase).
* **RUTINĂ:** Pentru controale anuale și vaccinări.
* **MONITORIZARE:** Pentru cazuri aflate sub observație.

De asemenea, un **View SQL** (tabelă virtuală) permite personalului să vadă instant lista urgențelor medicale active, simplificând procesul de triaj.

### 2. Procesul de Adopție (Lifecycle Management)
Aplicația gestionează ciclul de viață al animalului în adăpost:
* Înregistrarea intrării și alocarea resurselor de hrană specifice.
* Procesarea formularelor de adopție prin care se înregistrează simultan noul stăpân și se actualizează automat statusul animalului.
* Menținerea unui istoric complet al adopțiilor realizate pentru fiecare punct de lucru.

### 3. Managementul Voluntariatului
O interfață dedicată permite coordonatorilor să administreze echipa:
* Înregistrarea voluntarilor noi și alocarea de roluri (Asistent, Îngrijitor, Coordonator).
* Actualizarea rolurilor în funcție de performanță.
* Ștergerea înregistrărilor pentru persoanele care părăsesc programul.

### 4. Monitorizarea Donațiilor și Resurselor
Sistemul oferă transparență totală asupra fondurilor colectate:
* Înregistrarea donațiilor cu opțiune de anonimat.
* Calcularea automată a sumelor totale prin **funcții agregate SQL**.
* Vizualizarea destinației fondurilor (scopul donației) și a adăpostului beneficiar.

---

## 🛠️ Detalii Tehnice (Stack-ul Proiectului)

* **Backend:** Python 3.10+ cu framework-ul Flask.
* **Bază de Date:** MySQL 8.0+ (utilizând motorul **InnoDB** pentru integritate referențială și tranzacții).
* **Frontend:** Interfață web modernă construită cu HTML5 și CSS3, structurată pe 9 template-uri dedicate.
* **Localizare:** Atât interfața grafică, cât și baza de date sunt configurate integral în **limba Română**.
* **Logică SQL:** Utilizarea de JOIN-uri complexe, sub-interogări, VIEW-uri și funcții programabile direct pe server.

---

## 📂 Structura Fișierelor

* `app.py`: Controller-ul principal care gestionează rutele web și conexiunea la baza de date.
* `baza_de_date.sql`: Script SQL complet pentru crearea tabelelor, constrângerilor (CHECK/UNIQUE), funcțiilor și view-urilor.
* **Scripturi de Populare:** Fișiere Python (`populare_adapost1_new.py`, `populare_vizite_veterinare.py`, `populare_voluntari.py` etc.) folosite pentru inițializarea sistemului cu date realiste.
* `templates/`: Directorul ce conține cele 9 pagini HTML (Home, Animale, Donații, Fișă Medicală, Voluntari etc.).

---

## ⚙️ Ghid de Instalare și Configurare

Urmează acești pași pentru a rula proiectul pe instanța ta locală:

### Pasul 1: Pregătirea Bazei de Date (MySQL)
1. Deschide MySQL Workbench și conectează-te la serverul tău local.
2. Execută scriptul `baza_de_date.sql`. Acesta va crea baza de date `proiect_adapost` și toate structurile necesare.
3. **CRITIC:** Deschide fișierul `app.py` și modifică valorile din secțiunea `# --- CONFIGURARE BAZĂ DE DATE ---` (Port, User, Parolă) pentru a se potrivi cu setările tale de MySQL.

### Pasul 2: Instalarea Dependențelor
În terminal, instalează bibliotecile necesare rulând:
```bash
pip install flask flask-mysqldb pymysql
```
### Pasul 3: Popularea cu date
Înainte de a porni site-ul, rulează scripturile de populare pentru a genera datele de test:
python populare_adapost1_new.py
python populare_vizite_veterinare.py
python populare_voluntari.py
# Rulează restul fișierelor de tip 'populare' disponibile în folder

### Pasul 4: Pornirea aplicatiei
Lanseaza serverul Flask
```bash
python app.py
```
Accesează în browser adresa: http://127.0.0.1:5000






