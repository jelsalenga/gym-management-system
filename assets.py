from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sqlite3
from queue import Queue
import re
from datetime import date
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from functools import partial
import hashlib
# DATABASE
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


font1 = QFont()
font2 = QFont()
font3 = QFont() 
font4 = QFont()
font5 = QFont()
font6 = QFont()

font1.setPointSize(20)
font2.setPointSize(18)
font3.setPointSize(16)
font4.setPointSize(26)
font5.setPointSize(8)
font6.setPointSize(12)

current_username = None
def set_username_global(text):
    global current_username
    current_username = text


def validate_input(field_name, value, rules):
    """Validate a field against given rules."""
    for rule in rules:
        if rule == "required" and not value:
            return False, f"{field_name} is required."
        if rule == "numeric" and not str(value).isdigit():
            return False, f"{field_name} must be numeric."
        if rule == "email":
            pattern = r"[^@]+@[^@]+\.[^@]+"
            if not re.match(pattern, value):
                return False, f"{field_name} must be a valid email."
        if rule == "date":
            if not isinstance(value, QDate):
                return False, f"{field_name} must be a valid date."
        if rule == "phone":
            pattern = r"^\+?\d{10,15}$"
            if not re.match(pattern, value):
                return False, f"{field_name} must be a valid phone number."
        if rule == "image":
            if isinstance(value, memoryview):
                value = bytes(value)
            byte_array = QByteArray(value)
            image = QImage()
            if not image.loadFromData(byte_array):
                return False, f"{field_name} must be a valid image."
        if rule == "alphabet":
            pattern = r"^[a-zA-Z\s\-]+$"
            if not re.match(pattern, value):
                return False, f"{field_name} must contain only alphabetic characters, spaces, or hyphens."
        if rule == "adult":
            if isinstance(value, QDate):
                current_date = QDate.currentDate()
                age = current_date.year() - value.year()
                if current_date.month() < value.month() or (current_date.month() == value.month() and current_date.day() < value.day()):
                    age -= 1
                if age < 18:
                    return False, f"{field_name} must be at least 18 years old."
        if rule == "date_range":
            start_date, end_date = value
            if not isinstance(start_date, QDate) or not isinstance(end_date, QDate):
                return False, f"{field_name} must be valid dates."
            if start_date >= end_date:
                return False, f"{field_name} start date must be before the end date."
    return True, ""


def validate_all_inputs(entity_type, inputs):
    VALIDATION_RULES = {
        # ATTENDANCE TABLE
        'Attendance': {
            'attendance_id': ["required"], 
            'member_id': ["required"], 
            'entry_time': ["required"], 
            'exit_time': ["required"], 
            'date': ["required"],
        },
        # MEMBERS TABLE
        'Members': {
            'member_id': ["required"], 
            'first_name': ["required", 'alphabet'], 
            'middle_name': ["required", 'alphabet'], 
            'last_name': ["required", 'alphabet'], 
            'address': ["required"],
            'gender': ["required"],
            'birthdate': ["required", "adult"],
            'phone': ["required", "phone", 'numeric'],
            'membership_type': ["required"],
            'membership_start_date': ["required", "date_range"],
            'membership_end_date': ["required", "date_range"],
            'image': ["required", "image"],
            'signature': ["required", "image"]
        },
        # EMPLOYEES TABLE
        'Employees': {
            'employee_id': ["required"], 
            'first_name': ["required", 'alphabet'], 
            'middle_name': ["required", 'alphabet'], 
            'last_name': ["required", 'alphabet'], 
            'birthdate': ["required"],
            'gender': ["required"],
            'address': ["required"],
            'phone': ["required", 'phone', 'numeric'],
            'hire_date': ["required"],
            'position': ["required", 'alphabet'],
            'photo': ["required", "image"],
        },
        # EQUIPMENTS TABLE
        'Equipments': {
            'equipment_id': ["required"], 
            'equipment_name': ["required"], 
            'equipment_serial_number': ["required"], 
            'equipment_category': ["required"], 
            'equipment_purchase_date': ["required"],
            'equipment_warranty_expiry': ["required"],
            'equipment_price': ["required", 'numeric'],
            'equipment_manufacturer': ["required"],
            'equipment_location': ["required"],
            'equipment_status': ["required"],
        },
        # PRODUCTS TABLE
        'Products': {
            'product_id': ["required"],
            'product_name': ["required"],
            'sku': ["required"],
            'quantity': ["required", 'numeric'],
            'supplier':["required"],
            'price': ["required", 'numeric'],
            'purchase_date': ["required"],
            'expiry_date': ["required"]
        },
        # SCHEDULE TABLE
        'Schedule': {
            'schedule_id': ["required"],
            'member_id': ["required"],
            'employee_id': ["required"],
            'appointment_type': ["required"],
            'appointment_name': ["required"],
            'appointment_date': ["required"],
            'appointment_start_time': ["required"],
            'appointment_end_time': ["required"],
            'status': ["required"]
        },
        # USERS TABLE
        'Users': {
            'employee_id': ["required"],
            'username': ["required"],
            'password': ["required"],
            'role': ["required"]
        },

        'Contracts': {
            'reference_number': ["required"],
            'member_id': ["required"],
            'softcopy': ["required"],
            'date_recorded':["required"],
        }
    }

    rules = VALIDATION_RULES.get(entity_type, {})
    for field, value in inputs.items():
        field_rules = rules.get(field, [])
        valid, message = validate_input(field, value, field_rules)
        if not valid:
            QMessageBox.warning(None, "Validation Error", message)
            return False
    return True


