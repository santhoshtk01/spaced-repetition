import mysql.connector

cursor = None
configuration = {
    'user': 'root',
    'password': 'Mysql0011@',
    'host': 'localhost',
    'database': 're_iterator'
}

try:
    connection = mysql.connector.connect(**configuration)
    print("Connection successful.")
except Exception as error:
    print(error)
else:
    cursor = connection.cursor(buffered=True)


def commit():
    connection.commit()
    connection.close()
    print('Connection closed successfully.')

