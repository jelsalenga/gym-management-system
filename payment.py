from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sqlite3
import fitz  
from functools import partial
from assets import *
from datetime import date
import time
import random
import subprocess
import os



class Payment(QWidget):  # Inherit from QWidget
    def __init__(self, parent=None):
        super(Payment, self).__init__(parent)
        self.setWindowTitle("Payment")
        self.setObjectName("Payment")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #E0E0E0;")

        # Search Bar Input Field
        self.search_bar = createLineInput(
            parent = self,
            name = "payment_search_bar",
            geometry = QRect(30, 20, 400, 61),
            font = font5,
            style = "background: white",
            placeholder = "Enter Member ID / Reference Number here"
        )

        # Search Button
        self.btn_search = createButton(
            parent = self,
            name = "payment_search_button",
            geometry = QRect(430, 20, 71, 61),
            text = "Search",
            font = font5,
            style = "background: #4681f4; color: white"
        )

        self.btn_load = createButton(
            parent = self,
            name = "payment_load_button",
            geometry = QRect(530, 20, 100, 60),
            text = "Load Data",
            font = font5,
            style = "background: #4681f4; color: white"
        )

        # Record option
        self.btn_record = createButton(
            parent = self,
            name = "payment_btn_record",
            geometry = QRect(770, 730, 140, 45),
            text = "Record",
            font = font5,
            style = "background: lime; color: white"
        )

        self.btn_search.clicked.connect(self.search)
        self.btn_record.clicked.connect(self.showRecord)
        self.btn_load.clicked.connect(self.loadData)

        # Table Widget Properties
        self.tableWidget = QTableWidget(self)
        table = self.tableWidget
        table.setGeometry(QRect(30, 100, 880, 620))
        table.setRowCount(0)
        table.setColumnCount(5)
        table.setObjectName("tableWidget")
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        table.setStyleSheet("background: white")
        self.loadData()
     

    # Populate Table View
    def loadData(self):
            # Load Table
            self.tableWidget.setRowCount(0)
            cursor.execute('PRAGMA table_info(Contracts)')
            columns_info = cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            column_names.append("")

            # Set column count and column names in table widget
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            cursor.execute("SELECT * FROM Contracts")
            for row_number, row_data in enumerate(cursor):
                self.tableWidget.insertRow(row_number)  
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignRight)
                    self.tableWidget.setItem(row_number, column_number, item)

                view_button = QPushButton("View")
                view_button.clicked.connect(partial(self.view_contract, row_number))
                self.tableWidget.setCellWidget(row_number, len(row_data), view_button) 
                   

    def search(self):
        search_term = self.search_bar.text()
        self.tableWidget.setRowCount(0)

        cursor.execute("""
                SELECT * 
                FROM Contracts 
                WHERE CAST(member_id AS TEXT) LIKE ? OR CAST(reference_number AS TEXT) LIKE ?
                """, (search_term + '%', search_term + '%'))
        
        for row_number, row_data in enumerate(cursor):
            self.tableWidget.insertRow(row_number)  
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignRight)
                self.tableWidget.setItem(row_number, column_number, item)

            view_button = QPushButton("View")
            view_button.clicked.connect(lambda rn=row_number: self.view_contract(rn))
            self.tableWidget.setCellWidget(row_number, len(row_data), view_button) 
    
    def view_contract(self, row_number):
            if row_number is not None:
                contract_data = []
                for column_number in range(self.tableWidget.columnCount() - 1):  
                    cell_item = self.tableWidget.item(row_number, column_number)
                    if cell_item:
                        contract_data.append(cell_item.text())
                
            if len(contract_data) > 2:
                pdf_data = contract_data[2]
                print(pdf_data)
                self.run_script(pdf_data)
            else:
                print("No PDF data found in contract_data")
    
    def run_script(self, file_path):
        if os.path.isfile(file_path):
            os.startfile(file_path)


    def showRecord(self):
        popup = Record(self)
        popup.exec_()


