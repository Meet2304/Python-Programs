import streamlit as st
import sqlite3
import pandas as pd
import hashlib

# Connect to SQLite database
conn = sqlite3.connect('hotel.db')
c = conn.cursor()

# Create tables if not exists
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS Guests (
                GuestID INTEGER PRIMARY KEY,
                Name TEXT,
                ContactInfo TEXT,
                Address TEXT,
                Nationality TEXT,
                Password TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Rooms (
                RoomID INTEGER PRIMARY KEY,
                RoomNumber TEXT,
                RoomType TEXT,
                Description TEXT,
                Rate REAL,
                Status TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                ReservationID INTEGER PRIMARY KEY,
                GuestID INTEGER,
                RoomID INTEGER,
                CheckInDate TEXT,
                CheckOutDate TEXT,
                TotalCost REAL,
                Status TEXT,
                FOREIGN KEY(GuestID) REFERENCES Guests(GuestID),
                FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Staff (
                StaffID INTEGER PRIMARY KEY,
                Name TEXT,
                Position TEXT,
                ContactInfo TEXT,
                Department TEXT,
                Salary REAL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Services (
                ServiceID INTEGER PRIMARY KEY,
                ServiceName TEXT,
                Description TEXT,
                Cost REAL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Payments (
                PaymentID INTEGER PRIMARY KEY,
                GuestID INTEGER,
                ReservationID INTEGER,
                PaymentDate TEXT,
                Amount REAL,
                PaymentMethod TEXT,
                FOREIGN KEY(GuestID) REFERENCES Guests(GuestID),
                FOREIGN KEY(ReservationID) REFERENCES Reservations(ReservationID)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS RoomInventory (
                InventoryID INTEGER PRIMARY KEY,
                RoomID INTEGER,
                ItemName TEXT,
                Quantity INTEGER,
                Description TEXT,
                FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS RoomTypes (
                RoomTypeID INTEGER PRIMARY KEY,
                RoomType TEXT,
                Description TEXT,
                Capacity INTEGER,
                Rate REAL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS RoomBookings (
                BookingID INTEGER PRIMARY KEY,
                RoomID INTEGER,
                BookingDate TEXT,
                Status TEXT,
                FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Feedback (
                FeedbackID INTEGER PRIMARY KEY,
                GuestID INTEGER,
                ReservationID INTEGER,
                FeedbackDescription TEXT,
                Rating INTEGER,
                FOREIGN KEY(GuestID) REFERENCES Guests(GuestID),
                FOREIGN KEY(ReservationID) REFERENCES Reservations(ReservationID)
                )''')

create_tables()

# Function to display data from a selected table
def display_table(table_name):
    c.execute(f"SELECT * FROM {table_name}")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=[x[0] for x in c.description])
    return df

# Function to add data to a table
def add_data(table_name, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    c.execute(sql, tuple(data.values()))
    conn.commit()

# Function to update data in a table
def update_data(table_name, set_values, condition):
    set_clause = ', '.join([f"{key} = ?" for key in set_values.keys()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
    c.execute(sql, tuple(set_values.values()))
    conn.commit()

# Function to delete data from a table
def delete_data(table_name, condition):
    sql = f"DELETE FROM {table_name} WHERE {condition}"
    c.execute(sql)
    conn.commit()

# Function to check if username already exists
def check_username_exists(username):
    c.execute("SELECT * FROM Guests WHERE Name=?", (username,))
    data = c.fetchone()
    if data:
        return True
    else:
        return False

# Sign-up Page
def signup():
    st.title("Sign Up")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Sign Up'):
        if not check_username_exists(username):
            guest_data = {'Name': username, 'ContactInfo': '', 'Address': '', 'Nationality': ''}
            add_data('Guests', guest_data)
            st.success('Sign up successful! You can now log in.')
        else:
            st.error('Username already exists. Please choose a different username.')

# Login Page
def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hashing the password

    # Query the database to check if the username and hashed password match
    c.execute("SELECT * FROM Guests WHERE Name=? AND Password=?", (username, hashed_password))
    user = c.fetchone()

    if user:
        return user  # Return user data if login is successful
    else:
        return None  # Return None if login fails


# User Panel
def user_panel():
    st.title('User Panel')
    st.write("Welcome to the User Panel. Here, you can book a room and manage your reservations.")
    # Booking Form
    st.subheader("Book a Room")
    name = st.text_input('Name', help='Enter your name')
    phone_number = st.text_input('Phone Number', help='Enter your phone number')
    num_people = st.number_input('Number of People', min_value=1, value=1, help='Enter the number of people')
    duration_of_stay = st.number_input('Duration of Stay (days)', min_value=1, value=1, help='Enter the duration of stay in days')
    room_type = st.selectbox('Room Type', ['Single', 'Double', 'Suite'], help='Select the type of room')
    book_button = st.button('Book Room')

    if book_button:
        # Here you can add code to process the booking
        st.success('Room booked successfully!')

    # Reservation Management
    st.subheader("Manage Reservations")
    # Here you can display the user's reservations and provide options to modify or cancel them

# Admin Panel
def admin_panel():
    st.title('Admin Panel')
    st.write("Welcome to the Admin Panel. Here, you can manage the hotel's operations.")
    selected_table = st.selectbox('Select Table', ['Guests', 'Rooms', 'Reservations', 'Staff', 'Services', 'Payments', 'RoomInventory', 'RoomTypes', 'RoomBookings', 'Feedback'])
    st.write(display_table(selected_table))

    # Data manipulation options
    st.subheader("Data Manipulation")
    add_button = st.button("Add Data")
    if add_button:
        add_form(selected_table)
    
    update_button = st.button("Update Data")
    if update_button:
        update_form(selected_table)
    
    delete_button = st.button("Delete Data")
    if delete_button:
        delete_form(selected_table)

# Add, update, delete forms
def add_form(table_name):
    st.subheader(f"Add Data to {table_name}")
    # Define form fields based on table structure
    if table_name == 'Guests':
        name = st.text_input('Name')
        contact_info = st.text_input('Contact Information')
        address = st.text_input('Address')
        nationality = st.text_input('Nationality')
        if st.button('Add Guest'):
            guest_data = {'Name': name, 'ContactInfo': contact_info, 'Address': address, 'Nationality': nationality}
            add_data(table_name, guest_data)
            st.success('Guest added successfully!')

    # Add forms for other tables similarly...

def update_form(table_name):
    st.subheader(f"Update Data in {table_name}")
    # Define form fields based on table structure
    if table_name == 'Guests':
        guest_id = st.number_input('Guest ID')
        name = st.text_input('Name')
        contact_info = st.text_input('Contact Information')
        address = st.text_input('Address')
        nationality = st.text_input('Nationality')
        if st.button('Update Guest'):
            set_values = {'Name': name, 'ContactInfo': contact_info, 'Address': address, 'Nationality': nationality}
            update_data(table_name, set_values, f'GuestID = {guest_id}')
            st.success('Guest updated successfully!')

    # Add forms for other tables similarly...

def delete_form(table_name):
    st.subheader(f"Delete Data from {table_name}")
    # Define form fields based on table structure
    if table_name == 'Guests':
        guest_id = st.number_input('Guest ID')
        if st.button('Delete Guest'):
            delete_data(table_name, f'GuestID = {guest_id}')
            st.success('Guest deleted successfully!')

    # Add forms for other tables similarly...

def main():
    st.title('Hotel Management System')
    username, password = get_login_credentials()  # Function to get username and password from user input
    user_data = login(username, password)
    if user_data:
        role = user_data['Role']  # Assuming user role is stored in the database
        if role == 'admin':
            admin_panel()
        elif role == 'user':
            user_panel()
        else:
            st.error('Invalid role')
    else:
        st.error('Invalid username or password')


if __name__ == '__main__':
    main()