# Assuming current_username is a global variable that needs to be accessed and updated
def get_user_log(action, usertext):
    global current_username
    current_username = usertext
    if current_username:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO UserLog (username, action, timestamp) VALUES (?, ?, ?)",
                       (current_username, action, timestamp))
        connection.commit()
    else:
        print("Current current_username is not set.")  # Optional: Handle case where current_username is not set


# Define SQL queries as constants
SQL_GET_LAST_ATTENDANCE = ''' 
    SELECT attendance_id, entry_time, exit_time 
    FROM Attendance
    WHERE member_id = ? AND date = ? 
    ORDER BY attendance_id DESC LIMIT 1 
'''

SQL_INSERT_ATTENDANCE = '''
    INSERT INTO Attendance (member_id, entry_time, date) 
    VALUES (?, ?, ?)
'''

SQL_UPDATE_ATTENDANCE = '''  
    UPDATE Attendance 
    SET exit_time = ? 
    WHERE attendance_id = ?
'''

SQL_INSERT_MEMBER = '''
    INSERT INTO Members 
    (member_id, first_name, middle_name, last_name, address, phone_number, birthdate, membership_type,
    gender, membership_start_date, membership_end_date, photo, signature, void) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
'''

SQL_INSERT_EMPLOYEE = '''
    INSERT INTO Employees 
    (employee_id, first_name, middle_name, last_name, birthdate, gender, address, phone,
    hire_date, position, photo, void) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
'''

SQL_INSERT_USER = '''
    INSERT INTO Users
    (employee_id, username, password_hash, role, void) VALUES
    (?, ?, ?, ?, 0)
'''

SQL_INSERT_EQUIPMENT = '''
    INSERT INTO Equipments 
    (equipment_id, equipment_name, equipment_serial_number, equipment_category, equipment_purchase_date, 
    equipment_warranty_expiry, equipment_price, equipment_manufacturer, equipment_location, equipment_status, void
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)

'''

SQL_UPDATE_MEMBERS = '''
    UPDATE Members
    SET first_name = ?, middle_name = ?, last_name = ?,address = ?,   phone_number = ?, birthdate = ?, membership_type = ?, 
    gender = ?,  membership_start_date = ? , membership_end_date = ?, photo = ?, signature = ?
    WHERE member_id = ?          
'''

SQL_UPDATE_USER = '''
    UPDATE Users
    SET username = ?, password_hash = ?, role = ? 
    WHERE employee_id = ?
'''

SQL_UPDATE_EQUIPMENT = '''
    UPDATE Equipments
    SET equipment_name = ?, equipment_serial_number = ?, equipment_category = ?, equipment_purchase_date = ?, 
    equipment_warranty_expiry = ?, equipment_price = ?, equipment_manufacturer = ?, equipment_location = ?, equipment_status = ?
    WHERE equipment_id = ?
'''