class Record(QDialog):
    def __init__(self, parent=None):
        super(Record, self).__init__(parent)
        self.setWindowTitle("Record")
        self.resize(700, 600)
        self.setStyleSheet("background-color: #E0E0E0;")
         
        # Search Bar
        self.search_bar = createLineInput(
            parent = self,
            name = "record_bar_record",
            geometry = QRect(30, 20, 574, 61),
            font = font5,
            style = "background: white",
            placeholder = "Enter Member ID here"
        )

        # Search Button 
        self.btn_search = createButton(
            parent = self,
            name = "record_btn_search_record",
            geometry = QRect(604, 20, 71, 61),
            text = "Search",
            font = font5,
            style = "background: #4681f4; color: white"
        )
        

        # Add button 
        self.add_button = createButton(
            parent = self,
            name = "record_add_button",
            geometry = QRect(535, 530, 140, 45),
            text = "Add",
            font = font5,
            style = "background: lime; color: white"
        )
        add = self.add_button

        # Insert button
        self.insert_button = createButton(
            parent = self,
            name = "record_insert_button",
            geometry = QRect(50, 520, 361, 61),
            text = "Search",
            font = font5,
            style = "background: red; color: white"
        )
        insert = self.insert_button

        # Label Properties
        self.name = createLabel(
            parent = self,
            name = "record_name_label",
            geometry = QRect(40, 100, 121, 51),
            text = "Name",
            font = font1,
            style = "font: bold"
        )

        self.id = createLabel(
            parent = self,
            name = "record_id_label",
            geometry = QRect(40, 200, 301, 51),
            text = "Membership ID",
            font = font1,
            style = "font: bold"
        )

        self.name_id = createLabel(
            parent = self,
            name = "record_name_identity",
            geometry = QRect(40, 150, 361, 51),
            text = "Full Name",
            font = font6,
            style = "background: white; border: 1px solid black; font-style: italic; color: #A9A9AC"
        )

        self.id_id = createLabel(
            parent = self,
            name = "record_id_identity",
            geometry = QRect(40, 260, 361, 51),
            text = "Member ID",
            font = font6,
            style = "background: white; border: 1px solid black; font-style: italic; color: #A9A9AC"
        )

        self.photo = createLabel(
            parent = self,
            name = "record_photo_identity",
            geometry = QRect(450, 100, 225, 255),
            text = "Photo",
            font = font6,
            style = "background: white; border: 1px solid black; font-style: italic; color: #A9A9AC"
        )
        self.photo.setAlignment(Qt.AlignCenter)
        
        self.softcopy = createLabel(
            parent = self,
            name = "record_softcopy",
            geometry = QRect(50, 373, 361, 151),
            text = "",
            font = font6,
            style = "background: white; border: 1px solid black; font-style: italic; color: #A9A9AC"
        )
        self.copy = None

        
        # button clicks
        self.btn_search.clicked.connect(self.search)
        insert.clicked.connect(self.insert)
        add.clicked.connect(self.record)
        
    # Identify the member first
    def search(self):
        search_term = self.search_bar.text()

        cursor.execute("SELECT member_id, first_name || ' ' || middle_name || ' ' || last_name AS full_name, photo FROM Members WHERE member_id = ?", (search_term, ))
        result = cursor.fetchone()
        if result:
            membership_id, full_name, photo = result
            self.name_id.setText(full_name)
            self.id_id.setText(str(membership_id))

            pixmap = QPixmap()
            pixmap.loadFromData(photo)
            if not pixmap.isNull():
                self.photo.setPixmap(pixmap.scaled(self.photo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.photo.setText("No image available")
                self.photo.setAlignment(Qt.AlignCenter)

            return membership_id, True
        
        else:
            self.name_id.setText('No match found.')
            self.id_id.setText('No match found.')
            self.photo.clear()
            self.photo.setText("No image available")
            self.photo.setAlignment(Qt.AlignCenter)
            
        return None, False
    
    # Insert Softcopy function
    def insert(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_name:
            self.copy = file_name 
            self.softcopy.setText("File Inserted")
            self.softcopy.setAlignment(Qt.AlignCenter)
        else: 
            self.softcopy.setText("Missing File")
            self.softcopy.setAlignment(Qt.AlignCenter)

  
    # Then Record When The member is Identified and Softcopy is inserted
    def record(self):

        def generate_reference_number():
            timestamp = int(time.time() * 10)  # Get current timestamp in seconds
            random_num = random.randint(1000, 9999)  # Generate a random 4-digit number
            reference_number = f"{timestamp}{random_num}"
            return reference_number

        try:
            # Get count of existing rows in Contracts table
            reference_number = int(generate_reference_number())

            date_recorded = date.today()

            # Call search to get membership_id and found
            membership_id, found = self.search()
            

            # Call insert to get softcopy data
            softcopy = self.copy

            if softcopy is not None and found:
                # Insert new record into Contracts table
                cursor.execute("INSERT INTO Contracts (reference_number, member_id, softcopy_contract, date_recorded) VALUES (?, ?, ?, ?)",
                            (
                                reference_number,
                                membership_id, 
                                softcopy, 
                                date_recorded.strftime('%Y-%m-%d')
                            )
                        )
                
                connection.commit()
                QMessageBox.information(None, 'Success', 'Recorded')
    
            else:
                # Display error message if recording failed
                QMessageBox.critical(None, 'Error', 'Recording failed. Please try again.')

        except sqlite3.Error as e:
            # Handle any SQLite errors
            QMessageBox.critical(None, 'Error', 'Recording failed. Please try again.')
            print("error in sqlite3", e)
            connection.rollback()  # Rollback changes if error occurs

class View(QDialog):
    def __init__(self, item, parent=None):
        super(View, self).__init__(parent)
        self.setWindowTitle("Contract")
        self.resize(600, 900)
        self.setStyleSheet("background-color: #E0E0E0;")

        layout = QVBoxLayout(self)
        scrollArea = QScrollArea(self)
        layout.addWidget(scrollArea)
        
        container = QWidget()
        containerLayout = QVBoxLayout(container)
        self.loading = QMessageBox()
        self.loading.setIcon(QMessageBox.Information)
        self.loading.setWindowTitle("Loading")
        self.loading.setText("Loading PDF...")
        self.loading.show()

        try:
            # Open the document using the file path
            document = fitz.open(item)
            self.loading.show()
            for page_num in range(len(document)):  # Load pages on-demand
                page = document.load_page(page_num)
                label = QLabel()
                pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                if pix.width > 0 and pix.height > 0:
                    image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(image)
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    time.sleep(1)
                    containerLayout.addWidget(label)


        except Exception as e:
            error_label = QLabel(f"Error loading PDF: {e}")
            containerLayout.addWidget(error_label)

        if self.loading.isVisible():
            self.loading.close()

        scrollArea.setWidget(container)
        scrollArea.setWidgetResizable(True)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Payment()
    window.show()
    sys.exit(app.exec_())