import mysql.connector
import os 
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT'))}

def extract_data(output_csv='data/pagespeed_data.csv', chunk_size=1000):
    print("Connecting to the database...")
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True, buffered=False) as cursor:
                query = """
                SELECT *
                FROM pagespeed_results
                ORDER BY fetch_time DESC
                """
                cursor.execute(query)
                first_chunk = True
                os.makedirs(os.path.dirname(output_csv), exist_ok=True)
                while True:
                    rows = cursor.fetchmany(chunk_size)
                    if not rows:
                        break
                    df = pd.DataFrame(rows)
                    df.to_csv(output_csv, mode='w' if first_chunk else 'a', header=first_chunk, index=False)
                    if first_chunk:
                        print(f"Fetched {len(rows)} rows (first chunk) from the database.")
                        first_chunk = False
                print(f"Data saved to {output_csv}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    extract_data()
    print("Data extraction completed.")