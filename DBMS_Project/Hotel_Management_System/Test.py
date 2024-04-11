import streamlit as st
import sqlite3
import hashlib

# Create a connection to the SQLite database
conn = sqlite3.connect('hotel.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS customers
             (id INTEGER PRIMARY KEY, 
             username TEXT, 
             password TEXT,
             role TEXT)''')

# Create Guests Table
c.execute('''CREATE TABLE IF NOT EXISTS guests
             (id INTEGER PRIMARY KEY, 
             name TEXT, 
             contact_info TEXT,
             address TEXT,
             nationality TEXT,
             other_details TEXT)''')

# Create Rooms Table
c.execute('''CREATE TABLE IF NOT EXISTS rooms
             (id INTEGER PRIMARY KEY, 
             room_number INTEGER,
             room_type TEXT,
             description TEXT,
             rate REAL,
             status TEXT)''')

# Create Reservations Table
c.execute('''CREATE TABLE IF NOT EXISTS reservations
             (id INTEGER PRIMARY KEY, 
             guest_id INTEGER,
             room_id INTEGER,
             check_in_date DATE,
             check_out_date DATE,
             total_cost REAL,
             status TEXT,
             FOREIGN KEY(guest_id) REFERENCES guests(id),
             FOREIGN KEY(room_id) REFERENCES rooms(id))''')

# Create Staff Table
c.execute('''CREATE TABLE IF NOT EXISTS staff
             (id INTEGER PRIMARY KEY, 
             name TEXT,
             position TEXT,
             contact_info TEXT,
             department TEXT,
             salary REAL)''')

# Create Services Table
c.execute('''CREATE TABLE IF NOT EXISTS services
             (id INTEGER PRIMARY KEY, 
             service_name TEXT,
             description TEXT,
             cost REAL)''')

# Create Payments Table
c.execute('''CREATE TABLE IF NOT EXISTS payments
             (id INTEGER PRIMARY KEY, 
             guest_id INTEGER,
             reservation_id INTEGER,
             payment_date DATE,
             amount REAL,
             payment_method TEXT,
             FOREIGN KEY(guest_id) REFERENCES guests(id),
             FOREIGN KEY(reservation_id) REFERENCES reservations(id))''')

# Create Room Inventory Table
c.execute('''CREATE TABLE IF NOT EXISTS room_inventory
             (id INTEGER PRIMARY KEY, 
             room_id INTEGER,
             item_name TEXT,
             quantity INTEGER,
             description TEXT,
             FOREIGN KEY(room_id) REFERENCES rooms(id))''')

# Create Room Types Table
c.execute('''CREATE TABLE IF NOT EXISTS room_types
             (id INTEGER PRIMARY KEY, 
             room_type TEXT,
             description TEXT,
             capacity INTEGER,
             rate REAL)''')

# Create Room Bookings Table
c.execute('''CREATE TABLE IF NOT EXISTS room_bookings
             (id INTEGER PRIMARY KEY, 
             room_id INTEGER,
             booking_date DATE,
             status TEXT,
             FOREIGN KEY(room_id) REFERENCES rooms(id))''')

# Create Feedback Table
c.execute('''CREATE TABLE IF NOT EXISTS feedback
             (id INTEGER PRIMARY KEY, 
             guest_id INTEGER,
             reservation_id INTEGER,
             feedback_description TEXT,
             rating INTEGER,
             FOREIGN KEY(guest_id) REFERENCES guests(id),
             FOREIGN KEY(reservation_id) REFERENCES reservations(id))''')


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a customer
def add_customer(username, password, role):
    hashed_password = hash_password(password)
    c.execute("INSERT INTO customers (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()

# Function to check if a user exists
def check_user(username, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM customers WHERE username=? AND password=?", (username, hashed_password))
    return c.fetchone()

# Function to display tables for admin
def display_tables():
    selected_table = st.sidebar.selectbox("Select Table", ("Guests", "Rooms", "Reservations", "Staff", "Services", "Payments", "Room Inventory", "Room Types", "Room Bookings", "Feedback"))

    if selected_table == "Guests":
        st.subheader("Guests")
        guests_data = c.execute("SELECT * FROM guests").fetchall()
        st.table(guests_data)
    elif selected_table == "Rooms":
        st.subheader("Rooms")
        rooms_data = c.execute("SELECT * FROM rooms").fetchall()
        st.table(rooms_data)
    elif selected_table == "Reservations":
        st.subheader("Reservations")
        reservations_data = c.execute("SELECT * FROM reservations").fetchall()
        st.table(reservations_data)
    elif selected_table == "Staff":
        st.subheader("Staff")
        staff_data = c.execute("SELECT * FROM staff").fetchall()
        st.table(staff_data)
    elif selected_table == "Services":
        st.subheader("Services")
        services_data = c.execute("SELECT * FROM services").fetchall()
        st.table(services_data)
    elif selected_table == "Payments":
        st.subheader("Payments")
        payments_data = c.execute("SELECT * FROM payments").fetchall()
        st.table(payments_data)
    elif selected_table == "Room Inventory":
        st.subheader("Room Inventory")
        inventory_data = c.execute("SELECT * FROM room_inventory").fetchall()
        st.table(inventory_data)
    elif selected_table == "Room Types":
        st.subheader("Room Types")
        room_types_data = c.execute("SELECT * FROM room_types").fetchall()
        st.table(room_types_data)
    elif selected_table == "Room Bookings":
        st.subheader("Room Bookings")
        bookings_data = c.execute("SELECT * FROM room_bookings").fetchall()
        st.table(bookings_data)
    elif selected_table == "Feedback":
        st.subheader("Feedback")
        feedback_data = c.execute("SELECT * FROM feedback").fetchall()
        st.table(feedback_data)

# Function to add a guest
def add_guest(name, contact_info, address, nationality, other_details):
    c.execute("INSERT INTO guests (name, contact_info, address, nationality, other_details) VALUES (?, ?, ?, ?, ?)",
              (name, contact_info, address, nationality, other_details))
    conn.commit()

# Function to update a guest
def update_guest(guest_id, name, contact_info, address, nationality, other_details):
    c.execute("UPDATE guests SET name=?, contact_info=?, address=?, nationality=?, other_details=? WHERE id=?",
              (name, contact_info, address, nationality, other_details, guest_id))
    conn.commit()

# Function to delete a guest
def delete_guest(guest_id):
    c.execute("DELETE FROM guests WHERE id=?", (guest_id,))
    conn.commit()

# Function to add a room
def add_room(room_number, room_type, description, rate, status):
    c.execute("INSERT INTO rooms (room_number, room_type, description, rate, status) VALUES (?, ?, ?, ?, ?)",
              (room_number, room_type, description, rate, status))
    conn.commit()

# Function to update a room
def update_room(room_id, room_number, room_type, description, rate, status):
    c.execute("UPDATE rooms SET room_number=?, room_type=?, description=?, rate=?, status=? WHERE id=?",
              (room_number, room_type, description, rate, status, room_id))
    conn.commit()

# Function to delete a room
def delete_room(room_id):
    c.execute("DELETE FROM rooms WHERE id=?", (room_id,))
    conn.commit()

# Sign up page
st.title("Hotel Management System")
st.header("Sign Up")
username_signup = st.text_input("Username (Sign Up)", key="username_signup")
password_signup = st.text_input("Password (Sign Up)", type="password", key="password_signup")
role = st.selectbox("Role", ["Customer", "Admin"], key="role_signup")
if st.button("Sign Up"):
    add_customer(username_signup, password_signup, role)
    st.success("Signed up successfully")

# Login page
st.header("Login")
username_login = st.text_input("Username (Login)", key="username_login")
password_login = st.text_input("Password (Login)", type="password", key="password_login")
if st.button("Login"):
    user = check_user(username_login, password_login)
    if user:
        st.success("Logged in successfully")
        if user[3] == "Admin":
            display_tables()
            # Handle CRUD operations for Guests
            operation = st.sidebar.selectbox("Select Operation", ("Add Guest", "Update Guest", "Delete Guest"))
            if operation == "Add Guest":
                st.subheader("Add Guest")
                name = st.text_input("Name")
                contact_info = st.text_input("Contact Information")
                address = st.text_input("Address")
                nationality = st.text_input("Nationality")
                other_details = st.text_input("Other Details")
                if st.button("Add"):
                    add_guest(name, contact_info, address, nationality, other_details)
                    st.success("Guest added successfully")
            elif operation == "Update Guest":
                st.subheader("Update Guest")
                guest_id = st.number_input("Guest ID")
                name = st.text_input("Name")
                contact_info = st.text_input("Contact Information")
                address = st.text_input("Address")
                nationality = st.text_input("Nationality")
                other_details = st.text_input("Other Details")
                if st.button("Update"):
                    update_guest(guest_id, name, contact_info, address, nationality, other_details)
                    st.success("Guest updated successfully")
            elif operation == "Delete Guest":
                st.subheader("Delete Guest")
                guest_id = st.number_input("Guest ID")
                if st.button("Delete"):
                    delete_guest(guest_id)
                    st.success("Guest deleted successfully")
    else:
        st.error("Invalid username or password")

# Close the connection
conn.close()