SQL_UPDATE_EMPLOYEE = '''
    UPDATE Employees
    SET first_name = ?, middle_name = ?, last_name = ?, birthdate = ?, 
    gender = ?, address = ?, phone = ?, hire_date = ?, position =? , photo = ?
    WHERE employee_id = ?
'''

SQL_INSERT_PRODUCT = '''
    INSERT INTO Products
    (product_id, name, brand, sku, quantity, supplier, price, purchase_date, expiry_date, status, void) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active', 0)
'''

SQL_UPDATE_CONTRACT = '''
    UPDATE Contracts
    SET softcopy_contract = ?, date_recorded = ?
    WHERE reference_number = ?
'''


SQL_FETCH_MEMBER =  '''
    SELECT member_id, 
    first_name || ' ' || last_name, membership_type, phone_number, membership_end_date
    FROM Members
    WHERE void = 0
'''

SQL_FETCH_EMPLOYEE = '''
    SELECT 
    employee_id, first_name || ' ' || last_name, position, phone, hire_date
    FROM Employees 
    WHERE void = 0
'''

SQL_FETCH_USER = '''
    SELECT 
    employee_id, username, role 
    FROM Users 
    WHERE void = 0
'''

SQL_FETCH_EQUIPMENT = '''
    SELECT 
    equipment_id, equipment_name, equipment_serial_number, equipment_category, equipment_status 
    FROM Equipments
    WHERE void = 0
'''

SQL_FETCH_PRODUCT = '''
    SELECT 
    product_id, name, quantity,expiry_date, status
    FROM Products
    WHERE void = 0 
'''

SQL_FETCH_PAYMENT = ''' SELECT * FROM Contracts '''

SQL_SEARCH_MEMBER = '''
    SELECT 
        member_id, 
        first_name || ' ' || last_name, 
        membership_type, 
        phone_number,  
        membership_end_date
    FROM Members
    WHERE (member_id LIKE ? OR first_name || ' ' || last_name LIKE ? OR first_name LIKE ?) AND void = 0 ;
'''


SQL_SEARCH_EMPLOYEE = '''
    SELECT 
    employee_id, first_name || ' ' || last_name, position, phone, hire_date
    FROM Employees
    WHERE (employee_id LIKE ? OR first_name || ' ' || last_name LIKE ?) AND void = 0;
'''

SQL_SEARCH_USER = '''
    SELECT 
    employee_id, username, role
    FROM Users
    WHERE (employee_id LIKE ? OR username LIKE ?) AND void = 0;
'''

SQL_SEARCH_EQUIPMENT = '''
    SELECT 
    equipment_id, equipment_name, equipment_serial_number, equipment_category, equipment_status, equipment_purchase_date
    FROM Equipments
    WHERE (equipment_id LIKE ? OR equipment_name LIKE ? OR equipment_serial_number LIKE ?) AND void = 0;
'''

SQL_SEARCH_PRODUCT = '''
    SELECT 
    product_id, name, quantity, expiry_date, status
    FROM Products
    WHERE (product_id LIKE ? OR name LIKE ?) AND void = 0;
'''

SQL_SEARCH_PAYMENT = '''
    SELECT 
    c.reference_number AS "Payment ID", c.member_id AS "Members ID", c.softcopy_contract AS "File Path", c.date_recorded AS "Date Recorded"
    FROM Contracts c
    JOIN Members m ON m.member_id = c.member_id
    WHERE c.reference_number LIKE ? OR m.first_name LIKE ? OR m.last_name LIKE ?;
'''

ENTITY_ID_MAPPING = {
    'Members': 'member_id',
    'Employees': 'employee_id',
    'Equipments': 'equipment_id',
    'Products': 'product_id',
    'Users': 'employee_id',
    # Add more entities as needed
}
def search_entity(entity, search_text, table_widget, view_function):
    keyword = search_text.text().strip()

    # Assuming cursor and queries are defined elsewhere
    queries = {
        "Members": SQL_SEARCH_MEMBER,
        "Employees": SQL_SEARCH_EMPLOYEE,
        "Users": SQL_SEARCH_USER,
        "Equipments": SQL_SEARCH_EQUIPMENT,
        "Products": SQL_SEARCH_PRODUCT,
        "Payments": SQL_SEARCH_PAYMENT
    }
    query = queries.get(entity)

    # Adjust the number of parameters in the query based on the entity
    if entity in ["Equipments", "Payments", "Members"]:
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    elif entity in ["Users", "Products", "Employees"]:
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))

    results = cursor.fetchall()
    table_widget.setRowCount(len(results))

    for row_idx, row_data in enumerate(results):
        for col_idx, col_data in enumerate(row_data):
            table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Add view button in the correct column after the last data column
        add_view_buttons(table_widget, void_row, row_idx, row_data)

        # Add void button in the correct column after the view button
        add_void_buttons(table_widget, void_row, row_idx, entity, row_data)
       
