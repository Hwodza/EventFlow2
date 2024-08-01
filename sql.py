import mysql.connector
from mysql.connector import Error

def connect_to_database(host, port, database, user, password):
    try:
        connection = mysql.connector.connect(
            host='172.234.204.179',
            port=3306,
            database='eventflowdb',
            user='remote_eventflow',
            password='eventPassword'
        )
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error: {e}")
        return None

def main():
    host = 'localhost'
    port = 3306
    database = 'your_database_name'
    user = 'your_database_user'
    password = 'your_database_password'

    connection = connect_to_database(host, port, database, user, password)

    if not connection:
        return

    query = """
SELECT 
    event.event_id,
    event.event_name,
    event.event_date,
    event.event_description,
    budget.total_budget,
    budget.remaining_budget
FROM 
    event,
    allocated,
    budget
WHERE 
    event.event_id = allocated.event_id
    AND allocated.budget_id = budget.budget_id
    AND budget.remaining_budget < 1000;

    """

    print(f"Executing query: {query}")
    results = execute_query(connection, query)
    if results:
        for row in results:
            print(row)

    if connection.is_connected():
        connection.close()
        print("Database connection closed")

if __name__ == '__main__':
    main()
