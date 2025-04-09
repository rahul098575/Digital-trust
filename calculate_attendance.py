import sqlite3

def calculate_attendance():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Count records per person
    cursor.execute("""
        SELECT name, COUNT(DISTINCT date) AS days_present
        FROM attendance
        GROUP BY name
    """)

    results = cursor.fetchall()

    print("📊 Attendance Summary:")
    for name, count in results:
        print(f"👤 {name} was present on {count} day(s)")

    conn.close()

if __name__ == "__main__":
    calculate_attendance()