def add_view_buttons(table_widget, view_function, row_idx, row_data):
    view_button = QPushButton("View")
    view_button.clicked.connect(partial(view_function, row_idx))
    # Place the button in the next column after the last data column
    table_widget.setCellWidget(row_idx, len(row_data), view_button)

def add_void_buttons(table_widget, void_function, row_idx, entity, row_data):
    void_button = QPushButton("Void")
    void_button.setStyleSheet("background-color: red; color: #FFFFFF")
    void_button.clicked.connect(partial(void_function, table_widget, row_idx, entity))
    # Place the button in the next column after the "View" button
    table_widget.setCellWidget(row_idx, len(row_data) + 1, void_button)
def fetch_entity(entity):

    fetch_queries = {
        "Members": SQL_FETCH_MEMBER,
        "Employees": SQL_FETCH_EMPLOYEE,
        "Users": SQL_FETCH_USER,
        "Equipments": SQL_FETCH_EQUIPMENT,
        "Products": SQL_FETCH_PRODUCT,
        "Payments": SQL_FETCH_PAYMENT
    }
    query = fetch_queries.get(entity)
    if query:
        cursor.execute(query)
        return cursor.fetchall()
    else:
        raise ValueError(f"Unknown entity: {entity}") 

def get_last_attendance(cursor, member_id, date):
    cursor.execute(SQL_GET_LAST_ATTENDANCE, (member_id, date))
    return cursor.fetchone()


def update_table_widget(entity, table_widget, view_function):
    # Fetch the data
    data = fetch_entity(entity)
    
    # Sort the data in descending order (assuming sorting by the first column)
    data.sort(key=lambda x: x[0], reverse=True)

    # Set the number of rows in the table
    table_widget.setRowCount(len(data))

    for row_index, row_data in enumerate(data):
        for col_index, col_data in enumerate(row_data):
            # Add data to the table
            table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        # Add a view button
        view_button = QPushButton("View")
        view_button.clicked.connect(partial(view_function, row_index))
        table_widget.setCellWidget(row_index, len(row_data), view_button)

        add_void_buttons(table_widget, void_row, row_index, entity, row_data)

    table_widget.verticalHeader().setVisible(False)

