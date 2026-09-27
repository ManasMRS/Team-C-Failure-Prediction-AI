from database import get_connection

try:
    connection = get_connection()
    print("✅ Database connected successfully!")

    cursor = connection.cursor()

    cursor.execute("SELECT current_database();")
    print("Database:", cursor.fetchone()[0])

    cursor.execute("SELECT * FROM projects;")
    rows = cursor.fetchall()

    print("Projects stored in database:")
    for row in rows:
        print(row)

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Database connection failed:")
    print(e)