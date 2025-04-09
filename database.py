import sqlite3

def create_table():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def mark_attendance(name):
    from datetime import datetime
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Avoid duplicate entries per day (optional)
    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        conn.commit()
        print(f"✅ Attendance marked for {name} at {time}")
    else:
        print(f"🕒 {name} is already marked present today.")

    conn.close()