def void_row(table_widget, row_index, entity):

    first_column_value = table_widget.item(row_index, 0).text()


    # Show a confirmation dialof
    reply = QMessageBox.question(
        None, 'Confirmation', 'Are you sure you want to void this row?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        if entity in ENTITY_ID_MAPPING:
            id_column = ENTITY_ID_MAPPING[entity]
            cursor = connection.cursor()
            cursor.execute(f"UPDATE {entity} SET void = 1 WHERE {id_column} = ?", (first_column_value,))
            connection.commit()

        for col_index in range(table_widget.columnCount() - 1):
            table_widget.setItem(row_index, col_index, QTableWidgetItem("VOIDED"))
        
        view_button = table_widget.cellWidget(row_index, table_widget.columnCount() - 2)
        if view_button:
            view_button.setDisabled(True)

        void_button = table_widget.cellWidget(row_index, table_widget.columnCount() - 1)
        if void_button:
            void_button.setDisabled(True)


def insert_attendance(cursor, member_id, entry_time, date):
    cursor.execute(SQL_INSERT_ATTENDANCE, (member_id, entry_time, date))

def update_attendance(cursor, attendance_id, exit_time):
    cursor.execute(SQL_UPDATE_ATTENDANCE, (exit_time, attendance_id))

# REGISTERING ATTENDANCE 
def register_attendance(inputs, page):

    member_id = inputs["member_id"]
    date = inputs["date"].toString("yyyy-MM-dd")
    time = inputs["time"].toString()
    
    last_record = get_last_attendance(cursor, member_id, date)
    
    try:

        if validate_all_inputs("Attendance", inputs):
            if inputs["attendance"] == "Entry":
                if last_record and not last_record[2]:  # If there's an entry with no exit
                    QMessageBox.warning(None, "Error" , "Member already has an entry record with no exit recorded.")
                    get_user_log(f"Failed to Register Entry Attendance", current_username)
                else:
                    insert_attendance(cursor, member_id, time, date)
                    connection.commit()
                    QMessageBox.information(None, "Success", "Entry registered successfully!")
                    get_user_log(f"Registered Entry Attendance", current_username)
                    clear_inputs(page)
            else:  # Exit
                if last_record and not last_record[2]:  # If there's an entry with no exit
                    update_attendance(cursor, last_record[0], time)
                    connection.commit()
                    QMessageBox.information(None, "Success", "Exit registered successfully!")
                    get_user_log(f"Registered Exit Attendance", current_username)
                    clear_inputs(page)
                else:
                    QMessageBox.warning(None, "Error", "No entry record found or already exited.")
                    get_user_log(f"Failed to Register Exit Attendance", current_username) 
    except sqlite3.Error as e:
        return f"Database error: {e}"

def register_member(inputs, page, text):
    try:
        if validate_date(inputs["start_date"], inputs["end_date"]):
            if validate_all_inputs("Members", inputs):
                cursor.execute(SQL_INSERT_MEMBER, (
                    inputs["member_id"],
                    inputs["first_name"].strip(),
                    inputs["middle_name"].strip(),
                    inputs["last_name"].strip(),
                    inputs["address"],
                    inputs["phone"],
                    inputs["birthdate"].toString("yyyy-MM-dd"),
                    inputs["membership_type"],
                    inputs["gender"],
                    inputs["start_date"].toString("yyyy-MM-dd"),
                    inputs["end_date"].toString("yyyy-MM-dd"),
                    inputs["image"],
                    inputs["signature"],
                ))
                connection.commit()
                QMessageBox.information(None, "Success", "Member registered successfully!")
                get_user_log(f"Registered a Member", current_username)
                clear_inputs(page)
                generate_id("Members", text)
    except sqlite3.Error as e:
        connection.rollback()
        return f"Database error: {e}"
    
def register_employee(inputs, page, text):
    try:
        if validate_all_inputs("Employees", inputs):
            cursor.execute(SQL_INSERT_EMPLOYEE, (
                inputs["employee_id"],
                inputs["first_name"].strip(),
                inputs["middle_name"].strip(),  # Handle cases where middle_name might be missing
                inputs["last_name"].strip(),
                inputs["birthdate"].toString("yyyy-MM-dd"),  # Format date correctly
                inputs["gender"],
                inputs["address"],
                inputs["phone"],
                inputs["hire_date"].toString("yyyy-MM-dd"),  # Format date correctly
                inputs["position"],
                inputs["photo"],
            ))
            connection.commit()
            QMessageBox.information(None, "Success", "Employee registered successfully!")
            get_user_log(f"Registered an Employee", current_username)
            clear_inputs(page)
            generate_id("Employees", text)
    except sqlite3.Error as e:
        connection.rollback()
        return f"Database error: {e}"

def register_user(inputs, page):
    try:
        if inputs["password"] == inputs["retry_password"]:
            if validate_all_inputs("Users", inputs):
                password_bytes = inputs["password"].encode()
                hashed_password = hashlib.sha256(password_bytes).hexdigest()
                cursor.execute(SQL_INSERT_USER, (
                                inputs["employee_id"],
                                inputs["username"],
                                hashed_password,
                                inputs["role"]
                                )
                            )

                connection.commit()
                QMessageBox.information(None, "Registered", "Account Sucessfully Registered")
                get_user_log(f"Registered an Employee", current_username)
                clear_inputs(page)
        else: 
            QMessageBox.warning(None, "Error", "Password Unidentical")
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"

def register_equipment(inputs, page, text):
    try:
        if validate_all_inputs("Equipments", inputs):
            if validate_date(inputs['equipment_purchase_date'], inputs['equipment_warranty_expiry']):
                cursor.execute(SQL_INSERT_EQUIPMENT, (
                            inputs['equipment_id'], 
                            inputs['equipment_name'], 
                            inputs['equipment_serial_number'], 
                            inputs['equipment_category'], 
                            inputs['equipment_purchase_date'], 
                            inputs['equipment_warranty_expiry'], 
                            inputs['equipment_price'], 
                            inputs['equipment_manufacturer'], 
                            inputs['equipment_location'], 
                            inputs['equipment_status']
                            )
                )
                connection.commit()
                QMessageBox.information(None, "Registered", "Account Sucessfully Registered")
                get_user_log(f"Registered an Equipment", current_username)
                clear_inputs(page)
                generate_id("Equipments", text)
            else: 
                QMessageBox.warning(None, "Error", "Register of Equipment Failed")
                get_user_log(f"Registered an Equipment Failedd", current_username)
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"

def register_product(inputs, page, text):
    try:
        if validate_all_inputs("Products", inputs):
            cursor.execute(SQL_INSERT_PRODUCT, (
                            inputs['product_id'],
                            inputs['product_name'],
                            inputs['brand'],
                            inputs['sku'],
                            inputs['quantity'],
                            inputs['supplier'],
                            inputs['price'],
                            inputs['purchase_date'].toString("yyyy-MM-dd"),
                            inputs['expiry_date'].toString("yyyy-MM-dd"),
                        )
            )
            connection.commit()
            QMessageBox.information(None, "Registered", "Product Successfully Updated")
            get_user_log("Registered a Product", current_username)
            clear_inputs(page)
            generate_id("Products", text)
        else: 
            QMessageBox.warning(None, "Error", "Update Information Failed")
            get_user_log("Update Product Information Failed", current_username)
    except sqlite3.Error as e:
        connection.rollback()
        QMessageBox.warning(None, "Database Error", f"Database error: {e}")
        get_user_log(f"Database error: {e}", current_username)

def update_member(inputs, page):
    try:
        if validate_all_inputs("Members", inputs):
            cursor.execute(SQL_UPDATE_MEMBERS, (
                            inputs["first_name"].strip(),
                            inputs["middle_name"].strip(),
                            inputs["last_name"].strip(),
                            inputs["address"],
                            inputs["phone"],
                            inputs["birthdate"].toString("yyyy-MM-dd"),
                            inputs["membership_type"],
                            inputs["gender"],
                            inputs["start_date"].toString("yyyy-MM-dd"),
                            inputs["end_date"].toString("yyyy-MM-dd"),
                            inputs["image"],
                            inputs["signature"],
                            inputs["member_id"],
                        )
            )
            connection.commit()
            QMessageBox.information(None, "Registered", "Member Successfully Updated")
            get_user_log("Updated a Member", current_username)
            page()  # Call the page function if needed
        else: 
            QMessageBox.warning(None, "Error", "Update Information Failed")
            get_user_log("Update Member Information Failed", current_username)
    except sqlite3.Error as e:
        connection.rollback()
        QMessageBox.warning(None, "Database Error", f"Database error: {e}")
        get_user_log(f"Database error: {e}", current_username)

def update_employee(inputs, page):
    try:
        if validate_all_inputs("Employees", inputs):
            cursor.execute(SQL_UPDATE_EMPLOYEE, (                     
                            inputs['first_name'],
                            inputs['middle_name'],
                            inputs['last_name'],
                            inputs['birthdate'].toString("yyyy-MM-dd"),
                            inputs['gender'],
                            inputs['address'],
                            inputs['phone'],
                            inputs['hire_date'].toString("yyyy-MM-dd"),
                            inputs['position'],
                            inputs['photo'],
                            inputs['employee_id'],
                        )
            )
            connection.commit()
            QMessageBox.information(None, "Registered", "Employee Information Successfully Updated")
            get_user_log("Updated an Employee", current_username)
            page()  # Call the page function if needed
        else: 
            QMessageBox.warning(None, "Error", "Update Information Failed")
            get_user_log("Update Employee Information Failed", current_username)
    except sqlite3.Error as e:
        connection.rollback()
        QMessageBox.warning(None, "Database Error", f"Database error: {e}")
        get_user_log(f"Database error: {e}", current_username)

def update_user(inputs, page):
    try:
        if validate_all_inputs("Users", inputs):
            print("lmao")
            password_bytes = inputs["password"].encode()
            hashed_password = hashlib.sha256(password_bytes).hexdigest()
            print(hashed_password)
            cursor.execute(SQL_UPDATE_USER, (
                            inputs["username"],
                            hashed_password,
                            inputs["role"],
                            inputs["employee_id"],

                        )
            )
            connection.commit()
            QMessageBox.information(None, "Updated", "Account Sucessfully Updated")
            get_user_log(f"Updated an Account", current_username)
            page()
        else: 
            QMessageBox.warning(None, "Error", "Update Information Failed")
            get_user_log(f"Update Account Information Failed", current_username)
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"

def update_equipment(inputs, page):
    try:
        if validate_all_inputs("Equipments", inputs):
            if validate_date(inputs['equipment_purchase_date'], inputs['equipment_warranty_expiry']):
                cursor.execute(SQL_UPDATE_EQUIPMENT, (
                                inputs['equipment_name'], 
                                inputs['equipment_serial_number'], 
                                inputs['equipment_category'], 
                                inputs['equipment_purchase_date'].toString("yyyy-MM-dd"), 
                                inputs['equipment_warranty_expiry'].toString("yyyy-MM-dd"), 
                                inputs['equipment_price'], 
                                inputs['equipment_manufacturer'], 
                                inputs['equipment_location'], 
                                inputs['equipment_status'],
                                inputs['equipment_id']
                            )
                )
                connection.commit()
                QMessageBox.information(None, "Updated", "Equipment Sucessfully Updated")
                get_user_log(f"Updated an Account", current_username)
                page()
            else: 
                QMessageBox.warning(None, "Error", "Update Information Failed")
                get_user_log(f"Update Equipment Information Failed", current_username)
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"

def update_product(inputs, page):
    try:
        if validate_all_inputs("Products", inputs):
            if validate_date(inputs['equipment_purchase_date'], inputs['equipment_warranty_expiry']):
                cursor.execute(SQL_UPDATE_EQUIPMENT, (
                                inputs['product_id'],
                                inputs['product_name'],
                                inputs['sku'],
                                inputs['quantity'],
                                inputs['supplier'],
                                inputs['price'],
                                inputs['purchase_date'],
                                inputs['expiry_date'],
                            )
                )
                connection.commit()
                QMessageBox.information(None, "Updated", "Product Sucessfully Updated")
                get_user_log(f"Updated a Product", current_username)
                page()
        else: 
            QMessageBox.warning(None, "Error", "Update Information Failed")
            get_user_log(f"Update Product Information Failed", current_username)
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"

def update_payment(inputs, page):
    try:
        if validate_all_inputs("Contracts", inputs):
            cursor.execute(SQL_UPDATE_CONTRACT, (
                        inputs['softcopy'],
                        inputs['date_recorded'],
                        inputs['reference_number'],
                        )
            )
            connection.commit()
            QMessageBox.information(None, "Registered", "Account Sucessfully Registered")
            get_user_log(f"Updated a Payment", current_username)
        else: 
            QMessageBox.warning(None, "Error", "Update of Payment Failed")
            get_user_log(f"Updated a Payment Failed", current_username)
    except sqlite3.Error as e:
            connection.rollback()
            return f"Database error: {e}"


def disable_past_date(label):
    label.setMinimumDate(QDate.currentDate())
        # Disable selection of past dates
    label.setDateRange(QDate.currentDate(), QDate(2099, 12, 31))

def validate_date(start_date, end_date):
    if start_date >= end_date:
        QMessageBox.warning(None, "Invalid Date", "Start Date must be less than End Date.")
        return False
    return True
    
def validate_time(start_time, end_time):
    if start_time >= end_time:
        QMessageBox.warning(None, "Invalid Time", "Start Time must be less than End Time.")
        return False
    return True
def generate_id(entity_type, label):

    current_time = datetime.now()
    formatted_time = current_time.strftime('%m%d%y')
    if entity_type == "Members":
        query = f"SELECT COUNT(*) FROM {entity_type}"
        prefix = "MEM"
    elif entity_type == "Employees":
        query = f"SELECT COUNT(*) FROM {entity_type}"
        prefix = "EMP"
    elif entity_type == "Equipments":
        query = f"SELECT COUNT(*) FROM {entity_type}"
        prefix = "EQP"
    elif entity_type == "Products":
        query = f"SELECT COUNT(*) FROM {entity_type}"
        prefix = "PRD"

    cursor.execute(query)
    count = cursor.fetchone()[0] + 1
    generated_id = f"{prefix}-{formatted_time}-{count:04}"

    label.setText(generated_id)



def clear_inputs(page):
    for widget in page.findChildren(QWidget):
        if isinstance(widget, QLineEdit):
            widget.clear()
        elif isinstance(widget, QComboBox):
            widget.setCurrentIndex(-1)  # Reset the selection
        elif isinstance(widget, QDateEdit):
            current_date = QDate.currentDate()
            widget.setDate(current_date)
            widget.clear()
        elif isinstance(widget, QTimeEdit):
            current_time = QTime.currentTime()
            widget.setTime(current_time)
            widget.clear()
        elif isinstance(widget, QLabel):
            if widget.objectName() in ["image_label", "signature_label", "output"]:
                widget.clear()  # Clears the label content
                widget.setPixmap(QPixmap())  # Clears any image or signature

def insert_image(image):
    # Open a file dialog to select an image file
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.bmp *.gif)"
        )

        if file_name:
            # Load the image and set it to the label
            pixmap = QPixmap(file_name)
            image.setPixmap(pixmap.scaled(image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

def pixmap_to_bytes(pixmap):
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QBuffer.WriteOnly)
    pixmap.save(buffer, "PNG")
    return byte_array.data()


def createDate(parent, geometry, name = "date", font = font2, style = "background-color: #F9F7FF; border: 1px solid black"):
    current_date = QDate.currentDate()
    date = QDateEdit(parent)
    date.setObjectName(name)
    date.setGeometry(QRect(geometry))
    date.setFont(QFont(font))
    date.setCalendarPopup(True)
    date.setStyleSheet(style)
    date.setDate(current_date)
    return date

def createComboBox(parent, geometry, item,name ="combo_box", font = font2, style = "background-color: #F9F7FF; border: 1px solid black"):
    combo_box = QComboBox(parent)
    combo_box.setObjectName(name)
    combo_box.setGeometry(geometry)
    combo_box.setFont(QFont(font))
    combo_box.setStyleSheet(style)
    combo_box.setCurrentIndex(-1) 
    combo_box.addItems(item)

    return combo_box

def createTime(parent, name, geometry, font, style= "background-color: #F9F7FF; border: 1px solid black"):
    current_time = QTime.currentTime()
    time = QTimeEdit(parent)
    time.setObjectName(name)
    time.setGeometry(geometry)
    time.setFont(QFont(font))
    time.setTime(current_time)
    time.setStyleSheet(style)
    return time

def createLabel(parent, geometry, name = "label", text = "", font = font1, style = ""):
    label = QLabel(parent)
    label.setObjectName(name)
    label.setGeometry(geometry)
    label.setText(text)
    label.setFont(QFont(font))
    label.setStyleSheet(style)
    return label

def createOutputLabel(parent, geometry, name = "output", text = "", font = font2, style = "background-color: #F9F7FF; border: 1px solid black"):
    output_label = QLabel(parent)
    output_label.setObjectName(name)
    output_label.setGeometry(geometry)
    output_label.setText(text)
    output_label.setFont(QFont(font))
    output_label.setStyleSheet(style)
    return output_label

def createLineInput(parent,geometry, name = "input", font = font2, style = "background-color: #F9F7FF; border: 1px solid black", placeholder = ""):
    line_input = QLineEdit(parent)
    line_input.setObjectName(name)
    line_input.setGeometry(geometry)
    line_input.setFont(font)
    line_input.setStyleSheet(style)
    line_input.setPlaceholderText(placeholder)
    return line_input

def createButton(parent, name, geometry, text, font, style):
    button = QPushButton(parent)
    button.setObjectName(name)
    button.setGeometry(geometry)
    button.setText(text)
    button.setFont(QFont(font))
    button.setStyleSheet(style)
    return button

