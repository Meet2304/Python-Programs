import streamlit as st
import sqlite3
import pandas as pd

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('gym.db')
    return conn

# Function to create tables if they don't exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Gym (
                        Gym_ID INTEGER PRIMARY KEY,
                        Name TEXT,
                        Address TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Gym_Member (
                        Gym_Member_ID INTEGER PRIMARY KEY,
                        First_Name TEXT,
                        Last_Name TEXT,
                        Phone_Number TEXT,
                        Email_ID TEXT,
                        Username TEXT UNIQUE,
                        Password TEXT,
                        Age INTEGER,
                        Address TEXT,
                        City TEXT,
                        Membership_Type TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Instructor (
                        Instructor_ID INTEGER PRIMARY KEY,
                        First_Name TEXT,
                        Last_Name TEXT,
                        Phone_Number TEXT,
                        Email_ID TEXT,
                        Username TEXT UNIQUE,
                        Password TEXT,
                        Age INTEGER,
                        Address TEXT,
                        City TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exercise (
                        Exercise_ID INTEGER PRIMARY KEY,
                        Exercise_Types TEXT UNIQUE
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Diet_Plan (
                        Diet_Plan_ID INTEGER PRIMARY KEY,
                        Diet_Types TEXT UNIQUE
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Membership (
                        Membership_ID INTEGER PRIMARY KEY,
                        Membership_Type TEXT,
                        Instructor_ID INTEGER,
                        Cost REAL,
                        Timing TEXT,
                        Date DATE,
                        FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Management_Staff (
                        Management_Staff_ID INTEGER PRIMARY KEY,
                        First_Name TEXT,
                        Last_Name TEXT,
                        Phone_Number TEXT,
                        Email_ID TEXT,
                        Username TEXT UNIQUE,
                        Password TEXT,
                        Age INTEGER,
                        Address TEXT,
                        City TEXT,
                        Salary INTEGER
                    )''')
    conn.commit()
    conn.close()

# Function to fetch data from a table
def fetch_data(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()
    return data, column_names

# Function to add data to a table
def add_data(table_name, values):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(values))})", values)
    conn.commit()
    conn.close()

# Function to delete data from a table
def delete_data(table_name, primary_key):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE {table_name}_ID=?", (primary_key,))
        conn.commit()
        st.success(f"Data deleted successfully from {table_name}!")
    except sqlite3.Error as e:
        st.error(f"Error deleting data from {table_name}: {e}")
    finally:
        conn.close()



# Function to update data in a table
def update_data(table_name, primary_key, column, new_value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET {column}=? WHERE {table_name}_ID=?", (new_value, primary_key))
    conn.commit()
    conn.close()    

# Main function to run the Streamlit app
def main():
    create_tables()

    st.title("Gym Management System")

    operation = st.selectbox("Select Operation", ["Add", "Delete", "Update"])
    table = st.selectbox("Select Table", ["Gym", "Gym Member", "Instructor", "Exercise", "Diet Plan", "Membership", "Management Staff"])

    if operation == "Add":
        st.header(f"Add New {table}")
        if table == "Gym":
            name = st.text_input("Enter Name")
            address = st.text_input("Enter Address")
            if st.button("Add"):
                add_data("Gym", (None, name, address))
                st.success("Gym added successfully!")
        elif table == "Gym Member":
            first_name = st.text_input("Enter First Name")
            last_name = st.text_input("Enter Last Name")
            phone_number = st.text_input("Enter Phone Number")
            email_id = st.text_input("Enter Email ID")
            username = st.text_input("Enter Username")
            password = st.text_input("Enter Password", type="password")
            age = st.number_input("Enter Age", min_value=18, max_value=100)
            address = st.text_input("Enter Address")
            city = st.text_input("Enter City")
            membership_type = st.text_input("Enter Membership Type")
            if st.button("Add"):
                add_data("Gym_Member", (None, first_name, last_name, phone_number, email_id, username, password, age, address, city, membership_type))
                st.success("Gym Member added successfully!")
        elif table == "Instructor":
            first_name = st.text_input("Enter First Name")
            last_name = st.text_input("Enter Last Name")
            phone_number = st.text_input("Enter Phone Number")
            email_id = st.text_input("Enter Email ID")
            username = st.text_input("Enter Username")
            password = st.text_input("Enter Password", type="password")
            age = st.number_input("Enter Age", min_value=18, max_value=100)
            address = st.text_input("Enter Address")
            city = st.text_input("Enter City")
            if st.button("Add"):
                add_data("Instructor", (None, first_name, last_name, phone_number, email_id, username, password, age, address, city))
                st.success("Instructor added successfully!")
        elif table == "Exercise":
            Exercise_type = st.text_input("Enter Exercise Type")
            if st.button("Add"):
                add_data("Exercise", (None, Exercise_type))
                st.success("Exercise added successfully!")
        elif table == "Diet Plan":
            Diet_Type = st.text_input("Enter Diet Type")
            if st.button("Add"):
                add_data("Diet_Plan", (None, Diet_Type))
                st.success("Diet Plan added successfully!")
        elif table == "Membership":
            membership_type = st.text_input("Enter Membership Type")
            instructor_id = st.number_input("Enter Instructor ID", min_value=1)
            cost = st.number_input("Enter Cost", min_value=0.0)
            timing = st.text_input("Enter Timing")
            date = st.date_input("Enter Date")
            if st.button("Add"):
                add_data("Membership", (None, membership_type, instructor_id, cost, timing, date))
                st.success("Membership added successfully!")
        elif table == "Management Staff":
            first_name = st.text_input("Enter First Name")
            last_name = st.text_input("Enter Last Name")
            phone_number = st.text_input("Enter Phone Number")
            email_id = st.text_input("Enter Email ID")
            username = st.text_input("Enter Username")
            password = st.text_input("Enter Password", type="password")
            age = st.number_input("Enter Age", min_value=18, max_value=100)
            address = st.text_input("Enter Address")
            city = st.text_input("Enter City")
            salary = st.number_input("Enter Salary")
            if st.button("Add"):
                add_data("Management_Staff", (None, first_name, last_name, phone_number, email_id, username, password, age, address, city, salary))
                st.success("Management Staff added successfully!")

    
    elif operation == "Delete":
        st.header(f"Delete {table}")
        data, column_names = fetch_data(table.replace(" ", "_"))
        data_dict = {item[0]: item[1:] for item in data}
        primary_key = st.selectbox(f"Select {table[:-1]} to Delete", list(data_dict.keys()))
        if st.button("Delete"):
            delete_data(table.replace(" ", "_"), primary_key)
            st.success(f"{table[:-1]} deleted successfully!")

    elif operation == "Update":
        st.header(f"Update {table}")
        data, column_names = fetch_data(table.replace(" ", "_"))
        data_dict = {item[0]: item[1:] for item in data}
        primary_key = st.selectbox(f"Select {table[:-1]} to Update", list(data_dict.keys()))
        column = st.selectbox("Select Column to Update", [col for col in column_names if col != f"{table}_ID"])
        new_value = st.text_input(f"Enter New Value for {column}")
        if st.button("Update"):
            update_data(table.replace(" ", "_"), primary_key, column, new_value)
            st.success(f"{table[:-1]} updated successfully!")

    st.header(f"{table} Table")
    data, column_names = fetch_data(table.replace(" ", "_"))
    if data:
        df = pd.DataFrame(data, columns=column_names)
        st.table(df)
    else:
        st.write("No data available for this table.")

if __name__ == "__main__":
    main()
