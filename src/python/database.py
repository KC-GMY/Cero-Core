import sqlite3
import os
from datetime import date
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
TABLES = {"kHz": "kHz", "MHz": "MHz", "GHz": "GHz", "Ir": "Ir"}

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_connection() as conn:
        cursor= conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kHz(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                tag_hex TEXT NOT NULL,
                tag_dec INTEGER NOT NULL,
                checksum_hex TEXT NOT NULL,
                checksum_valid BOOLEAN NOT NULL,
                date DATE)''') # 'YYYY-MM-DD' or #MM/DD/YYYY#
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MHz(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                UID TEXT,
                PICC_type TEXT,
                date DATE)''') # 'YYYY-MM-DD' or #MM/DD/YYYY#
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS GHz(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                data TEXT,
                date DATE)''') # 'YYYY-MM-DD' or #MM/DD/YYYY#
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ir(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                hex_data TEXT,
                date DATE)''') # 'YYYY-MM-DD' or #MM/DD/YYYY#
        conn.commit()
    
def save_reading(tool, name, data):
    if tool not in TABLES:
        raise ValueError("Unknown tool")
    with get_connection() as conn:
        cursor = conn.cursor()
        if tool=="kHz":
            parts=data.split(sep="\n", maxsplit=3)
            if parts[3]=="True":
                Val_CheckSum=True
            else:
                Val_CheckSum=False
            try:
                cursor.execute(
                "INSERT INTO kHz (name,tag_hex,tag_dec,checksum_hex,checksum_valid,date) VALUES (?,?,?,?,?,?)",
                (name,parts[0],parts[2],parts[1],Val_CheckSum, date.today().isoformat()))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        newname = f"{name}({i})"
                        cursor.execute(
                        "INSERT INTO kHz (name,tag_hex,tag_dec,checksum_hex,checksum_valid,date) VALUES (?,?,?,?,?,?)",
                        (newname,parts[0],parts[2],parts[1],Val_CheckSum, date.today().isoformat()))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="MHz":
            parts=data.split(sep="\n", maxsplit=1)
            if len(parts) < 2:
                raise ValueError(f"Invalid data format for MHz. Got: {data!r}")
            try:
                cursor.execute(
                    "INSERT INTO MHz (name,UID,PICC_type,date) VALUES (?,?,?,?)",
                    (name,parts[0],parts[1],date.today().isoformat()))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        newname = f"{name}({i})"
                        cursor.execute(
                        "INSERT INTO MHz (name,UID,PICC_type,date) VALUES (?,?,?,?)",
                        (newname,parts[0],parts[1],date.today().isoformat()))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="GHz":
            try:
                cursor.execute(
                "INSERT INTO GHz (name, data, date) VALUES (?, ?, ?)",
                (name, data, date.today().isoformat()))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        newname = f"{name}({i})"
                        cursor.execute(
                        "INSERT INTO GHz (name, data, date) VALUES (?, ?, ?)",
                        (newname, data, date.today().isoformat()))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="Ir":
            try:
                cursor.execute(
                "INSERT INTO Ir (name, hex_data, date) VALUES (?, ?, ?)",
                (name, data, date.today().isoformat()))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        newname = f"{name}({i})"
                        cursor.execute(
                        "INSERT INTO Ir (name, hex_data, date) VALUES (?, ?, ?)",
                        (newname, data, date.today().isoformat()))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        conn.commit()                

def delete_reading(tool, name):
    if tool not in TABLES:
        raise ValueError("Unknown tool")

    table = TABLES[tool]
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE name=?", (name,))
        conn.commit()

def get_reading(tool):
    if tool not in TABLES:
        raise ValueError("Unknown tool")

    table = TABLES[tool]
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM {table}")
        return cursor.fetchall()

def change_name(tool,oldname,newname):
    if tool not in TABLES:
        raise ValueError("Unknown tool")
    with get_connection() as conn:
        cursor= conn.cursor()
        if tool=="kHz":
            try:
                cursor.execute("UPDATE kHz SET name=? WHERE name=?",(newname,oldname))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        altname = f"{newname}({i})"
                        cursor.execute("UPDATE kHz SET name=? WHERE name=?",(altname,oldname))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="MHz":
            try:
                cursor.execute("UPDATE MHz SET name=? WHERE name=?",(newname,oldname))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        altname = f"{newname}({i})"
                        cursor.execute("UPDATE MHz SET name=? WHERE name=?",(altname,oldname))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="GHz":
            try:
                cursor.execute("UPDATE GHz SET name=? WHERE name=?",(newname,oldname))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        altname = f"{newname}({i})"
                        cursor.execute("UPDATE GHz SET name=? WHERE name=?",(altname,oldname))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        elif tool=="Ir":
            try:
                cursor.execute("UPDATE Ir SET name=? WHERE name=?",(newname,oldname))
            except sqlite3.IntegrityError:
                i=1
                while True:
                    try:
                        altname = f"{newname}({i})"
                        cursor.execute("UPDATE Ir SET name=? WHERE name=?",(altname,oldname))
                        break
                    except sqlite3.IntegrityError:
                        i+=1
        conn.commit()

def drop_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        for table in TABLES.values():
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        conn.commit()

def get_data(tool,name):
    if tool not in TABLES:
        raise ValueError("Unknown tool")
    with get_connection() as conn:
        cursor=conn.cursor()
        if tool=="kHz":
            cursor.execute("SELECT tag_hex,tag_dec,checksum_hex,checksum_valid,date FROM kHz WHERE name=?",(name,))
        elif tool=="MHz":
            cursor.execute("SELECT UID,PICC_type,date FROM MHz WHERE name=?",(name,))
        elif tool=="GHz":
            cursor.execute("SELECT data,date FROM GHz WHERE name=?",(name,))
        elif tool=="Ir":
            cursor.execute("SELECT hex_data,date FROM Ir WHERE name=?",(name,))
        return cursor.fetchall()