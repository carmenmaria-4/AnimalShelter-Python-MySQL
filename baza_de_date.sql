USE proiect_adapost;

-- 1. Ștergem tabelele care depind de Vizite_Veterinare sau Animale (ca să evităm erori de Foreign Key)
-- Ordinea este importantă: ștergem "copiii" înainte de "părinți"
DROP TABLE IF EXISTS Vizite_Veterinare;
DROP TABLE IF EXISTS Adoptii;
DROP TABLE IF EXISTS Voluntari;
DROP TABLE IF EXISTS Animale;
DROP TABLE IF EXISTS Hrana;
DROP TABLE IF EXISTS Donatii;
DROP TABLE IF EXISTS Stapani;
DROP TABLE IF EXISTS Adapost;

-- 2. Acum reconstruim totul de la zero cu structura corectă
CREATE TABLE Adapost(
    ID_Adapost INT AUTO_INCREMENT PRIMARY KEY,
    Nume_Adapost VARCHAR(150) NOT NULL UNIQUE,
    Adresa VARCHAR(300) NOT NULL,
    Capacitate INT CHECK (Capacitate > 0)
) ENGINE=InnoDB;

CREATE TABLE Hrana(
    ID_Produs INT AUTO_INCREMENT PRIMARY KEY, 
    Tip_Hrana VARCHAR(50) NOT NULL,
    Cantitate_Kg DECIMAL(10,2) DEFAULT 0.00,
    ID_Adapost INT,
    FOREIGN KEY (ID_Adapost) REFERENCES Adapost(ID_Adapost) ON DELETE CASCADE
) ENGINE=InnoDB;

select * from Hrana;

CREATE TABLE Animale (
    ID_Animal INT AUTO_INCREMENT PRIMARY KEY,
    Nume VARCHAR(50) NOT NULL, 
    Specie VARCHAR(50) DEFAULT 'Pisica',
    Varsta INT CHECK (Varsta >= 0),
    Status VARCHAR(20) DEFAULT 'Disponibil',
    ID_Adapost INT, 
    ID_Produs INT, 
    FOREIGN KEY (ID_Adapost) REFERENCES Adapost(ID_Adapost) ON DELETE CASCADE,
    FOREIGN KEY (ID_Produs) REFERENCES Hrana(ID_Produs) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE Stapani(
    ID_Stapan INT AUTO_INCREMENT PRIMARY KEY,
    Nume VARCHAR(100) NOT NULL,
    Telefon VARCHAR(15) UNIQUE,
    Email VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE Adoptii(
    ID_Adoptie INT AUTO_INCREMENT PRIMARY KEY,
    Data_Adoptie DATE NOT NULL,
    ID_Animal INT, 
    ID_Stapan INT, 
    ID_Adapost INT,
    FOREIGN KEY (ID_Animal) REFERENCES Animale(ID_Animal) ON DELETE CASCADE,
    FOREIGN KEY (ID_Stapan) REFERENCES Stapani(ID_Stapan) ON DELETE CASCADE,
    FOREIGN KEY (ID_Adapost) REFERENCES Adapost(ID_Adapost) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Voluntari(
    ID_Voluntar INT AUTO_INCREMENT PRIMARY KEY, 
    Nume VARCHAR(100) NOT NULL,
    Telefon VARCHAR(20) UNIQUE,
    Rol VARCHAR(50) DEFAULT 'Asistent',
    Data_Alaturare DATE,
    ID_Adapost INT, 
    FOREIGN KEY (ID_Adapost) REFERENCES Adapost(ID_Adapost) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Vizite_Veterinare (
    ID_Vizita INT AUTO_INCREMENT PRIMARY KEY,
    ID_Animal INT,
    Data_Vizita DATE NOT NULL,
    Diagnostic TEXT,
    Tratament VARCHAR(255),
    -- Am setat coloana pentru a stoca statusul de sănătate (Vindecat/Nevindecat/N/A)
    Status_Vindecare VARCHAR(50) DEFAULT 'Nevindecat', 
    FOREIGN KEY (ID_Animal) REFERENCES Animale(ID_Animal) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Donatii(
    ID_Donatie INT AUTO_INCREMENT PRIMARY KEY,
    Nume_Donator VARCHAR(100) DEFAULT 'Donator Anonim',
    Suma DECIMAL(10,2) NOT NULL CHECK (Suma > 0),
    Data_Donatie DATETIME DEFAULT CURRENT_TIMESTAMP,
    Scop_Donatie VARCHAR(100) DEFAULT 'Unde este nevoie mai mult',
    ID_Adapost INT NOT NULL,
    FOREIGN KEY (ID_Adapost) REFERENCES Adapost(ID_Adapost) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Aici e subinterogarea
CREATE OR REPLACE VIEW Urgente_Medicale AS
SELECT Nume, Specie, ID_Adapost
FROM Animale
WHERE ID_Animal IN (
    SELECT ID_Animal 
    FROM Vizite_Veterinare 
    -- TRIM scoate spațiile accidentale, LOWER face totul literă mică
    WHERE TRIM(LOWER(Status_Vindecare)) = 'nevindecat'
);

-- Aici e functia scalara
-- Ștergem funcția dacă există deja
DROP FUNCTION IF EXISTS DeterminUrgenta;

-- Schimbăm delimitatorul pentru a permite semicolonul în interiorul funcției
DELIMITER //

CREATE FUNCTION DeterminUrgenta(diagnostic TEXT) 
RETURNS VARCHAR(50) CHARSET utf8mb4
DETERMINISTIC
BEGIN
    DECLARE alerta VARCHAR(50);
    DECLARE diag_low TEXT;
    
    SET diag_low = LOWER(diagnostic);
    
    IF diag_low LIKE '%fractura%' OR diag_low LIKE '%parvo%' OR diag_low LIKE '%urgent%' OR diag_low LIKE '%hemoragie%' THEN
        SET alerta = 'URGENTA';
    ELSEIF diag_low LIKE '%control%' OR diag_low LIKE '%consult%' OR diag_low LIKE '%rutina%' THEN
        SET alerta = 'RUTINA';
    ELSE
        SET alerta = 'MONITORIZARE';
    END IF;
    
    RETURN alerta;
END //

DELIMITER ;

-- Pasul 3: Testează funcția direct în SQL
SELECT DeterminUrgenta('Are o fractura urata') AS Rezultat;



SELECT ID_Animal, Diagnostic, Status_Vindecare FROM Vizite_Veterinare;
USE proiect_adapost;

-- Dezactivează "Safe Mode" pentru sesiunea curentă (Cea mai rapidă)
SET SQL_SAFE_UPDATES = 0;

-- Modificăm toate înregistrările să fie consecvente
UPDATE Vizite_Veterinare 
SET Status_Vindecare = 'Nevindecat' 
WHERE Status_Vindecare = 'In curs';
-- 1. Ar trebui să vezi 0 rânduri (pentru că le-ai modificat pe toate)
SELECT * FROM Vizite_Veterinare WHERE Status_Vindecare = 'In curs';

-- 2. Ar trebui să vezi acum lista cu Pufi, Bella, Max etc.
SELECT * FROM Urgente_Medicale;

-- Interogare statistică pentru raportul medical din aplicație
SELECT 
    DeterminUrgenta(Diagnostic) AS Tip_Alerta, -- <-- FUNCȚIA SCALARĂ (clasifică diagnosticul)
    COUNT(*) AS Numar_Cazuri                    -- <-- FUNCȚIA DE AGREGARE (numără cazurile)
FROM Vizite_Veterinare 
GROUP BY DeterminUrgenta(Diagnostic);