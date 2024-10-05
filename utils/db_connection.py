import mysql.connector
from mysql.connector import Error
import json

def create_connection():
    try:
        # Load connection configuration from JSON file
        with open('utils/db_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Establish the connection
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection

    except Error as e:
        print(f"Error: '{e}' occurred")
        return None

# Example usage:
if __name__ == '__main__':
    db_connection = create_connection()
