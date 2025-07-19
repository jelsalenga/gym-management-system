from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from assets import *
import datetime

class Inventory(QWidget):
    def __init__(self, parent=None):
        super(Inventory, self).__init__(parent)
        self.setObjectName(u"Inventory")
        self.resize(950, 800)
        self.setMinimumSize(QSize(950, 800))
        self.setMaximumSize(QSize(950, 800))
        self.setStyleSheet(u"background-color: #FFFFFF;")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inventory')

       # Create a stacked widget
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(QRect(0, 0, 950, 800))
        

        # Create page 1
        self.page1 = QWidget(self.stacked_widget)
        self.page1.setWindowTitle("Equipments")
        self.setupPage1()
        self.loadData("Equipments")

        # Create page 2
        self.page2 = QWidget(self.stacked_widget)
        self.page2.setWindowTitle("Products")
        self.setupPage2()
        self.loadData("Products")

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)



    def setupPage1(self):
        self.equipment_lineEdit = createLineInput(
            parent=self.page1,
            name="lineEdit",
            geometry=QRect(30, 60, 451, 61),
            font=font5,
            style="",
            placeholder=""
        )

        self.equipment_searchButton = createButton(
            parent=self.page1,
            name="equipment_searchButton",
            geometry=QRect(480, 60, 111, 61),
            text="Search",
            font=font5,
            style="background: #4681f4; color: white"
        )

        self.equipment_statusSelect = createComboBox(
            parent = self.page1, 
            name = "equipment_statusSelect", 
            geometry = QRect(610, 60, 121, 61), 
            font = font5, 
            item = ("All", "Active", "Repair", "Retired"), 
            style = ""
        )


        self.equipment_stockButton = createButton(
            parent=self.page1,
            name="Stock",
            geometry=QRect(760, 60, 151, 61),
            text="Stock",
            font=font5,
            style="background: lime; color: white"
        )
        self.equipment_stockButton.clicked.connect(self.switchPage)
        self.equipment_searchButton.clicked.connect(lambda: self.search("Equipments"))
        self.loadData(lambda: "Equipments")
        
        self.tableWidget = QTableWidget(self.page1)
        self.tableWidget.setGeometry(QRect(30, 160, 891, 611))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # Adjust columns to content
        header.setStretchLastSection(True)
        self.tableWidget.setStyleSheet("background: white")


    def setupPage2(self):   
        self.stock_lineEdit = createLineInput(
            parent=self.page2,
            name="stock_lineEdit",
            geometry=QRect(40, 60, 471, 61),
            font=font5,
            style="",
            placeholder=" "
        )

        self.stock_searchButton = createButton(
            parent=self.page2,
            name="stock_searchButton",
            geometry=QRect(510, 60, 111, 61),
            text="Search",
            font=font5,
            style="background: #4681f4; color: white"
        )

        self.stock_date = createDate(
            parent=self.page2,
            name="stock_date",
            geometry=QRect(130, 140, 171, 41),
            font=font5,
            style=""
        )

        self.stock_dateDirectory = createComboBox(
            parent=self.page2,
            name="stock_dateDirectory",
            geometry=QRect(350, 140, 171, 41),
            font=font5,
            style="",
            item = ('on', 'before', 'after')
        )

        self.stock_startDatelabel = createLabel(
            parent=self.page2,
            name="stock_startDatelabel",
            geometry=QRect(50, 150, 71, 21),
            text="Expiry Date :",
            font=font5,
            style=""
        )

        self.stock_equipmentButton = createButton(
            parent=self.page2,
            name="Equipment",
            geometry=QRect(760, 60, 151, 61),
            text="Inventory",
            font=font5,
            style="background: lime; color: white"
        )

        self.stock_equipmentButton.clicked.connect(self.switchPage)
        self.stock_searchButton.clicked.connect(lambda: self.search("Products"))
        
        
        self.tableWidget2 = QTableWidget(self.page2)  # Assign to self.page2
        self.tableWidget2.setGeometry(QRect(30, 200, 891, 571))
        self.tableWidget2.setRowCount(0)
        self.tableWidget2.setColumnCount(10)
        self.tableWidget2.setObjectName("stocktableWidget")
        self.tableWidget2.verticalHeader().setVisible(False)
        self.tableWidget2.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        header2 = self.tableWidget2.horizontalHeader()
        header2.setSectionResizeMode(QHeaderView.Stretch)
        header2.setDefaultAlignment(Qt.AlignCenter)
        header2.setSectionResizeMode(QHeaderView.ResizeToContents)  # Adjust columns to content
        header2.setStretchLastSection(True)
        self.tableWidget2.setStyleSheet("background: white")
        self.loadData(lambda: "Products")


    def switchPage(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:
            self.loadData("Equipments")
        elif current_index == 1:
            self.loadData("Products")
        new_index = (current_index + 1) % 2
        self.stacked_widget.setCurrentIndex(new_index)

    def loadData(self, table):
        if table == "Equipments":
            # Load Table
            self.tableWidget.setRowCount(0)
            cursor.execute('PRAGMA table_info(Equipments)')
            columns_info = cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            column_names.append("")

            # Set column count and column names in table widget
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            cursor.execute("SELECT * FROM Equipments")
            for row_number, row_data in enumerate(cursor):
                self.tableWidget.insertRow(row_number)  
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignRight)
                    self.tableWidget.setItem(row_number, column_number, item)
        
        elif table == "Products":
            self.tableWidget2.setRowCount(0)
            cursor.execute('PRAGMA table_info(Products)')
            columns_info = cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            column_names.append("")

            # Set column count and column names in table widget
            self.tableWidget2.setHorizontalHeaderLabels(column_names)
            cursor.execute("SELECT * FROM Products")
            for row_number, row_data in enumerate(cursor):
                self.tableWidget2.insertRow(row_number)  
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignRight)
                    self.tableWidget2.setItem(row_number, column_number, item)

    def search(self, table):
        if table == "Equipments":
            search_term = self.equipment_lineEdit.text()
            select = self.equipment_statusSelect.currentIndex()
            
            if select == 0:
                status = ""
            elif select == 1:
                status = "Active"
            elif select == 2:
                status = "Repair"
            elif select == 3:
                status = "Retired"
            
            self.tableWidget.setRowCount(0)

            cursor.execute("""
                SELECT * 
                FROM Equipments 
                WHERE (CAST(equipment_id AS TEXT) LIKE ? OR 
                    CAST(equipment_name AS TEXT) LIKE ?) AND 
                    equipment_status LIKE ?
                """, (search_term + '%', search_term + '%', status + '%',))
            
            for row_number, row_data in enumerate(cursor):
                self.tableWidget.insertRow(row_number)  
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignRight)
                    self.tableWidget.setItem(row_number, column_number, item)

        elif table == "Products":
            search_term = self.stock_lineEdit.text()
            select = self.stock_dateDirectory.currentIndex()
            
            if select == 0:
                status = "="
            elif select == 1:
                status = "<"
            elif select == 2:
                status = ">"

            
            start = self.stock_date.date().toString(Qt.ISODate)


            self.tableWidget2.setRowCount(0)
            cursor.execute(f"""
                SELECT * 
                FROM Products 
                WHERE (CAST(product_id AS TEXT) LIKE ? OR 
                    CAST(name AS TEXT) LIKE ?) AND
                    expiry_date {status} ?
                """, (search_term + '%', search_term + '%', start))
            
            print(start)
            for row_number, row_data in enumerate(cursor):
                self.tableWidget2.insertRow(row_number)  
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignRight)
                    self.tableWidget2.setItem(row_number, column_number, item)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Inventory()
    window.show()
    sys.exit(app.exec_())
