import sqlite3
import pandas as pd

def export_to_excel():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Fetch all data
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['ID', 'Name', 'Date', 'Time'])

    # Export to Excel
    df.to_excel("attendance.xlsx", index=False)
    print("✅ Attendance exported to 'attendance.xlsx' successfully!")

    conn.close()

if __name__ == "__main__":
    export_to_excel()
