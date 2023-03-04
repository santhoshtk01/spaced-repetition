import mysql.connector


cursor = None

configuration = {
    'user': 'root',
    'password': 'Mysql0011@',
    'host': 'localhost',
    'database': 're_iterator'
}


# Make a new connection with the above configuration.
try:
    connection = mysql.connector.connect(**configuration)
    print("Connection successful.")
except Exception as error:
    print(error)
else:
    cursor = connection.cursor(buffered=True)


def commit():
    """To make commit to the database to make the changes permanently."""
    connection.commit()
    connection.close()
    print('Connection closed successfully.')

