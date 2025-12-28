import mysql.connector

host = "localhost"
user = "root"
password = "root"
database = "internship_db"

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    print("Connected to MySQL database !!")
    
    cursor = conn.cursor()
    
    cursor.execute("Show tables")
    tables = cursor.fetchall()
    print("Tables in databases: ", tables)
    
    cursor.execute("SELECT * FROM employees WHERE department = 'Sales'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    cursor.close()
    conn.close()
    print("Connection closed.")
    
            
except mysql.connector.Error as err:
    print("Error: ", err)    