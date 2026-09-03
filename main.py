import sqlite3
import re
from difflib import SequenceMatcher


# ============================================================
# HOSPITAL PATIENT DATA MANAGEMENT SYSTEM
# ============================================================

# ------------------------------------------------------------
# 1. DATABASE CONNECTION
# ------------------------------------------------------------

conn = sqlite3.connect("hospital.db")
cur = conn.cursor()


# ------------------------------------------------------------
# 2. CREATE PATIENT TABLE
# ------------------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS Patient(
    Patient_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Phone TEXT,
    Email TEXT,
    Diagnosis TEXT
)
""")


# ------------------------------------------------------------
# 3. INSERT SAMPLE DIRTY RECORDS
# ------------------------------------------------------------

patients = [
    (1, "RAHUL kumar", 25, "male",
     "9876543210", "rahul@gmail.com", "Fever"),

    (2, "rahul KUMAR", 25, "Male",
     "9876543210", "rahul@gmail.com", "Fever"),

    (3, "Anita Devi", -5, "FEMALE",
     "98765", None, "Cold"),

    (4, "Suresh Rao", 135, "male",
     None, "suresh@gmail.com", "Diabetes"),

    (5, "Priya Sharma", 30, "female",
     "9123456789", "priya@gmail.com", "Fever")
]


cur.executemany("""
INSERT OR IGNORE INTO Patient
VALUES (?, ?, ?, ?, ?, ?, ?)
""", patients)

conn.commit()


# ------------------------------------------------------------
# 4. NAME NORMALIZATION
# ------------------------------------------------------------

def clean_name(name):
    if not name:
        return None

    return " ".join(
        name.strip().lower().split()
    ).title()


# ------------------------------------------------------------
# 5. PHONE VALIDATION USING REGEX
# ------------------------------------------------------------

def valid_phone(phone):
    if not phone:
        return False

    return bool(
        re.fullmatch(r"[6-9]\d{9}", phone)
    )


# ------------------------------------------------------------
# 6. EMAIL VALIDATION USING REGEX
# ------------------------------------------------------------

def valid_email(email):
    if not email:
        return False

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        )
    )


# ------------------------------------------------------------
# 7. AGE VALIDATION
# ------------------------------------------------------------

def valid_age(age):
    return age is not None and 0 <= age <= 120


# ------------------------------------------------------------
# 8. READ PATIENT RECORDS
# ------------------------------------------------------------

cur.execute("SELECT * FROM Patient")
rows = cur.fetchall()

cleaned = []
seen = set()


# ------------------------------------------------------------
# 9. DATA CLEANING
# ------------------------------------------------------------

for row in rows:

    pid, name, age, gender, phone, email, diagnosis = row

    # Normalize name
    name = clean_name(name)

    # Normalize gender
    gender = (
        gender.strip().lower().title()
        if gender else None
    )

    # Remove exact duplicate records
    key = (
        name,
        age,
        gender,
        phone,
        email,
        diagnosis
    )

    if key in seen:
        continue

    seen.add(key)

    # Validate phone
    if not valid_phone(phone):
        phone = None

    # Validate email
    if not valid_email(email):
        email = None

    # Validate age
    if not valid_age(age):
        age = None

    cleaned.append(
        (
            pid,
            name,
            age,
            gender,
            phone,
            email,
            diagnosis
        )
    )


# ------------------------------------------------------------
# 10. CREATE CLEAN_PATIENT TABLE
# ------------------------------------------------------------

cur.execute("DROP TABLE IF EXISTS Clean_Patient")

cur.execute("""
CREATE TABLE Clean_Patient(
    Patient_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Phone TEXT,
    Email TEXT,
    Diagnosis TEXT
)
""")


# ------------------------------------------------------------
# 11. INSERT CLEANED DATA
# ------------------------------------------------------------

cur.executemany("""
INSERT INTO Clean_Patient
VALUES (?, ?, ?, ?, ?, ?, ?)
""", cleaned)

conn.commit()


# ------------------------------------------------------------
# 12. FUZZY MATCHING
# ------------------------------------------------------------

def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


print("\n========================================")
print("POTENTIAL DUPLICATE PATIENTS")
print("========================================")


for i in range(len(cleaned)):

    for j in range(i + 1, len(cleaned)):

        n1 = cleaned[i][1]
        n2 = cleaned[j][1]

        if (
            n1 and
            n2 and
            similarity(n1, n2) >= 0.85
        ):
            print(
                cleaned[i][0],
                "<->",
                cleaned[j][0]
            )


# ------------------------------------------------------------
# 13. SELECT OPERATION
# ------------------------------------------------------------

print("\n========================================")
print("CLEAN PATIENT RECORDS")
print("========================================")

cur.execute("""
SELECT * FROM Clean_Patient
""")

for row in cur.fetchall():
    print(row)


# ------------------------------------------------------------
# 14. UPDATE OPERATION
# ------------------------------------------------------------

cur.execute("""
UPDATE Clean_Patient
SET Diagnosis = 'General Checkup'
WHERE Diagnosis IS NULL
""")


# ------------------------------------------------------------
# 15. DELETE OPERATION
# ------------------------------------------------------------

cur.execute("""
DELETE FROM Clean_Patient
WHERE Age IS NULL
AND Phone IS NULL
AND Email IS NULL
""")


conn.commit()


# ------------------------------------------------------------
# 16. FINAL MESSAGE
# ------------------------------------------------------------

print("\n========================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("========================================")


# ------------------------------------------------------------
# 17. CLOSE DATABASE CONNECTION
# ------------------------------------------------------------

conn.close()
