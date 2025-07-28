import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from environment
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'tofico_analyzer'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': True
}

def get_db_connection():
    """Buat koneksi ke database MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise e

def init_database():
    """Inisialisasi database dan tabel"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Read and execute create database script
        with open('scripts/create_database_normalized.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Split and execute each statement
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)
        
        print("Database tables created successfully!")
        
        # Insert sample data
        with open('scripts/seed_data_normalized.sql', 'r', encoding='utf-8') as file:
            seed_script = file.read()
            
        statements = seed_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)
        
        print("Sample data inserted successfully!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error initializing database: {e}")
        raise e

def test_connection():
    """Test database connection"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except Error as e:
        print(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("✅ Database connection successful!")
        init_database()
    else:
        print("❌ Database connection failed!")
