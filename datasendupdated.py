import pymysql
import csv

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'shubhanshu@1912'
DB_NAME = 'orgassistupdate'

def insert_qa_data_into_database(data):
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()

    try:
        # Insert data into the database
        for question, answer in data:
            cursor.execute("INSERT INTO qadataset (question, answer) VALUES (%s, %s)", (question, answer))
        
        # Commit changes
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print("Error:", e)
    finally:
        # Close connection
        connection.close()

def read_csv_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if present
        for row in csv_reader:
            data.append((row[0], row[1]))  # Assuming the CSV has two columns: question and answer
    return data

if __name__ == "__main__":
    csv_file_path = "qaorgassit.csv"  # Replace with the actual path to your CSV file
    data_to_insert = read_csv_data(csv_file_path)
    insert_qa_data_into_database(data_to_insert)
