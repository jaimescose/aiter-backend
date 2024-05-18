import sqlite3

# List of keywords
keywords = [
{"name": "ERITROCITOS", "unit": "10^6/uL", "min_value": 4.5, "max_value": 6.5},
{"name": "HEMOGLOBINA", "unit": "g/dL", "min_value": 13.0, "max_value": 18.0},
{"name": "HEMATOCRITO", "unit": "%", "min_value": 40.0, "max_value": 54.0},
{"name": "VCM", "unit": "fL", "min_value": 80.0, "max_value": 100.0},
{"name": "CHM", "unit": "pg", "min_value": 27.0, "max_value": 33.0},
{"name": "CHCM", "unit": "g/dL", "min_value": 32.0, "max_value": 36.0},
{"name": "ADE", "unit": "%", "min_value": 11.5, "max_value": 14.5},
{"name": "PLAQUETAS", "unit": "10^3/uL", "min_value": 150.0, "max_value": 450.0},
{"name": "LEUCOCITOS", "unit": "10^3/uL", "min_value": 4.0, "max_value": 11.0},
{"name": "VPM", "unit": "fL", "min_value": 7.0, "max_value": 11.0},
{"name": "NEUTROFILOS", "unit": "%", "min_value": 40.0, "max_value": 70.0},
{"name": "EOSINOFILOS", "unit": "%", "min_value": 0.0, "max_value": 5.0},
{"name": "BASOFILOS", "unit": "%", "min_value": 0.0, "max_value": 2.0},
{"name": "LINFOCITOS", "unit": "%", "min_value": 20.0, "max_value": 40.0},
{"name": "MONOCITOS", "unit": "%", "min_value": 2.0, "max_value": 10.0},
{"name": "NEUTROFILOS", "unit": "10^3/uL", "min_value": 2.0, "max_value": 7.5},
{"name": "EOSINOFILOS", "unit": "10^3/uL", "min_value": 0.0, "max_value": 0.5},
{"name": "BASOFILOS", "unit": "10^3/uL", "min_value": 0.0, "max_value": 0.2},
{"name": "LINFOCITOS", "unit": "10^3/uL", "min_value": 1.0, "max_value": 4.0},
{"name": "MONOCITOS", "unit": "10^3/uL", "min_value": 0.1, "max_value": 1.0},
{"name": "NITROGENO", "unit": "mg/dL", "min_value": 7.0, "max_value": 20.0},
{"name": "SICLEMIA", "unit": "mg/dL", "min_value": 70.0, "max_value": 99.0},
{"name": "GLOMERULAR", "unit": "mL/min/1.73m^2", "min_value": 90.0, "max_value": 120.0},
{"name": "COLESTEROL", "unit": "mg/dL", "min_value": 0.0, "max_value": 200.0},
{"name": "TRIGLICERIDOS", "unit": "mg/dL", "min_value": 0.0, "max_value": 150.0},
{"name": "ALANINO", "unit": "U/L", "min_value": 7.0, "max_value": 55.0},
{"name": "ASPARTATO", "unit": "U/L", "min_value": 8.0, "max_value": 48.0},
{"name": "AMILASA", "unit": "U/L", "min_value": 40.0, "max_value": 140.0},
{"name": "LIPASA", "unit": "U/L", "min_value": 0.0, "max_value": 160.0},
{"name": "HORMONAS", "unit": "mIU/L", "min_value": 0.4, "max_value": 4.0},
{"name": "TSH", "unit": "mIU/L", "min_value": 0.4, "max_value": 4.0},
{"name": "INSULINA", "unit": "uIU/mL", "min_value": 2.6, "max_value": 24.9},
{"name": "PROTEINAS", "unit": "g/dL", "min_value": 6.0, "max_value": 8.3},
{"name": "PROTEINA", "unit": "g/dL", "min_value": 6.0, "max_value": 8.3},
{"name": "CREATININA", "unit": "mg/dL", "min_value": 0.6, "max_value": 1.2},
{"name": "ERITROSEDIMENTACION", "unit": "mm/h", "min_value": 0.0, "max_value": 20.0},
{"name": "TESTOSTERONA", "unit": "ng/dL", "min_value": 300.0, "max_value": 1000.0}
]

# SQLite database file
db_file = 'database.db'

def create_table(conn):
    """Create a table in the database."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY,
            name TEXT,
            unit TEXT,
            min_value NUMERIC,
            max_value NUMERIC
        )
    ''')
    conn.commit()

def insert_keywords(conn, keywords_data):
    """Insert keywords into the database."""
    cursor = conn.cursor()
    for data in keywords_data:
        cursor.execute('''
            INSERT INTO keywords (name, unit, min_value, max_value)
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['unit'], data['min_value'], data['max_value']))
    conn.commit()

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create table
    create_table(conn)

    # Insert keywords
    insert_keywords(conn, keywords)

    # Close the connection
    conn.close()
    print("Database created and filled successfully!")

if __name__ == "__main__":
    main()
