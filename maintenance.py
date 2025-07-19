from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from assets import *
import shutil
import os

# ==============================================================================
# ==============================================================================
#                           MAINTENANCE    CLASS
# ==============================================================================
# ==============================================================================
class Maintenance(QWidget):
    def __init__(self, parent=None):
        super(Maintenance, self).__init__(parent)
        self.setObjectName("Form")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #FFFFFF")
        self.open_maintenance_interface()

    def assigned_input(self, entity):
        INPUTS = {}  # Initialize INPUTS to an empty dictionary

        if entity == "Employees":
            image = pixmap_to_bytes(self.create_employee_image_label.pixmap())
            INPUTS = {
                "employee_id": self.create_employee_id_output_label.text(),
                "first_name": self.create_employee_first_name_input.text(),
                "middle_name": self.create_employee_middle_name_input.text(),
                "last_name": self.create_employee_last_name_input.text(),
                "birthdate": self.create_employee_birth_date.date(),
                "gender": self.create_employee_gender_combo_box.currentText(),
                "address": self.create_employee_address_input.text(),
                "phone": self.create_employee_phone_number_input.text(),
                "hire_date": self.create_employee_hire_date.date(),
                "position": self.create_employee_position_input.text(),
                "photo": sqlite3.Binary(image),
            }

        elif entity == "Users":
            INPUTS = {
                "employee_id": self.user_employee_id_output_label.text(),
                "username": self.username_input.text(),
                "password": self.password_input.text(),
                "retry_password": self.re_password_input.text(),
                "role": self.role_combo_box.currentText()
            }

        elif entity == "Update Users":
            INPUTS = {
                "employee_id": self.view_user_employee_id_output_label.text(),
                "username": self.edit_username_input.text(),
                "password": self.edit_password_input.text(),
                "retry_password": self.re_edit_password_input.text(),
                "role": self.edit_role_combo_box_output.currentText()
            }

        elif entity == 'Equipments':
            INPUTS = {
                'equipment_id': self.create_equipment_id_output_label.text(), 
                'equipment_name': self.create_equipment_name_input.text(), 
                'equipment_serial_number': self.create_equipment_serial_number_input.text(), 
                'equipment_category': self.create_equipment_category_combo_box.currentText(), 
                'equipment_purchase_date': self.create_equipment_purchase_date.date().toString('yyyy-MM-dd'),
                'equipment_warranty_expiry': self.create_equipment_warranty_date.date().toString('yyyy-MM-dd'),
                'equipment_price': self.create_equipment_price_input.text(),
                'equipment_manufacturer': self.create_equipment_manufacturer_input.text(),
                'equipment_location': self.create_equipment_location_input.text(),
                'equipment_status': self.create_equipment_status_combo_box.currentText(),
            }

        elif entity == 'Update Equipments':
            INPUTS = {
                'equipment_id': self.edit_equipment_id_output_label.text(),
                'equipment_name': self.edit_equipment_name_input.text(),
                'equipment_serial_number': self.edit_equipment_serial_number_input.text(),
                'equipment_category': self.edit_equipment_category_combo_box.currentText(),
                'equipment_purchase_date': self.edit_equipment_purchase_date.date(),
                'equipment_warranty_expiry': self.edit_equipment_warranty_date.date(),
                'equipment_price': self.edit_equipment_price_input.text(),
                'equipment_manufacturer': self.edit_equipment_manufacturer_input.text(),
                'equipment_location': self.edit_equipment_location_input.text(),
                'equipment_status': self.edit_equipment_status_combo_box.currentText(),
            }

        elif entity == "Members":
            image = pixmap_to_bytes(self.member_image_label.pixmap())
            signature = pixmap_to_bytes(self.member_signature_label.pixmap())

            INPUTS = {
                "member_id": self.member_id_output_label.text(),
                "first_name": self.member_first_name_input.text(),
                "middle_name": self.member_middle_name_input.text(),
                "last_name": self.member_last_name_input.text(),
                "address": self.member_address_input.text(),
                "phone": self.member_phone_number_input.text(),
                "gender": self.member_gender_combo_box.currentText(),
                "membership_type": self.member_membership_type_combo_box.currentText(),
                "birthdate": self.member_birth_date.date(),
                "start_date": self.member_start_date.date(),
                "end_date": self.member_end_date.date(),
                "image": sqlite3.Binary(image),
                "signature": sqlite3.Binary(signature),
            }

        elif entity == "Update Member":
            image = pixmap_to_bytes(self.edit_member_image_label.pixmap())
            signature = pixmap_to_bytes(self.edit_member_signature_label.pixmap())

            INPUTS = {
                "first_name": self.edit_member_first_name_input.text(),
                "middle_name": self.edit_member_middle_name_input.text(),
                "last_name": self.edit_member_last_name_input.text(),
                "address": self.edit_member_address_input.text(),
                "phone": self.edit_member_phone_number_input.text(),
                "gender": self.edit_member_gender_combo_box.currentText(),
                "membership_type": self.edit_member_membership_type_combo_box.currentText(),
                "birthdate": self.edit_member_birth_date.date(),
                "start_date": self.edit_member_start_date.date(),
                "end_date": self.edit_member_end_date.date(),
                "image": sqlite3.Binary(image),
                "signature": sqlite3.Binary(signature),
                "member_id": self.edit_member_id_output_label.text()
            }

        elif entity == "Update Employee":
            photo = pixmap_to_bytes(self.edit_employee_image_label.pixmap())
            INPUTS = {
                'employee_id': self.edit_employee_id_output_label.text(), 
                'first_name': self.edit_employee_first_name_input.text(), 
                'middle_name': self.edit_employee_middle_name_input.text(), 
                'last_name': self.edit_employee_last_name_input.text(), 
                'birthdate': self.edit_employee_birth_date.date(),
                'gender': self.edit_employee_gender_combo_box.currentText(),
                'address': self.edit_employee_address_input.text(),
                'phone': self.edit_employee_phone_number_input.text(),
                'hire_date': self.edit_employee_hire_date.date(),
                'position': self.edit_employee_position_input.text(),
                'photo': sqlite3.Binary(photo),
            }

        elif entity == "Product":
            INPUTS = {
                'product_id': self.create_product_id_output_label.text(),
                'product_name': self.create_product_name_input.text(),
                'brand': self.create_product_brand_input.text(),
                'sku': self.create_product_brand_input.text(),
                'quantity':  self.create_product_quantity_input.text(),
                'supplier': self.create_product_supplier_input.text(),
                'price':  self.create_product_price_input.text(),
                'purchase_date':  self.create_product_purchase_date.date(),
                'expiry_date':  self.create_product_expiry_date.date(),
            }

        elif entity == "Update Contract":
            INPUTS = {
                'reference_number': self.edit_payment_ref_number_input.text(),
                'softcopy': self.copy,
                'date_recorded': self.edit_payment_date_input.text(),
            }

        else:
            # Handle unexpected entity values
            print(f"Unexpected entity: {entity}")
            return {}  # Return an empty dictionary for unexpected entities

        return INPUTS

    
    
    def open_maintenance_interface(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
  
        self.open_main_page()           # MAINTENANCE MAIN PAGE


        # ========================     MEMBER MAINTENANCE
        self.open_member_page()
        self.open_create_member() 
        self.open_edit_member()
        self.open_view_member()

        # =======================      EMPLOYEE MAINTENANCE

        self.open_employee_page()
        self.create_employee()
        self.edit_employee()
        self.view_employee()

        # ========================     USER MAINTENANCE

        self.open_user_page()
        self.open_create_user_page()
        self.open_view_user_page()
        

        # ========================     PRODUCT MAINTENANCE

        self.open_product()
        self.create_product()
        self.edit_product()
        self.view_product()

        # ========================     EQUIPMENT MAINTENANCE

        self.open_equipment_page()
        self.create_equipment()
        self.view_equipment()
        self.edit_equipment()


        # ========================     PAYMENT MAINTENANCE

        self.open_payment_page()
        self.view_payment_page()
        self.edit_payment_page()

        self.verticalLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_member_page(self):
        update_table_widget("Members", self.member_table_widget, self.show_view_member_temp)
        self.stackedWidget.setCurrentIndex(1)
    
    def show_add_member(self):
        clear_inputs(self.member_page)
        generate_id("Members", self.member_id_output_label)
        self.stackedWidget.setCurrentIndex(2)
    
    def show_edit_member(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_view_member(self):
        self.stackedWidget.setCurrentIndex(4)

    def show_employee_page(self):
        update_table_widget("Employees", self.employee_table_widget, self.show_view_employee_temp)
        self.stackedWidget.setCurrentIndex(5)

    def show_create_employee(self):
        clear_inputs(self.create_employee_page)
        generate_id("Employees", self.create_employee_id_output_label)
        self.stackedWidget.setCurrentIndex(6)

    def show_edit_employee(self):
        self.stackedWidget.setCurrentIndex(7)

    def show_view_employee(self):
        self.stackedWidget.setCurrentIndex(8)

    def show_user_page(self):
        update_table_widget("Users", self.user_table_widget, self.show_view_user_temp)
        self.stackedWidget.setCurrentIndex(9)
    def show_create_user(self):
        clear_inputs(self.create_user_page)
        self.stackedWidget.setCurrentIndex(10)

    def show_edit_user(self):
        self.stackedWidget.setCurrentIndex(11)

    def show_product_page(self):
        update_table_widget("Products", self.product_table_widget, self.show_view_product_temp)
        self.stackedWidget.setCurrentIndex(12)

    def show_create_product(self):
        clear_inputs(self.create_product_page)
        generate_id("Products", self.create_product_id_output_label)
        self.stackedWidget.setCurrentIndex(13)

    def show_edit_product(self):
        self.stackedWidget.setCurrentIndex(14)

    def show_view_product(self):
        self.stackedWidget.setCurrentIndex(15)

    def show_equipment_page(self):
        update_table_widget("Equipments", self.equipment_table_widget, self.show_view_equipment_temp)
        self.stackedWidget.setCurrentIndex(16)
    
    def show_create_equipment_page(self):
        generate_id("Equipments", self.create_equipment_id_output_label)
        self.stackedWidget.setCurrentIndex(17)
    
    def show_view_equipment_page(self):
        self.stackedWidget.setCurrentIndex(18)

    def show_edit_equipment_page(self):
        self.stackedWidget.setCurrentIndex(19)

    def show_payment_page(self):
        self.stackedWidget.setCurrentIndex(20)

    def show_view_payment_page(self):
        self.stackedWidget.setCurrentIndex(21)

    def show_edit_payment_page(self):
        self.stackedWidget.setCurrentIndex(22)

    def open_main_page(self):
        self.main_page = QWidget()
        self.main_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.main_page)
        # ===========================================
        #             MAIN PAGE LABEL
        # ===========================================

        self.maintenance_text_label = createLabel(
            parent = self.main_page,
            name = "maintenance_text",
            geometry = QRect(360, 90, 230, 40),
            text = "Maintenance",
            font = font4,
            style = "font: bold"
        )
        # ===========================================
        #             MAIN PAGE BUTTONS
        # ===========================================
        self.switch_member_page_button = createButton(
            parent = self.main_page,
            name = "member_page_button",
            geometry = QRect(140, 190, 300, 100),
            text = "Manage Members",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_employee_page_button = createButton(
            parent = self.main_page,
            name = "employee_page_button",
            geometry = QRect(140, 340, 300, 100),
            text = "Manage Employees",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_user_page_button = createButton(
            parent = self.main_page,
            name = "user_page_button",
            geometry = QRect(140, 480, 300, 100),
            text = "Manage User Accounts",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_equipment_page_button = createButton(
            parent = self.main_page,
            name = "equipment_page_button",
            geometry = QRect(500, 190, 300, 100),
            text = "Manage Equipment",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_product_page_button = createButton(
            parent = self.main_page,
            name = "product_page_button",
            geometry = QRect(500, 340, 300, 100),
            text = "Manage Products",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_payment_page_button = createButton(
            parent = self.main_page,
            name = "payment_page_button",
            geometry = QRect(500, 480, 300, 100),
            text = "Manage Payments",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_backup_button = createButton(
            parent = self.main_page,
            name = "backup_page_button",
            geometry = QRect(140, 630, 300, 100),
            text = "Backup",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_restore_button = createButton(
            parent = self.main_page,
            name = "restore_button",
            geometry = QRect(500, 630, 300, 100),
            text = "Restore",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_member_page_button.clicked.connect(self.show_member_page)
        self.switch_employee_page_button.clicked.connect(self.show_employee_page)
        self.switch_user_page_button.clicked.connect(self.show_user_page)
        self.switch_product_page_button.clicked.connect(self.show_product_page)
        self.switch_equipment_page_button.clicked.connect(self.show_equipment_page)
        self.switch_payment_page_button.clicked.connect(self.show_payment_page)
        self.switch_backup_button.clicked.connect(self.backup_path)
        self.switch_restore_button.clicked.connect(self.restore_path)
#========================================================================================================================
#                                     MEMBER MAINTENANCE
#========================================================================================================================

    def open_member_page(self):
        self.manage_member_page = QWidget()
        self.manage_member_page.setObjectName("manage_member_page")

        # ===========================================
        #         MANAGE MEMBER PAGE LABELS
        # ===========================================
        self.manage_member_text_label = createLabel(
            parent=self.manage_member_page,
            name="manage_members_text",
            geometry=QRect(120, 40, 310, 40),
            text="Manage Members",
            font=font4,
            style="font: bold"
        )

        self.manage_search_text_label = createLabel(
            parent=self.manage_member_page,
            name="manage_members_text",
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
            font=font1,
            style=""
        )

        # ===========================================
        #      MANAGE MEMBER PAGE LINE INPUTS
        # ===========================================
        self.manage_search_input = createLineInput(
            parent=self.manage_member_page,
            name="search_input",
            geometry=QRect(130, 140, 580, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.manage_search_input.setPlaceholderText("Member ID / Name")
    

        # ===========================================
        #         MANAGE MEMBER TABLE WIDGET
        # ===========================================
        self.member_table_widget = QTableWidget(self.manage_member_page)
        self.member_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.member_table_widget.setRowCount(0)
        self.member_table_widget.setColumnCount(7)  # Limited columns

        # Set the horizontal header labels
        self.member_table_widget.setHorizontalHeaderLabels(
            ["Member ID", "Full Name", "Membership Type", "Phone Number", "Membership End Date", "Actions", "Void"],
        )

        self.stackedWidget.addWidget(self.manage_member_page)

        self.member_table_widget.resizeColumnsToContents()
        self.member_table_widget.resizeRowsToContents()
        self.member_table_widget.horizontalHeader().setStretchLastSection(True)
        self.member_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.manage_search_input.textChanged.connect(lambda: search_entity("Members", self.manage_search_input, self.member_table_widget, self.show_view_member_temp))
        update_table_widget('Members', self.member_table_widget, self.show_view_member_temp)


        #         MANAGE MEMBER BUTTONS
        # ===========================================
        self.member_back_button = createButton(
            parent=self.manage_member_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.member_add_button = createButton(
            parent=self.manage_member_page,
            name="add_button",
            geometry=QRect(680, 40, 250, 50),
            text="Add Member",
            font=font2,
            style="background-color: #28a745; color: #FFFFFF"
        )

        self.member_back_button.clicked.connect(self.show_main_page)
        self.member_add_button.clicked.connect(self.show_add_member)
    
    def open_create_member(self):
        self.member_page = QWidget()
        self.member_page.setObjectName("member_page")
        self.stackedWidget.addWidget(self.member_page)

        # ===========================================
        #             MEMBER PAGE LABELS
        # ===========================================

        # List of label properties
     
        labels_info = [
            {"geometry": QRect(310, 50, 380, 40), "text": "Member Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Membership ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Membership Type"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Start Date"},
            {"geometry": QRect(280, 630, 180, 40), "text": "End Date"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.member_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )
        
        # IMAGE LABEL 
        self.member_image_label = createOutputLabel(
            parent = self.member_page,
            geometry = QRect(680, 140, 250, 250),
        )
        
        # SIGNATURE LABEL
        self.member_signature_label = createOutputLabel(
            parent = self.member_page,
            geometry = QRect(750, 460, 180, 90),

        )

        # ===========================================
        #             MEMBER PAGE INPUTS
        # ===========================================

        self.member_id_output_label = createOutputLabel(
            parent=self.member_page,
            geometry=QRect(240, 150, 410, 40)
        )

        self.member_first_name_input = createLineInput(
            parent=self.member_page,
            geometry=QRect(40, 260, 330, 40),
        )

        self.member_middle_name_input = createLineInput(
            parent=self.member_page,
            geometry=QRect(380, 260, 280, 40),
        )

        self.member_last_name_input = createLineInput(
            parent=self.member_page,
            geometry=QRect(40, 360, 330, 40),
        )

        self.member_address_input = createLineInput(
            parent=self.member_page,
            geometry=QRect(40, 470, 330, 40),
        )

        self.member_phone_number_input = createLineInput(
            parent=self.member_page,
            geometry=QRect(40, 570, 330, 40),
        )

        # ===========================================
        #            MEMBER PAGE COMBO BOX
        # ===========================================

        self.member_gender_combo_box = createComboBox(
            parent=self.member_page,
            geometry=QRect(380, 360, 140, 40),
            item=['Male', 'Female'],
        )

        self.member_membership_type_combo_box = createComboBox(
            parent=self.member_page,
            geometry=QRect(380, 570, 210, 40),
            item=['Standard', 'Lifetime'],
        )

        self.member_membership_type_combo_box.currentIndexChanged.connect(self.update_end_date)

        # ===========================================
        #              MEMBER PAGE DATE
        # ===========================================

        self.member_birth_date = createDate(
            parent=self.member_page,
            geometry=QRect(380, 470, 200, 40),
        )

        self.member_start_date = createDate(
            parent=self.member_page,
            geometry=QRect(40, 670, 200, 40),
        )

        disable_past_date(self.member_start_date)

        self.member_end_date = createDate(
            parent=self.member_page,
            geometry=QRect(280, 670, 200, 40),
        )

        disable_past_date(self.member_end_date)

        # ===========================================
        #              MEMBER PAGE BUTTONS
        # ===========================================

        self.member_back_button = createButton(
            parent=self.member_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A; color: #FFFFFF"
        )

        self.member_insert_image_button = createButton(
            parent=self.member_page,
            name="insert_image_button",
            geometry=QRect(680, 400, 250, 50),
            text="Insert Image",
            font=font3,
            style="background-color: #004F9A; color: #FFFFFF"
        )

        self.member_insert_signature_button = createButton(
            parent=self.member_page,
            name="insert_signature_button",
            geometry=QRect(680, 560, 250, 50),
            text="Insert Signature",
            font=font3,
            style="background-color: #004F9A; color: #FFFFFF"
        )

        self.member_clear_button = createButton(
            parent=self.member_page,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Clear",
            font=font3,
            style="background-color: #882400; color: #FFFFFF"
        )

        self.member_register_button = createButton(
            parent=self.member_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Register",
            font=font3,
            style="background-color: #006646; color: #FFFFFF"
        )

        self.member_back_button.clicked.connect(self.show_member_page)
        self.member_clear_button.clicked.connect(lambda: clear_inputs(self.member_page))
        self.member_register_button.clicked.connect(lambda: register_member(self.assigned_input("Members"), self.member_page, self.member_id_output_label))
        self.member_insert_image_button.clicked.connect(lambda: insert_image(self.member_image_label))
        self.member_insert_signature_button.clicked.connect(lambda: insert_image(self.member_signature_label))

    def open_edit_member(self):
        self.edit_member = QWidget()
        self.edit_member.setObjectName("member_page")
        self.stackedWidget.addWidget(self.edit_member)

        # ===========================================
        #             MEMBER PAGE LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(310, 50, 380, 40), "text": "Edit Member Details", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Membership ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Membership Type"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Start Date"},
            {"geometry": QRect(280, 630, 180, 40), "text": "End Date"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.edit_member,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        # IMAGE LABEL 
        self.edit_member_image_label = createOutputLabel(
            parent=self.edit_member,
            geometry=QRect(680, 140, 250, 250),
        )

        # SIGNATURE LABEL
        self.edit_member_signature_label = createLabel(
            parent=self.edit_member,
            geometry=QRect(750, 460, 180, 90),
        )

        # ===========================================
        #             MEMBER PAGE INPUTS
        # ===========================================

        self.edit_member_id_output_label = createOutputLabel(
            parent=self.edit_member,
            geometry=QRect(240, 150, 410, 40),

        )

        self.edit_member_first_name_input = createLineInput(
            parent=self.edit_member,
            geometry=QRect(40, 260, 330, 40),

        )

        self.edit_member_middle_name_input = createLineInput(
            parent=self.edit_member,
            geometry=QRect(380, 260, 280, 40),
        )

        self.edit_member_last_name_input = createLineInput(
            parent=self.edit_member,
            geometry=QRect(40, 360, 330, 40),
        )

        self.edit_member_address_input = createLineInput(
            parent=self.edit_member,
            geometry=QRect(40, 470, 330, 40),
        )

        self.edit_member_phone_number_input = createLineInput(
            parent=self.edit_member,
            geometry=QRect(40, 570, 330, 40),

        )
        # ===========================================
        #            MEMBER PAGE COMBO BOX
        # ===========================================

        self.edit_member_gender_combo_box = createComboBox(
            parent=self.edit_member,
            geometry=QRect(380, 360, 140, 40),
            item=['Male', 'Female'],

        )

        self.edit_member_membership_type_combo_box = createComboBox(
            parent=self.edit_member,
            geometry=QRect(380, 570, 210, 40),
            item=['Standard', 'Lifetime'],

        )

        self.edit_member_membership_type_combo_box.currentIndexChanged.connect(self.update_end_date)

        # ===========================================
        #              MEMBER PAGE DATE
        # ===========================================

        self.edit_member_birth_date = createDate(
            parent=self.edit_member,
            geometry=QRect(380, 470, 200, 40),
        )

        self.edit_member_start_date = createDate(
            parent=self.edit_member,
            geometry=QRect(40, 670, 200, 40),
        )

        self.edit_member_end_date = createDate(
            parent=self.edit_member,
            geometry=QRect(280, 670, 200, 40),

        )

        # ===========================================
        #              MEMBER PAGE BUTTONS
        # ===========================================

        self.edit_member_back_button = createButton(
            parent=self.edit_member,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.edit_member_insert_image_button = createButton(
            parent=self.edit_member,
            name="insert_image_button",
            geometry=QRect(680, 400, 250, 50),
            text="Insert Image",
            font=font3,
            style="background-color: #004F9A"
        )

        self.edit_member_insert_signature_button = createButton(
            parent=self.edit_member,
            name="insert_signature_button",
            geometry=QRect(680, 560, 250, 50),
            text="Insert Signature",
            font=font3,
            style="background-color: #004F9A"
        )

        self.edit_member_clear_button = createButton(
            parent=self.edit_member,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Cancel",
            font=font3,
            style="background-color: #882400"
        )

        self.edit_member_update_button = createButton(
            parent=self.edit_member,
            name="update_button",
            geometry=QRect(690, 730, 250, 50),
            text="Update Member",
            font=font3,
            style="background-color: #006646"
        )

        self.edit_member_back_button.clicked.connect(self.show_view_member)
        self.edit_member_clear_button.clicked.connect(self.show_view_member)
        self.edit_member_insert_image_button.clicked.connect(lambda: insert_image(self.edit_member_image_label))
        self.edit_member_insert_signature_button.clicked.connect(lambda: insert_image(self.edit_member_signature_label))
        self.edit_member_update_button.clicked.connect(lambda: update_member(self.assigned_input("Update Member"), self.show_member_page))

    def open_view_member(self):
        self.view_member = QWidget()
        self.view_member.setObjectName("member_page")
        self.stackedWidget.addWidget(self.view_member)

        # ===========================================
        #             MEMBER PAGE LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(310, 50, 380, 40), "text": "Member Details", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Membership ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Membership Type"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Start Date"},
            {"geometry": QRect(280, 630, 180, 40), "text": "End Date"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.view_member,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        # ===========================================
        #           MEMBER PAGE OUTPUT LABELS
        # ===========================================

         # MEMBER ID OUTPUT LABEL
        self.view_member_id_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(240, 150, 410, 40),
        )

        # FIRST NAME OUTPUT LABEL
        self.view_member_first_name_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(40, 260, 330, 40),
        )

        # MIDDLE NAME OUTPUT LABEL
        self.view_member_middle_name_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(380, 260, 280, 40),
        )

        # LAST NAME OUTPUT LABEL
        self.view_member_last_name_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(40, 360, 330, 40),
        )

        # GENDER OUTPUT LABEL
        self.view_member_gender_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(380, 360, 140, 40),
        )

        # ADDRESS OUTPUT LABEL
        self.view_member_address_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(40, 470, 330, 40),
        )

        # BIRTHDATE OUTPUT LABEL
        self.view_member_birthdate_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(380, 470, 200, 40),
        )

        # PHONE NUMBER OUTPUT LABEL
        self.view_member_phone_number_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(40, 570, 330, 40),
        )

        # MEMBERSHIP TYPE OUTPUT LABEL
        self.view_member_membership_type_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(380, 570, 210, 40),
        )

        # START DATE OUTPUT LABEL
        self.view_member_start_date_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(40, 670, 200, 40),
        )

        # END DATE OUTPUT LABEL
        self.view_member_end_date_output_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(280, 670, 200, 40),
        )

        # IMAGE LABEL 
        self.view_member_image_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(680, 140, 250, 250),
        )

        # SIGNATURE LABEL
        self.view_member_signature_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(750, 460, 180, 90),
        )

        # IMAGE LABEL
        self.view_member_image_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(680, 140, 250, 250),
        )

        # SIGNATURE LABEL
        self.view_member_signature_label = createOutputLabel(
            parent=self.view_member,
            geometry=QRect(750, 460, 180, 90),
        )

        # ===========================================
        #              MEMBER PAGE BUTTONS
        # ===========================================

        self.view_member_back_button = createButton(
            parent=self.view_member,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.view_member_register_button = createButton(
            parent=self.view_member,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Edit",
            font=font3,
            style="background-color: #006646; color: #FFFFFF"
        )

        # Connect the buttons to the appropriate functions
        self.view_member_back_button.clicked.connect(self.show_member_page)
        self.view_member_register_button.clicked.connect(self.edit_member_button)


    def update_end_date(self):
        membership_type = self.member_membership_type_combo_box.currentText()
        if membership_type == "Lifetime":
            self.member_end_date.setDate(QDate(9999, 12, 31))  # Set to a far future date
            self.member_end_date.setDisabled(True)  # Optionally disable the end date field
        else:
            self.member_end_date.setDisabled(False)
            self.member_end_date.setDate(QDate.currentDate())  # Reset to the current date

    
    def show_view_member_temp(self, row):
        member_id = self.member_table_widget.item(row, 0).text()

        cursor.execute(
            """
            SELECT * 
            FROM Members
            WHERE member_id = ?
            """,
            (member_id,)
        )

        results = cursor.fetchone()

        if results is None:
            # Handle the case where no member is found
            QMessageBox.warning(None, "No Member Found", f"No member found with ID: {member_id}")
            return

        # Unpack the results
        (employee_id, first_name, middle_name, last_name, address, gender, birthdate, phone,
        membership_type, start_date, end_date, photo, signature, void) = results

        pixmap = QPixmap()
        pixmap_2 = QPixmap()
        
        # Update the labels with member details
        self.view_member_id_output_label.setText(employee_id)
        self.view_member_first_name_output_label.setText(first_name)
        self.view_member_middle_name_output_label.setText(middle_name)
        self.view_member_last_name_output_label.setText(last_name)
        self.view_member_birthdate_output_label.setText(birthdate)
        self.view_member_gender_output_label.setText(gender)
        self.view_member_address_output_label.setText(address)
        self.view_member_phone_number_output_label.setText(phone)
        self.view_member_membership_type_output_label.setText(membership_type)
        self.view_member_start_date_output_label.setText(start_date)
        self.view_member_end_date_output_label.setText(end_date)

        if photo:
            pixmap.loadFromData(photo)
            self.view_member_image_label.setPixmap(pixmap)
        else:
            # Handle the case where no photo is available
            self.view_member_image_label.setText("No photo available")

        if signature:
            pixmap_2.loadFromData(signature)
            self.view_member_signature_label.setPixmap(pixmap_2)
        else:
            # Handle the case where no signature is available
            self.view_member_signature_label.setText("No signature available")

        self.show_view_member()

    
    def edit_member_button(self):
        employee_id =  self.view_member_id_output_label.text()
        first_name = self.view_member_first_name_output_label.text()
        middle_name = self.view_member_middle_name_output_label.text()
        last_name = self.view_member_last_name_output_label.text()
        birthdate = self.view_member_birthdate_output_label.text()
        gender = self.view_member_gender_output_label.text()
        address =self.view_member_address_output_label.text()
        phone = self.view_member_phone_number_output_label.text()
        membership_type = self.view_member_membership_type_output_label.text()
        start_date = self.view_member_start_date_output_label.text()
        end_date = self.view_member_end_date_output_label.text()
        photo = self.view_member_image_label.pixmap()
        signature = self.view_member_signature_label.pixmap()

        birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.edit_member_id_output_label.setText(employee_id)
        self.edit_member_first_name_input.setText(first_name)
        self.edit_member_middle_name_input.setText(middle_name)
        self.edit_member_last_name_input.setText(last_name)
        self.edit_member_birth_date.setDate(birthdate)
        self.edit_member_gender_combo_box.setCurrentText(gender)
        self.edit_member_address_input.setText(address)
        self.edit_member_phone_number_input.setText(phone)
        self.edit_member_membership_type_combo_box.setCurrentText(membership_type)
        self.edit_member_start_date.setDate(start_date)
        self.edit_member_end_date.setDate(end_date)

        self.edit_member_image_label.setPixmap(photo)
        self.edit_member_signature_label.setPixmap(signature)
        update_table_widget('Members', self.member_table_widget, self.show_view_member_temp)
        self.show_edit_member()
    
    def add_view_buttons(self):
   
        for row in range(self.member_table_widget.rowCount()):
            view_button = QPushButton("View")
            view_button.clicked.connect(partial(self.show_view_member_temp, row))
            self.member_table_widget.setCellWidget(row, 5, view_button)

#========================================================================================================================
#                                     EMPLOYEE MAINTENANCE
#========================================================================================================================
    def open_employee_page(self):
        self.employee_page = QWidget()
        self.employee_page.setObjectName("employee_page")

        # ===========================================
        #         MANAGE MEMBER PAGE LABELS
        # ===========================================
        self.manage_employee_text_label = createLabel(
            parent=self.employee_page,
            name="manage_members_text",
            geometry=QRect(120, 40, 350, 40),
            text="Manage Employees",
            font=font4,
            style="font: bold"
        )

        self.manage_search_text_label = createLabel(
            parent=self.employee_page,
            name="manage_members_text",
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
            font=font1,
            style=""
        )

        # ===========================================
        #      MANAGE MEMBER PAGE LINE INPUTS
        # ===========================================
        self.manage_employee_search_input = createLineInput(
            parent=self.employee_page,
            name="search_input",
            geometry=QRect(130, 140, 580, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.manage_employee_search_input.setPlaceholderText("Employee ID / Name")

        # ===========================================
        #         MANAGE MEMBER TABLE WIDGET
        # ===========================================
        self.employee_table_widget = QTableWidget(self.employee_page)
        self.employee_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.employee_table_widget.setRowCount(0)
        self.employee_table_widget.setColumnCount(7)# Limited columns
    
        self.manage_employee_search_input.textChanged.connect(lambda: search_entity("Employees", self.manage_employee_search_input, self.employee_table_widget, self.show_view_employee_temp))
        # Set the horizontal header labels
        self.employee_table_widget.setHorizontalHeaderLabels(
            ["Employee ID", "Full Name", "Position", "Phone", "Hire Date", "Actions", "Void"]
        )

        self.stackedWidget.addWidget(self.employee_page)
        self.employee_table_widget.resizeColumnsToContents()
        self.employee_table_widget.resizeRowsToContents()
        self.employee_table_widget.horizontalHeader().setStretchLastSection(True)
        self.employee_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        update_table_widget("Employees", self.employee_table_widget, self.show_view_employee_temp)

        #         MANAGE MEMBER BUTTONS
        # ===========================================
        self.employee_back_button = createButton(
            parent=self.employee_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.member_add_button = createButton(
            parent=self.employee_page,
            name="add_button",
            geometry=QRect(680, 40, 250, 50),
            text="Add Employee",
            font=font2,
            style="background-color: #28a745; color: #FFFFFF"
        )

        self.employee_back_button.clicked.connect(self.show_main_page)
        self.member_add_button.clicked.connect(self.show_create_employee)

    def create_employee(self):
        self.create_employee_page = QWidget()
        self.create_employee_page.setObjectName("create_employee_page")
        self.stackedWidget.addWidget(self.create_employee_page)

        # ===========================================
        #             EMPLOYEE PAGE LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(305, 50, 400, 40), "text": "Employee Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Employee ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Position"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Hire Date"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.create_employee_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        self.create_employee_id_output_label = createOutputLabel(
            parent=self.create_employee_page,
            name="employee_id_output",
            geometry=QRect(240, 150, 410, 40)
        )

        self.create_employee_first_name_input = createLineInput(
            parent=self.create_employee_page,
            name="first_name_output",
            geometry=QRect(40, 260, 330, 40)
        )

        self.create_employee_middle_name_input = createLineInput(
            parent=self.create_employee_page,
            name="middle_name_output",
            geometry=QRect(380, 260, 280, 40)
        )

        self.create_employee_last_name_input = createLineInput(
            parent=self.create_employee_page,
            name="last_name_output",
            geometry=QRect(40, 360, 330, 40)
        )

        self.create_employee_address_input = createLineInput(
            parent=self.create_employee_page,
            name="address_output",
            geometry=QRect(40, 470, 330, 40)
        )

        self.create_employee_phone_number_input = createLineInput(
            parent=self.create_employee_page,
            name="phone_number_output",
            geometry=QRect(40, 570, 330, 40)
        )

        self.create_employee_gender_combo_box = createComboBox(
            parent=self.create_employee_page,
            name="gender_combo_box",
            geometry=QRect(380, 360, 140, 40),
            item=['Male', 'Female']
        )

        self.create_employee_position_input = createLineInput(
            parent=self.create_employee_page,
            name="position",
            geometry=QRect(380, 570, 210, 40)
        )

        self.create_employee_birth_date = createDate(
            parent=self.create_employee_page,
            name="birthdate",
            geometry=QRect(380, 470, 200, 40)
        )

        self.create_employee_hire_date = createDate(
            parent=self.create_employee_page,
            name="employee_start_date",
            geometry=QRect(40, 670, 200, 40)
        )

        self.create_employee_image_label = createOutputLabel(
            parent=self.create_employee_page,
            name="image_label",
            geometry=QRect(680, 140, 250, 250)
        )

        self.create_employee_back_button = createButton(
            parent=self.create_employee_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.create_employee_insert_image_button = createButton(
            parent=self.create_employee_page,
            name="insert_image_button",
            geometry=QRect(680, 400, 250, 50),
            text="Insert Image",
            font=font3,
            style="background-color: #004F9A"
        )

        self.create_employee_clear_button = createButton(
            parent=self.create_employee_page,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Clear",
            font=font3,
            style="background-color: #882400"
        )

        self.create_employee_register_button = createButton(
            parent=self.create_employee_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Register",
            font=font3,
            style="background-color: #006646"
        )

        self.create_employee_clear_button.clicked.connect(lambda: clear_inputs(self.create_employee_page))
        self.create_employee_insert_image_button.clicked.connect(lambda: insert_image(self.create_employee_image_label))
        self.create_employee_back_button.clicked.connect(self.show_employee_page)
        self.create_employee_register_button.clicked.connect(lambda: register_employee(self.assigned_input('Employees'), self.create_employee_page, self.create_employee_id_output_label))

    
    
        
    def view_employee(self):
        self.view_employee_page = QWidget()
        self.view_employee_page.setObjectName("view_employee_page")
        self.stackedWidget.addWidget(self.view_employee_page)

        # ===========================================
        #             EMPLOYEE PAGE LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(305, 50, 385, 40), "text": "Employee Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Employee ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name:"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name:"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name:"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender:"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address:"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate:"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number:"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Position:"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Hire Date:"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.view_employee_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        self.view_employee_id_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="employee_id_output",
            geometry=QRect(240, 150, 410, 40)
        )

        self.view_employee_first_name_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="first_name_output",
            geometry=QRect(40, 260, 330, 40)
        )

        self.view_employee_middle_name_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="middle_name_output",
            geometry=QRect(380, 260, 280, 40)
        )

        self.view_employee_last_name_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="last_name_output",
            geometry=QRect(40, 360, 330, 40)
        )

        self.view_employee_gender_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="gender_output",
            geometry=QRect(380, 360, 140, 40)
        )

        self.view_employee_address_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="address_output",
            geometry=QRect(40, 470, 330, 40)
        )

        self.view_employee_birthdate_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="birthdate_output",
            geometry=QRect(380, 470, 200, 40)
        )

        self.view_employee_phone_number_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="phone_number_output",
            geometry=QRect(40, 570, 330, 40)
        )

        self.view_employee_position_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="position_output",
            geometry=QRect(380, 570, 210, 40)
        )

        self.view_employee_hire_date_output_label = createOutputLabel(
            parent=self.view_employee_page,
            name="hire_date_output",
            geometry=QRect(40, 670, 200, 40)
        )

        self.view_employee_image_label = createOutputLabel(
            parent=self.view_employee_page,
            name="image_label",
            geometry=QRect(680, 140, 250, 250)
        )

        # ===========================================
        #              EMPLOYEE PAGE BUTTONS
        # ===========================================

        self.view_employee_back_button = createButton(
            parent=self.view_employee_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.view_employee_register_button = createButton(
            parent=self.view_employee_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Edit",
            font=font3,
            style="background-color: #006646; color: #FFFFFF"
        )

        self.view_employee_back_button.clicked.connect(self.show_employee_page)
        self.view_employee_register_button.clicked.connect(self.edit_employee_button)



    def edit_employee(self):
        self.edit_employee_page = QWidget()
        self.edit_employee_page.setObjectName("edit_employee_page")
        self.stackedWidget.addWidget(self.edit_employee_page)

        # ===========================================
        #             EMPLOYEE PAGE LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(305, 50, 385, 40), "text": "Employee Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 191, 40), "text": "Employee ID:"},
            {"geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 530, 210, 40), "text": "Position"},
            {"geometry": QRect(40, 630, 180, 40), "text": "Hire Date"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.edit_employee_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        self.edit_employee_id_output_label = createOutputLabel(
            parent=self.edit_employee_page,
            geometry=QRect(240, 150, 410, 40),
        )

        self.edit_employee_image_label = createOutputLabel(
            parent=self.edit_employee_page,
            geometry=QRect(680, 140, 250, 250),
        )

        # ===========================================
        #             EMPLOYEE PAGE INPUTS
        # ===========================================

                # FIRST NAME INPUT
        self.edit_employee_first_name_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(40, 260, 330, 40),
        )

        # MIDDLE NAME INPUT
        self.edit_employee_middle_name_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(380, 260, 280, 40),
        )

        # LAST NAME INPUT
        self.edit_employee_last_name_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(40, 360, 330, 40),
        )

        # ADDRESS INPUT
        self.edit_employee_address_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(40, 470, 330, 40),
        )

        # PHONE NUMBER INPUT
        self.edit_employee_phone_number_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(40, 570, 330, 40),
        )

        # EMPLOYEE TYPE BOX
        self.edit_employee_position_input = createLineInput(
            parent=self.edit_employee_page,
            geometry=QRect(380, 570, 210, 40),
        )

        # ===========================================
        #            EMPLOYEE PAGE COMBO BOX
        # ===========================================

        self.edit_employee_gender_combo_box = createComboBox(
            parent=self.edit_employee_page,
            geometry=QRect(380, 360, 140, 40),
            item=['Male', 'Female'],
        )

        # ===========================================
        #              EMPLOYEE PAGE DATE
        # ===========================================

        self.edit_employee_birth_date = createDate(
            parent=self.edit_employee_page,
            geometry=QRect(380, 470, 200, 40),
        )

        self.edit_employee_hire_date = createDate(
            parent=self.edit_employee_page,
            geometry=QRect(40, 670, 200, 40),
        )

        # ===========================================
        #              EMPLOYEE PAGE BUTTONS
        # ===========================================

        self.edit_employee_back_button = createButton(
            parent=self.edit_employee_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.edit_employee_insert_image_button = createButton(
            parent=self.edit_employee_page,
            name="insert_image_button",
            geometry=QRect(680, 400, 250, 50),
            text="Insert Image",
            font=font3,
            style="background-color: #004F9A"
        )

        self.edit_employee_cancel_button = createButton(
            parent=self.edit_employee_page,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Cancel",
            font=font3,
            style="background-color: #882400"
        )

        self.edit_employee_register_button = createButton(
            parent=self.edit_employee_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Change",
            font=font3,
            style="background-color: #006646"
        )

        self.edit_employee_back_button.clicked.connect(self.show_view_employee)
        self.edit_employee_cancel_button.clicked.connect(self.show_view_employee)
        self.edit_employee_insert_image_button.clicked.connect(lambda: insert_image(self.edit_employee_image_label))
        self.edit_employee_register_button.clicked.connect(lambda: update_employee(self.assigned_input("Update Employee"), self.show_employee_page))


    def show_view_employee_temp(self, row):
        employee_id = self.employee_table_widget.item(row, 0).text()

        cursor.execute(
            """
            SELECT * 
            FROM Employees
            WHERE employee_id = ?
            """,
            (employee_id,)
        )

        results = cursor.fetchone()

        employee_id, first_name, middle_name, last_name, birth_date, gender, address, phone, hire_date, position, photo, void = results

        pixmap = QPixmap()
        self.view_employee_id_output_label.setText(str(employee_id))
        self.view_employee_first_name_output_label.setText(first_name)
        self.view_employee_middle_name_output_label.setText(middle_name)
        self.view_employee_last_name_output_label.setText(last_name)
        self.view_employee_birthdate_output_label.setText(birth_date)
        self.view_employee_gender_output_label.setText(gender)
        self.view_employee_address_output_label.setText(address)
        self.view_employee_phone_number_output_label.setText(phone)
        self.view_employee_hire_date_output_label.setText(hire_date)
        self.view_employee_position_output_label.setText(position)
        pixmap.loadFromData(photo)
        self.view_employee_image_label.setPixmap(pixmap)

        self.show_view_employee()

    def edit_employee_button(self):
        employee_id =  self.view_employee_id_output_label.text()
        first_name = self.view_employee_first_name_output_label.text()
        middle_name = self.view_employee_middle_name_output_label.text()
        last_name = self.view_employee_last_name_output_label.text()
        birthdate = self.view_employee_birthdate_output_label.text()
        gender = self.view_employee_gender_output_label.text()
        address =self.view_employee_address_output_label.text()
        phone = self.view_employee_phone_number_output_label.text()
        hire_date = self.view_employee_hire_date_output_label.text()
        position = self.view_employee_position_output_label.text()
        photo = self.view_employee_image_label.pixmap()

        birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        hire_date = datetime.strptime(hire_date, '%Y-%m-%d')

        self.edit_employee_id_output_label.setText(employee_id)
        self.edit_employee_first_name_input.setText(first_name)
        self.edit_employee_middle_name_input.setText(middle_name)
        self.edit_employee_last_name_input.setText(last_name)
        self.edit_employee_birth_date.setDate(birthdate)
        self.edit_employee_gender_combo_box.setCurrentText(gender)
        self.edit_employee_address_input.setText(address)
        self.edit_employee_phone_number_input.setText(phone)
        self.edit_employee_hire_date.setDate(hire_date)
        self.edit_employee_position_input.setText(position)

        self.edit_employee_image_label.setPixmap(photo)


        update_table_widget("Employees", self.employee_table_widget, self.show_view_employee_temp)
        self.show_edit_employee()

#========================================================================================================================
#                                     USER ACCOUNTS MAINTENANCE
#========================================================================================================================
    def open_user_page(self):
        self.user_page = QWidget()
        self.user_page.setObjectName("user_page")
        self.stackedWidget.addWidget(self.user_page)
        # ===========================================
        #         MANAGE MEMBER PAGE LABELS
        # ===========================================
        self.manage_employee_text_label = createLabel(
            parent=self.user_page,
            name="manage_members_text",
            geometry=QRect(120, 40, 350, 40),
            text="Manage Users",
            font=font4,
            style="font: bold"
        )

        self.manage_search_text_label = createLabel(
            parent=self.user_page,
            name="manage_members_text",
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
            font=font1,
            style=""
        )

        # ===========================================
        #      MANAGE MEMBER PAGE LINE INPUTS
        # ===========================================
        self.user_manage_search_input = createLineInput(
            parent=self.user_page,
            name="search_input",
            geometry=QRect(130, 140, 580, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.user_manage_search_input.setPlaceholderText("Equipment ID / Name")

        # ===========================================
        #         MANAGE MEMBER TABLE WIDGET
        # ===========================================
        self.user_table_widget = QTableWidget(self.user_page)
        self.user_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.user_table_widget.setRowCount(0)
        self.user_table_widget.setColumnCount(5)  # Limited columns

        # Set the horizontal header labels
        self.user_table_widget.setHorizontalHeaderLabels(
            ["Employee ID", "Username", "Role", "Actions", "Void"]
        )

        self.stackedWidget.addWidget(self.user_page)
        self.user_table_widget.resizeColumnsToContents()
        self.user_table_widget.resizeRowsToContents()
        self.user_table_widget.horizontalHeader().setStretchLastSection(True)
        self.user_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.user_manage_search_input.textChanged.connect(lambda: search_entity("Users", self.user_manage_search_input, self.user_table_widget, self.show_view_user_temp))
        #         MANAGE MEMBER BUTTONS
        # ===========================================
        self.user_back_button = createButton(
            parent=self.user_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.user_add_button = createButton(
            parent=self.user_page,
            name="add_button",
            geometry=QRect(680, 40, 250, 50),
            text="Add Users",
            font=font2,
            style="background-color: #28a745; color: #FFFFFF"
        )
        self.user_back_button.clicked.connect(self.show_main_page)
        self.user_add_button.clicked.connect(self.show_create_user)
   

    def open_create_user_page(self):
        self.create_user_page = QWidget()
        self.create_user_page.setObjectName("create_user_page")
        self.stackedWidget.addWidget(self.create_user_page)
        
        # ===========================================
        #             USER ACCOUNTS LABELS
        # ===========================================
        
        self.user_registration_label = createLabel(
            parent = self.create_user_page,
            name = "user_registration",
            geometry = QRect(270, 50, 430, 40),
            text = "User Registration",
            font = font4,
            style = "font: bold"
        )

        self.user_member_name_label = createLabel(
            parent = self.create_user_page,
            name = "member_name",
            geometry = QRect(40, 150, 190, 40),
            text = "Employee Name:",
            font = font1,
            style = ""
        )

        self.user_employee_id_label = createLabel(
            parent = self.create_user_page,
            name = "membership_id",
            geometry = QRect(40, 210, 190, 40),
            text = "Employee ID",
            font = font1,
            style = ""
        )

        self.user_employee_id_output_label = createLabel(
            parent = self.create_user_page,
            name = "output",
            geometry = QRect(40, 260, 330, 40),
            text = "",
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.user_gender_label = createLabel(
            parent = self.create_user_page,
            name = "gender",
            geometry = QRect(380, 210, 130, 40),
            text = "Gender",
            font = font1,
            style = ""
        )

        self.user_gender_output_label = createLabel(
            parent = self.create_user_page,
            name = "output",
            geometry = QRect(380, 260, 260, 40),
            text = "",
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.user_phone_number_label = createLabel(
            parent = self.create_user_page,
            name = "phone_number",
            geometry = QRect(40, 320, 180, 40),
            text = "Phone Number",
            font = font1,
            style = ""
        )

        self.user_phone_number_output_label = createLabel(
            parent = self.create_user_page,
            name = "output",
            geometry = QRect(40, 360, 330, 40),
            text = "",
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.user_hire_date_label = createLabel(
            parent = self.create_user_page,
            name = "hire_date",
            geometry = QRect(380, 320, 210, 40),
            text = "Hire Date",
            font = font1,
            style = ""
        )

        self.user_hire_date_output_label = createLabel(
            parent = self.create_user_page,
            name = "output",
            geometry = QRect(380, 360, 260, 40),
            text = "",
            font = font1,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.user_image_output_label = createLabel(
            parent = self.create_user_page,
            name = "output",
            geometry = QRect(680, 140, 250, 250),
            text = "",
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.username_label = createLabel(
            parent = self.create_user_page,
            name = "username",
            geometry = QRect(40, 480, 130, 40),
            text = "Username",
            font = font2,
            style = ""
        )

        self.user_password_label = createLabel(
            parent = self.create_user_page,
            name = "password",
            geometry = QRect(470, 480, 130, 40),
            text = "Password",
            font = font2,
            style = ""
        )

        self.user_re_password_label = createLabel(
            parent = self.create_user_page,
            name = "re_password",
            geometry = QRect(470, 580, 210, 40),
            text = "Re-type Password",
            font = font2,
            style = ""
        )

        self.user_role_label = createLabel(
            parent = self.create_user_page,
            name = "role",
            geometry = QRect(40, 580, 60, 40),
            text = "Role",
            font = font2,
            style = ""
        )


        # ===========================================
        #            USER ACCOUNT INPUTS
        # ===========================================

        self.user_member_name_input = createLineInput(
            parent=self.create_user_page,
            geometry=QRect(240, 150, 410, 40),
        )

        self.user_member_name_input.setPlaceholderText("Search Employee Name")
        self.user_member_name_input.textChanged.connect(self.update_search_results)

        self.username_input = createLineInput(
            parent=self.create_user_page,
            geometry=QRect(40, 530, 410, 40),
        )

        self.password_input = createLineInput(
            parent=self.create_user_page,
            geometry=QRect(470, 530, 410, 40),
        )

        self.password_input.setEchoMode(QLineEdit.Password)

        self.re_password_input = createLineInput(
            parent=self.create_user_page,
            geometry=QRect(470, 630, 410, 40),
        )

        self.re_password_input.setEchoMode(QLineEdit.Password)

        # ===========================================
        #         USER ACCOUNT COMBO BOX
        # =========================================== 

        self.role_combo_box = createComboBox(
            parent=self.create_user_page,
            geometry=QRect(40, 630, 190, 40),
            item=["Staff", "Admin"],
        )

        # ===========================================
        #         USER ACCOUNT LIST WIDGETS
        # =========================================== 

        self.search_results = QListWidget(self.create_user_page)
        self.search_results.hide()  # Hide initially
        self.search_results.setGeometry(240, 190, 410, 400)
        self.search_results.setFont(font2)
        self.user_member_name_input.textChanged.connect(self.update_search_results)
        self.search_results.itemClicked.connect(self.handle_item_selection)
        # ===========================================
        #           USER ACCOUNT PAGE BUTTONS
        # ===========================================

        # CLEAR BUTTON
        self.user_clear_button = createButton(
            parent=self.create_user_page,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Clear",
            font=font3,
            style="background-color: #882400"
        )

        # REGISTER BUTTON
        self.user_register_button = createButton(
            parent=self.create_user_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Register",
            font=font3,
            style="background-color: #006646"
        )

        # BACK BUTTON
        self.user_back_button = createButton(
            parent=self.create_user_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.user_register_button.clicked.connect(lambda: register_user(self.assigned_input("Users"), self.create_user_page))
        self.user_back_button.clicked.connect(self.show_user_page)
        self.user_clear_button.clicked.connect(lambda: clear_inputs(self.create_user_page))

    def open_view_user_page(self):
        self.view_user_page = QWidget()
        self.view_user_page.setObjectName("view_user_page")
        self.stackedWidget.addWidget(self.view_user_page)
        
        # ===========================================
        #             USER ACCOUNTS LABELS
        # ===========================================
        
        labels_info = [
            {"geometry": QRect(270, 50, 430, 40), "text": "User Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 190, 40), "text": "Employee Name:"},
            {"geometry": QRect(40, 210, 190, 40), "text": "Employee ID"},
            {"geometry": QRect(40, 320, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 210, 130, 40), "text": "Gender"},
            {"geometry": QRect(380, 320, 210, 40), "text": "Hire Date"},
            {"geometry": QRect(40, 480, 130, 40), "text": "Username"},
            {"geometry": QRect(470, 480, 130, 40), "text": "Password"},
            {"geometry": QRect(470, 580, 210, 40), "text": "Re-type Password"},
            {"geometry": QRect(40, 580, 60, 40), "text": "Role"},
        ]
        
        for label_info in labels_info:
            createLabel(
                parent=self.view_user_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        # Output Labels
        self.view_user_employee_id_output_label = createLabel(
            parent=self.view_user_page,
            name="output",
            geometry=QRect(40, 260, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.view_user_gender_output_label = createLabel(
            parent=self.view_user_page,
            name="output",
            geometry=QRect(380, 260, 260, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.view_user_phone_number_output_label = createLabel(
            parent=self.view_user_page,
            name="output",
            geometry=QRect(40, 360, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.view_user_hire_date_output_label = createLabel(
            parent=self.view_user_page,
            name="output",
            geometry=QRect(380, 360, 260, 40),
            text="",
            font=font1,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.view_user_image_output_label = createLabel(
            parent=self.view_user_page,
            name="output",
            geometry=QRect(680, 140, 250, 250),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        update_table_widget("Users", self.user_table_widget, self.show_view_user_temp)

        # ===========================================
        #            USER ACCOUNT INPUTS
        # ===========================================

        self.view_user_member_name_input = createLabel(
            parent=self.view_user_page,
            name="member_name_input",
            geometry=QRect(240, 150, 410, 40),
            font=font2,
            text="",
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.edit_username_input = createLineInput(
            parent=self.view_user_page,
            name="view_user_name_input",
            geometry=QRect(40, 530, 410, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.edit_password_input = createLineInput(
            parent=self.view_user_page,
            name="password_input",
            geometry=QRect(470, 530, 410, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )
        self.edit_password_input.setEchoMode(QLineEdit.Password)

        self.re_edit_password_input = createLineInput(
            parent=self.view_user_page,
            name="re_password_input",
            geometry=QRect(470, 630, 410, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )
        self.re_edit_password_input.setEchoMode(QLineEdit.Password)

        # ===========================================
        #         USER ACCOUNT COMBO BOX
        # ===========================================

        self.edit_role_combo_box_output = createComboBox(
            parent=self.view_user_page,
            name="role",
            geometry=QRect(40, 630, 190, 40),
            font=font2,
            item=["Staff", "Admin"],
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        # ===========================================
        #           view_user PAGE BUTTONS
        # ===========================================

        # CHANGE BUTTON
        self.view_user_edit_button = createButton(
            parent=self.view_user_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Change",
            font=font3,
            style="background-color: #006646"
        )

        # BACK BUTTON
        self.view_user_back_button = createButton(
            parent=self.view_user_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.view_user_edit_button.clicked.connect(lambda: update_user(self.assigned_input("Update Users"), self.show_user_page))
        self.view_user_back_button.clicked.connect(self.show_user_page)


    def search_member(self, member_input):
        # Split the full name into first name and last name
        name_parts = member_input.rsplit(' ', 1)
        
        if len(name_parts) < 2:
            print("Please enter both first name and last name.")
            return
        
        first_name = name_parts[0].strip()
        last_name = name_parts[1].strip()

        # Debug: Print the first and last name
        print(f"Searching for: first_name = '{first_name}', last_name = '{last_name}'")

        # Execute the SQL query with placeholders for the first name and last name
        cursor.execute('''
            SELECT employee_id, gender, phone, hire_date, photo
            FROM Employees
            WHERE first_name = ? AND last_name = ?
        ''', (first_name, last_name))

        # Fetch the results
        results = cursor.fetchone()

        # Check if the results are found
        if results:
            self.employee_id, gender, phone_number, hire_date, photo = results
            print("Membership ID:", self.employee_id)
            print("Membership Type:", gender)
            print("Start Date:", phone_number)
            print("End Date:", hire_date)
            print("Image")

            pixmap = QPixmap()
            if photo:
                pixmap.loadFromData(photo, 'PNG')  # 'PNG' is the format of the image. Change if necessary.
                self.user_image_output_label.setPixmap(pixmap)
                self.user_image_output_label.show()
            else:
                print("No photo found.")

        else:
            print("No matching member found.")

        self.user_employee_id_output_label.setText(self.employee_id)
        self.user_gender_output_label.setText(gender)
        self.user_phone_number_output_label.setText(phone_number)
        self.user_hire_date_output_label.setText(hire_date)
    def handle_item_selection(self, item):
        selected_name = item.text()
        # Handle item selection (e.g., perform an action with the selected name)
        self.user_member_name_input.setText(selected_name)
        self.search_member(selected_name)

        self.search_results.hide()  # Hide list widget after

        self.search_results.hide()  # Hide list widget after selection
    def update_search_results(self):
        search_text = self.user_member_name_input.text()
        self.search_results.clear()
        if search_text:
            # Fetch members from database based on search text
            query = "SELECT first_name, last_name FROM Employees WHERE first_name || ' ' || last_name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            results = cursor.fetchall()
            # Add results to list widget
            for first_name, last_name in results:
                full_name = f"{first_name} {last_name}"
                self.search_results.addItem(full_name)
            self.search_results.show()  # Show list widget when there are results
        else:
            self.search_results.hide()  # Hide list widget if search text is empty
    
    def show_view_user_temp(self, row):
        # Get the employee_id from the selected row
        member_id = self.user_table_widget.item(row, 0).text()

        try:
            # Fetch the user details from the Users table
            cursor.execute(
                """
                SELECT employee_id, username, password_hash, role 
                FROM Users
                WHERE employee_id = ?
                """,
                (member_id,)
            )
            results = cursor.fetchone()

            if results:
                employee_id, username, password, role = results

                # Fetch the employee details from the Employees table
                cursor.execute(
                    '''
                    SELECT first_name || " " || last_name as full_name,
                    gender, phone, hire_date, photo
                    FROM Employees
                    WHERE employee_id = ?
                    ''',
                    (member_id,)
                )
                employee_results = cursor.fetchone()

                if employee_results:
                    name, gender, phone, hire_date, photo= employee_results
                    pixmap = QPixmap()
                    picture = pixmap.loadFromData(photo)
                    # Update the UI elements with the fetched data
                    self.view_user_member_name_input.setText(name)
                    self.view_user_employee_id_output_label.setText(employee_id)
                    self.view_user_gender_output_label.setText(gender)
                    self.view_user_phone_number_output_label.setText(phone)
                    self.view_user_hire_date_output_label.setText(hire_date)
                    self.username_input.setText(username)
                    self.password_input.setText(password)
                    self.view_user_image_output_label.setPixmap(pixmap)
                    self.edit_role_combo_box_output.setCurrentText(role)
                    self.re_password_input.setText(password)
                    self.edit_username_input.setText(self.username_input.text())
                    self.edit_password_input.setText(self.password_input.text())
                    self.re_edit_password_input.setText(self.re_password_input.text())

                    # Call the function to display the edit user page
                    self.show_edit_user()
                else:
                    print("No employee details found for the given employee_id")
            else:
                print("No user details found for the given employee_id")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

#========================================================================================================================
#                                           PRODUCTS MAINTENANCE
#========================================================================================================================
    def open_product(self):
        self.product_page = QWidget()
        self.product_page.setObjectName("product_page")

        # ===========================================
        #         MANAGE MEMBER PAGE LABELS
        # ===========================================
        self.manage_employee_text_label = createLabel(
            parent=self.product_page,
            name="manage_members_text",
            geometry=QRect(120, 40, 350, 40),
            text="Manage products",
            font=font4,
            style="font: bold"
        )

        self.manage_search_text_label = createLabel(
            parent=self.product_page,
            name="manage_members_text",
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
            font=font1,
            style=""
        )

        # ===========================================
        #      MANAGE MEMBER PAGE LINE INPUTS
        # ===========================================
        self.manage_product_search_input = createLineInput(
            parent=self.product_page,
            name="search_input",
            geometry=QRect(130, 140, 580, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.manage_product_search_input.setPlaceholderText("product ID / Name")

        # ===========================================
        #         MANAGE MEMBER TABLE WIDGET
        # ===========================================
        self.product_table_widget = QTableWidget(self.product_page)
        self.product_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.product_table_widget.setRowCount(0)
        self.product_table_widget.setColumnCount(7)# Limited columns

        # Set the horizontal header labels
        self.product_table_widget.setHorizontalHeaderLabels(
            ["Product ID", "Name", " Quantity", "Expiry Date", "Status", "Actions", "Void"]
        )
        self.stackedWidget.addWidget(self.product_page)
        self.product_table_widget.resizeColumnsToContents()
        self.product_table_widget.resizeRowsToContents()
        self.product_table_widget.horizontalHeader().setStretchLastSection(True)
        self.product_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        #         MANAGE MEMBER BUTTONS
        # ===========================================
        self.product_back_button = createButton(
            parent=self.product_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.product_add_button = createButton(
            parent=self.product_page,
            name="add_button",
            geometry=QRect(680, 40, 250, 50),
            text="Add products",
            font=font2,
            style="background-color: #28a745; color: #FFFFFF"
        )

        self.product_back_button.clicked.connect(self.show_main_page)
        self.product_add_button.clicked.connect(self.show_create_product)
        self.manage_product_search_input.textChanged.connect(lambda: search_entity("Products", self.manage_product_search_input, self.product_table_widget, self.show_view_product_temp))
        update_table_widget("Products", self.product_table_widget, self.show_view_product_temp)

    def create_product(self):
        self.create_product_page = QWidget()
        self.create_product_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.create_product_page)
       
        # ===========================================
        #            product PAGE LABELS
        # ===========================================

        self.create_product_text_label = createLabel(
            parent = self.create_product_page,
            geometry = QRect(280, 50, 430, 40),
            text = "Register Product",
            font = font4,
            style = "font: bold",
        )

        # List of label data
        labels_data = [
            {"geometry": QRect(40, 150, 160, 40), "text": "Product ID:"},
            {"geometry": QRect(40, 210, 170, 40), "text": "Product Name"},
            {"geometry": QRect(380, 210, 170, 40), "text": "Brand"},
            {"geometry": QRect(40, 310, 130, 40), "text": "SKU"},
            {"geometry": QRect(380, 310, 170, 40), "text": "Quantity"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Supplier"},
            {"geometry": QRect(380, 420, 160, 40), "text": "Price"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Purchase Date"},
            {"geometry": QRect(380, 530, 160, 40), "text": "Expiry Date"},
        ]
        
        # Create labels using a for loop
        for label_data in labels_data:
            createLabel(parent=self.create_product_page, geometry=label_data["geometry"], text=label_data["text"])


        self.create_product_id_output_label = createOutputLabel(
            parent = self.create_product_page,
            geometry = QRect(210, 150, 360, 40),
        )

        # =================================================================

        self.create_product_name_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(40, 260, 330, 40),
        )

        self.create_product_brand_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(380, 260, 330, 40),
        )

        self.create_product_sku_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(40, 360, 330, 40),
        )

        self.create_product_quantity_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(380, 360, 200, 40),
        )

        self.create_product_supplier_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(40, 470, 330, 40),
        )

        self.create_product_price_input = createLineInput(
            parent = self.create_product_page,
            geometry = QRect(380, 470, 200, 40),
        )

        # ===================================================

        self.create_product_purchase_date = createDate(
            parent = self.create_product_page,
            geometry = QRect(40, 580, 230, 40),
        )

        self.create_product_expiry_date = createDate(
            parent = self.create_product_page,
            geometry = QRect(380, 580, 230, 40),
        )

        # ====================================================
        self.create_product_back_button = createButton(
            parent = self.create_product_page,
            name = "back_button",
            geometry = QRect(40, 50, 70, 50),
            text = "Back",
            font = font3,
            style = "background-color: #004F9A"
        )

        self.create_product_clear_button = createButton(
            parent = self.create_product_page,
            name = "clear_button",
            geometry = QRect(510, 730, 170, 50),
            text = "Clear",
            font = font3,
            style = "background-color: #882400"
        )

        # REGISTER BUTTON
        self.create_product_register_button = createButton(
            parent = self.create_product_page,
            name = "register_button",
            geometry = QRect(690, 730, 250, 50),
            text = "Register Product",
            font = font3,
            style = "background-color: #006646"
        )
        self.create_product_back_button.clicked.connect(self.show_product_page)
        self.create_product_clear_button.clicked.connect(lambda: clear_inputs(self.create_product_page))
        self.create_product_register_button.clicked.connect(lambda: register_product(self.assigned_input("Product"), self.create_product_page, self.create_product_id_output_label))

    def view_product(self):

        self.view_product_page = QWidget()
        self.view_product_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.view_product_page)
        
        # ===========================================
        #            product PAGE LABELS
        # ===========================================

        self.view_product_text_label = createLabel(
            parent=self.view_product_page,
            name="product_text",
            geometry=QRect(280, 50, 430, 40),
            text="View Product Details",
            font=font4,
            style="font: bold"
        )
        # List of label data
        labels_data = [
            {"geometry": QRect(40, 150, 160, 40), "text": "Product ID:"},
            {"geometry": QRect(40, 210, 170, 40), "text": "Product Name"},
            {"geometry": QRect(380, 210, 170, 40), "text": "Brand"},
            {"geometry": QRect(40, 310, 130, 40), "text": "SKU"},
            {"geometry": QRect(380, 310, 170, 40), "text": "Quantity"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Supplier"},
            {"geometry": QRect(380, 420, 160, 40), "text": "Price"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Purchase Date"},
            {"geometry": QRect(380, 530, 160, 40), "text": "Expiry Date"},
        ]
        
        # Create labels using a for loop
        for label_data in labels_data:
            createLabel(parent=self.view_product_page,
                        geometry=label_data["geometry"],
                        text=label_data["text"],
            )

        self.view_product_id_output_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(210, 150, 360, 40)
        )

        # =================================================================

        self.view_product_name_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(40, 260, 330, 40),
        )

        self.view_product_brand_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(380, 260, 330, 40),
        )

        self.view_product_sku_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(40, 360, 330, 40),
        )

        self.view_product_quantity_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(380, 360, 200, 40),
        )

        self.view_product_supplier_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(40, 470, 330, 40),
        )

        self.view_product_price_input_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(380, 470, 200, 40),
        )

        # ===================================================

        self.view_product_purchase_date_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(40, 580, 230, 40),
        )

        self.view_product_expiry_date_label = createOutputLabel(
            parent=self.view_product_page,
            geometry=QRect(380, 580, 230, 40),
        )

        # ====================================================
        self.view_product_back_button = createButton(
            parent=self.view_product_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        # REGISTER BUTTON
        self.view_product_edit_button = createButton(
            parent=self.view_product_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Edit",
            font=font3,
            style="background-color: #006646"
        )

        self.view_product_edit_button.clicked.connect(self.edit_product_button)
        self.view_product_back_button.clicked.connect(self.show_product_page)
   
    def edit_product(self):
        self.edit_product_page = QWidget()
        self.edit_product_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.edit_product_page)
       
        # ===========================================
        #            product PAGE LABELS
        # ===========================================

        self.edit_product_text_label = createLabel(
            parent = self.edit_product_page,
            geometry = QRect(280, 50, 430, 40),
            text = "Edit Product Details",
            font = font4,
            style = "font: bold"
        )

        labels_data = [
            {"geometry": QRect(40, 150, 160, 40), "text": "Product ID:"},
            {"geometry": QRect(40, 210, 170, 40), "text": "Product Name"},
            {"geometry": QRect(380, 210, 170, 40), "text": "Brand"},
            {"geometry": QRect(40, 310, 130, 40), "text": "SKU"},
            {"geometry": QRect(380, 310, 170, 40), "text": "Quantity"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Supplier"},
            {"geometry": QRect(380, 420, 160, 40), "text": "Price"},
            {"geometry": QRect(40, 530, 180, 40), "text": "Purchase Date"},
            {"geometry": QRect(380, 530, 160, 40), "text": "Expiry Date"}
        ]
        
        # Create labels using a for loop
        for label_data in labels_data:
            createLabel(parent=self.edit_product_page,
                        geometry=label_data["geometry"],
                        text=label_data["text"],
            )


        self.edit_product_id_output_label = createOutputLabel(
            parent = self.edit_product_page,
            geometry = QRect(210, 150, 360, 40),
        )

        # =================================================================

        self.edit_product_name_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(40, 260, 330, 40),
        )

        self.edit_product_brand_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(380, 260, 330, 40),
        )

        self.edit_product_sku_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(40, 360, 330, 40),
        )

        self.edit_product_quantity_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(380, 360, 200, 40),
        )

        self.edit_product_supplier_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(40, 470, 330, 40),
        )

        self.edit_product_price_input = createLineInput(
            parent = self.edit_product_page,
            geometry = QRect(380, 470, 200, 40),
        )

        # ===================================================

        self.edit_product_purchase_date = createDate(
            parent = self.edit_product_page,
            geometry = QRect(40, 580, 230, 40),
        )

        self.edit_product_expiry_date = createDate(
            parent = self.edit_product_page,
            geometry = QRect(380, 580, 230, 40),
        )

        # ====================================================
        self.edit_product_back_button = createButton(
            parent = self.edit_product_page,
            name = "back_button",
            geometry = QRect(40, 50, 70, 50),
            text = "Back",
            font = font3,
            style = "background-color: #004F9A"
        )

        self.edit_product_cancel_button = createButton(
            parent = self.edit_product_page,
            name = "clear_button",
            geometry = QRect(510, 730, 170, 50),
            text = "Cancel",
            font = font3,
            style = "background-color: #882400"
        )

        # REGISTER BUTTON
        self.edit_product_change_button = createButton(
            parent = self.edit_product_page,
            name = "register_button",
            geometry = QRect(690, 730, 250, 50),
            text = "Confirm Changes",
            font = font3,
            style = "background-color: #006646"
        )
        self.edit_product_back_button.clicked.connect(self.show_view_product)
        self.edit_product_cancel_button.clicked.connect(self.show_view_product)
        self.edit_product_change_button.clicked.connect(self.update_product)
    # ========================================================
    
    def show_view_product_temp(self, row):
        product_id = self.product_table_widget.item(row, 0).text()

        cursor.execute(
            """
            SELECT * 
            FROM Products
            WHERE product_id = ?
            """,
            (product_id,)
        )

        results = cursor.fetchone()

        product_id, name, quantity, price, expiry_date, purchase_date, supplier, brand, status, sku, void= results


        self.view_product_id_output_label.setText(product_id)
        self.view_product_name_input_label.setText(name)
        self.view_product_quantity_input_label.setText(str(quantity))
        self.view_product_price_input_label.setText(str(price))
        self.view_product_purchase_date_label.setText(purchase_date)
        self.view_product_expiry_date_label.setText(expiry_date)
        self.view_product_supplier_input_label.setText(supplier)
        self.view_product_brand_input_label.setText(brand)
        self.view_product_sku_input_label.setText(sku)
        self.show_view_product()
  
    
    def edit_product_button(self):
        product_id = self.view_product_id_output_label.text()
        name = self.view_product_name_input_label.text()
        quantity = self.view_product_quantity_input_label.text()
        price = self.view_product_price_input_label.text()
        purchase_date = self.view_product_purchase_date_label.text()
        expiry_date = self.view_product_expiry_date_label.text()
        supplier = self.view_product_supplier_input_label.text()
        brand = self.view_product_brand_input_label.text()
        sku = self.view_product_sku_input_label.text()

        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')

        self.edit_product_id_output_label.setText(product_id)
        self.edit_product_name_input.setText(name)
        self.edit_product_quantity_input.setText(quantity)
        self.edit_product_price_input.setText(price)
        self.edit_product_purchase_date.setDate(purchase_date)
        self.edit_product_expiry_date.setDate(expiry_date)
        self.edit_product_supplier_input.setText(supplier)
        self.edit_product_brand_input.setText(brand)
        self.edit_product_sku_input.setText(sku)

        update_table_widget("Products", self.product_table_widget, self.show_view_product_temp)
        self.show_edit_product()

    def update_product(self):

        product_id = self.edit_product_id_output_label.text()
        name = self.edit_product_name_input.text()
        quantity = self.edit_product_quantity_input.text()
        price = self.edit_product_price_input.text()
        purchase_date = self.edit_product_purchase_date.date()
        expiry_date = self.edit_product_expiry_date.date()
        supplier = self.edit_product_supplier_input.text()
        brand = self.edit_product_brand_input.text()
        sku = self.edit_product_sku_input.text()

        cursor.execute(
            """
            UPDATE Products
            SET name = ?,
                quantity = ?,
                price = ?,
                purchase_date = ?,
                expiry_date = ?,
                supplier = ?,
                brand = ?,
                sku = ?
            WHERE product_id = ?
            """,
            (name, quantity, price, purchase_date.toString("yyyy-MM-dd"), expiry_date.toString("yyyy-MM-dd"),supplier, brand, sku, product_id)
        )

        connection.commit()

        self.show_product_page()


# ======================================================================================================================================================
#                                                  EQUIPMENT PAGE
# ======================================================================================================================================================

    def open_equipment_page(self):
        self.equipment_page = QWidget()
        self.equipment_page.setObjectName("equipment_page")

        # ===========================================
        #         MANAGE MEMBER PAGE LABELS
        # ===========================================
        self.manage_employee_text_label = createLabel(
            parent=self.equipment_page,
            name="manage_members_text",
            geometry=QRect(120, 40, 350, 40),
            text="Manage Equipments",
            font=font4,
            style="font: bold"
        )

        self.manage_search_text_label = createLabel(
            parent=self.equipment_page,
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
        )

        # ===========================================
        #      MANAGE MEMBER PAGE LINE INPUTS
        # ===========================================
        self.equipment_manage_input = createLineInput(
            parent=self.equipment_page,
            geometry=QRect(130, 140, 580, 40),
        )

        self.equipment_manage_input.setPlaceholderText("Equipment ID / Name")
        self.equipment_manage_input.textChanged.connect(lambda: search_entity("Equipments", self.equipment_manage_input, self.equipment_table_widget, self.show_view_equipment_temp))
        # ===========================================
        #         MANAGE MEMBER TABLE WIDGET
        # ===========================================
        self.equipment_table_widget = QTableWidget(self.equipment_page)
        self.equipment_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.equipment_table_widget.setRowCount(0)
        self.equipment_table_widget.setColumnCount(7)# Limited columns

        # Set the horizontal header labels
        self.equipment_table_widget.setHorizontalHeaderLabels(
            ["Equipment ID", "Name", "Serial Number", "Category", "Status", "Actions", "Void"]
        )

        self.stackedWidget.addWidget(self.equipment_page)
        self.equipment_table_widget.resizeColumnsToContents()
        self.equipment_table_widget.resizeRowsToContents()
        self.equipment_table_widget.horizontalHeader().setStretchLastSection(True)
        self.equipment_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        #         MANAGE MEMBER BUTTONS
        # ===========================================
        self.equipment_back_button = createButton(
            parent=self.equipment_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.equipment_add_button = createButton(
            parent=self.equipment_page,
            name="add_button",
            geometry=QRect(680, 40, 250, 50),
            text="Add Equipments",
            font=font2,
            style="background-color: #28a745; color: #FFFFFF"
        )
        self.equipment_add_button.clicked.connect(self.show_create_equipment_page)
        self.equipment_back_button.clicked.connect(self.show_main_page)

    def create_equipment(self):
        self.create_equipment_page = QWidget()
        self.create_equipment_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.create_equipment_page)
       
        # ===========================================
        #            EQUIPMENT PAGE LABELS
        # ===========================================

        self.create_equipment_text_label = createLabel(
            parent = self.create_equipment_page,
            name = "create_equipment_text",
            geometry = QRect(280, 50, 430, 40),
            text = "Register Equipment",
            font = font4,
            style = "font: bold"
        )

        labels_data = [
        {"geometry": QRect(40, 150, 165, 40), "text": "Equipment ID:"},
        {"geometry": QRect(40, 230, 210, 40), "text": "Equipment Name"},
        {"geometry": QRect(40, 350, 170, 40), "text": "Serial Number"},
        {"geometry": QRect(490, 350, 110, 40), "text": "Category"},
        {"geometry": QRect(750, 350, 110, 40), "text": "Status"},
        {"geometry": QRect(40, 470, 170, 40), "text": "Purchase Date"},
        {"geometry": QRect(260, 470, 190, 40), "text": "Warranty Expiry"},
        {"geometry": QRect(480, 470, 190, 40), "text": "Equipment Price"},
        {"geometry": QRect(40, 590, 160, 40), "text": "Manufacturer"},
        {"geometry": QRect(490, 590, 130, 40), "text": "Location"}
        ]

        for label_data in labels_data:
            createLabel(
                parent=self.create_equipment_page,
                geometry=label_data["geometry"],
                text=label_data["text"]
            )



        self.create_equipment_id_output_label = createOutputLabel(
            parent = self.create_equipment_page,
            geometry = QRect(220, 150, 300, 40),
        )

        # ===========================================
        #            EQUIPMENT PAGE INPUTS
        # ===========================================

        self.create_equipment_name_input = createLineInput(
            parent = self.create_equipment_page,
            geometry = QRect(40, 280, 430, 40),
        )

        self.create_equipment_serial_number_input = createLineInput(
            parent = self.create_equipment_page,
            geometry = QRect(40, 400, 430, 40),
        )

        self.create_equipment_price_input = createLineInput(
            parent = self.create_equipment_page,
            geometry = QRect(480, 520, 250, 40),
        )

        self.create_equipment_manufacturer_input = createLineInput(
            parent = self.create_equipment_page,
            geometry = QRect(40, 630, 430, 40),
        )

        self.create_equipment_location_input = createLineInput(
            parent = self.create_equipment_page,
            geometry = QRect(490, 630, 430, 40),
        )

        # ===========================================
        #            EQUIPMENT COMBO BOX
        # ===========================================


        self.create_equipment_category_combo_box = createComboBox(
            parent = self.create_equipment_page,
            geometry = QRect(490, 400, 250, 40),
            item = ["Cardio", "Strength", "Flexibility", "Functional Training", "Bodyweight", "Core and Stability", "Others"],
        )

        self.create_equipment_status_combo_box = createComboBox(
            parent = self.create_equipment_page,
            geometry = QRect(750, 400, 180, 40),
            item = ["Active", "Repair", "Retired"],
        )

        # ===========================================
        #               EQUIPMENT DATE
        # ===========================================

        self.create_equipment_purchase_date = createDate(
            parent = self.create_equipment_page,
            geometry = QRect(40, 520, 200, 40),
        )


        self.create_equipment_warranty_date = createDate(
            parent = self.create_equipment_page,
            geometry = QRect(260, 520, 200, 40),
        )

        # ===========================================
        #               EQUIPMENT BUTTONS
        # ===========================================

        self.create_equipment_back_button = createButton(
            parent = self.create_equipment_page,
            name = "back_button",
            geometry = QRect(40, 50, 70, 50),
            text = "Back",
            font = font3,
            style = "background-color: #004F9A"
        )

        self.create_equipment_clear_button = createButton(
            parent = self.create_equipment_page,
            name = "clear_button",
            geometry = QRect(510, 730, 170, 50),
            text = "Clear",
            font = font3,
            style = "background-color: #882400"
        )

        # REGISTER BUTTON
        self.create_equipment_register_button = createButton(
            parent = self.create_equipment_page,
            name = "register_button",
            geometry = QRect(690, 730, 250, 50),
            text = "Register Equipment",
            font = font3,
            style = "background-color: #006646"
        )
        update_table_widget("Equipments", self.equipment_table_widget, self.show_view_equipment_page)
        self.create_equipment_clear_button.clicked.connect(lambda: self.create_equipment_page)
        self.create_equipment_back_button.clicked.connect(self.show_equipment_page)
        self.create_equipment_register_button.clicked.connect(lambda: register_equipment(self.assigned_input("Equipments"), self.create_equipment_page, self.create_equipment_id_output_label))

    def edit_equipment(self):
        self.edit_equipment_page = QWidget()
        self.edit_equipment_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.edit_equipment_page)
       
        # ===========================================
        #            EQUIPMENT PAGE LABELS
        # ===========================================

        self.creaete_equipment_text_label = createLabel(
            parent=self.edit_equipment_page,
            name="view_equipment_text",
            geometry=QRect(280, 50, 430, 40),
            text="Edit Equipment",
            font=font4,
            style="font: bold"
        )
        labels_data = [
        {"geometry": QRect(40, 150, 165, 40), "text": "Equipment ID:"},
        {"geometry": QRect(40, 230, 210, 40), "text": "Equipment Name"},
        {"geometry": QRect(40, 350, 170, 40), "text": "Serial Number"},
        {"geometry": QRect(490, 350, 110, 40), "text": "Category"},
        {"geometry": QRect(750, 350, 110, 40), "text": "Status"},
        {"geometry": QRect(40, 470, 170, 40), "text": "Purchase Date"},
        {"geometry": QRect(260, 470, 190, 40), "text": "Warranty Expiry"},
        {"geometry": QRect(480, 470, 190, 40), "text": "Equipment Price"},
        {"geometry": QRect(40, 590, 160, 40), "text": "Manufacturer"},
        {"geometry": QRect(490, 590, 130, 40), "text": "Location"}
        ]
    
        for label_data in labels_data:
            createLabel(
                parent=self.edit_equipment_page,
                geometry=label_data["geometry"],
                text=label_data["text"]
            )


        self.edit_equipment_id_output_label = createOutputLabel(
            parent = self.edit_equipment_page,
            geometry = QRect(220, 150, 300, 40),
        )

        # ===========================================
        #            EQUIPMENT PAGE INPUTS
        # ===========================================

        self.edit_equipment_name_input = createLineInput(
            parent = self.edit_equipment_page,
            geometry = QRect(40, 280, 430, 40),
        )

        self.edit_equipment_serial_number_input = createLineInput(
            parent = self.edit_equipment_page,
            geometry = QRect(40, 400, 430, 40),
        )

        self.edit_equipment_price_input = createLineInput(
            parent = self.edit_equipment_page,
            geometry = QRect(480, 520, 250, 40),
        )

        self.edit_equipment_manufacturer_input = createLineInput(
            parent = self.edit_equipment_page,
            geometry = QRect(40, 630, 430, 40),
        )

        self.edit_equipment_location_input = createLineInput(
            parent = self.edit_equipment_page,
            geometry = QRect(490, 630, 430, 40),
        )

        # ===========================================
        #            EQUIPMENT COMBO BOX
        # ===========================================


        self.edit_equipment_category_combo_box = createComboBox(
            parent = self.edit_equipment_page,
            geometry = QRect(490, 400, 250, 40),
            item = ["Cardio", "Strength", "Flexibility", "Functional Training", "Bodyweight", "Core and Stability", "Others"],
        )

        self.edit_equipment_status_combo_box = createComboBox(
            parent = self.edit_equipment_page,
            geometry = QRect(750, 400, 180, 40),
            item = ["Active", "Repair", "Retired"],
        )

        # ===========================================
        #               EQUIPMENT DATE
        # ===========================================

        self.edit_equipment_purchase_date = createDate(
            parent = self.edit_equipment_page,
            geometry = QRect(40, 520, 200, 40),
        )

        self.edit_equipment_warranty_date = createDate(
            parent = self.edit_equipment_page,
            geometry = QRect(260, 520, 200, 40),
        )

        # ===========================================
        #               EQUIPMENT BUTTONS
        # ===========================================

        self.edit_equipment_back_button = createButton(
            parent = self.edit_equipment_page,
            name = "back_button",
            geometry = QRect(40, 50, 70, 50),
            text = "Back",
            font = font3,
            style = "background-color: #004F9A"
        )

        self.edit_equipment_clear_button = createButton(
            parent = self.edit_equipment_page,
            name = "clear_button",
            geometry = QRect(510, 730, 170, 50),
            text = "Cance;",
            font = font3,
            style = "background-color: #882400"
        )

        # REGISTER BUTTON
        self.edit_equipment_register_button = createButton(
            parent = self.edit_equipment_page,
            name = "register_button",
            geometry = QRect(690, 730, 250, 50),
            text = "Edit",
            font = font3,
            style = "background-color: #006646"
        )

        self.edit_equipment_back_button.clicked.connect(self.show_view_equipment_page)
        self.edit_equipment_register_button.clicked.connect(lambda: update_equipment(self.assigned_input('Update Equipments'), self.show_equipment_page))

    def view_equipment(self):
        self.view_equipment_page = QWidget()
        self.view_equipment_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.view_equipment_page)

        # ===========================================
        #            EQUIPMENT PAGE LABELS
        # ===========================================

        self.view_equipment_text_label = createLabel(
            parent=self.view_equipment_page,
            name="view_equipment_text",
            geometry=QRect(280, 50, 430, 40),
            text="View Equipment",
            font=font4,
            style="font: bold"
        )

        labels_data = [
            {"geometry": QRect(40, 150, 165, 40), "text": "Equipment ID:"},
            {"geometry": QRect(40, 230, 210, 40), "text": "Equipment Name"},
            {"geometry": QRect(40, 350, 170, 40), "text": "Serial Number"},
            {"geometry": QRect(490, 350, 110, 40), "text": "Category"},
            {"geometry": QRect(750, 350, 110, 40), "text": "Status"},
            {"geometry": QRect(40, 470, 170, 40), "text": "Purchase Date"},
            {"geometry": QRect(260, 470, 190, 40), "text": "Warranty Expiry"},
            {"geometry": QRect(480, 470, 190, 40), "text": "Equipment Price"},
            {"geometry": QRect(40, 590, 160, 40), "text": "Manufacturer"},
            {"geometry": QRect(490, 590, 130, 40), "text": "Location"}
        ]
        
        for label_data in labels_data:
            createLabel(
                parent=self.view_equipment_page,
                geometry=label_data["geometry"],
                text=label_data["text"]
            )

        self.view_equipment_id_output_label = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(220, 150, 300, 40),
        )

        # ===========================================
        #            EQUIPMENT PAGE INPUTS
        # ===========================================

        self.view_equipment_name_input = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(40, 280, 430, 40),

        )

        self.view_equipment_serial_number_input = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(40, 400, 430, 40),
        )

        self.view_equipment_price_input = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(480, 520, 250, 40),
        )

        self.view_equipment_manufacturer_input = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(40, 630, 430, 40),
        )

        self.view_equipment_location_input = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(490, 630, 430, 40),
        )

        # ===========================================
        #            EQUIPMENT COMBO BOX
        # ===========================================

        self.view_equipment_category_combo_box = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(490, 400, 250, 40),
        )

        self.view_equipment_status_combo_box = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(750, 400, 180, 40),
        )

        # ===========================================
        #               EQUIPMENT DATE
        # ===========================================

        self.view_equipment_purchase_date = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(40, 520, 200, 40),
        )

        self.view_equipment_warranty_date = createOutputLabel(
            parent=self.view_equipment_page,
            geometry=QRect(260, 520, 200, 40),
        )

        # ===========================================
        #               EQUIPMENT BUTTONS
        # ===========================================

        self.view_equipment_back_button = createButton(
            parent=self.view_equipment_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A"
        )

        self.view_equipment_edit_button = createButton(
            parent=self.view_equipment_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Edit Equipment",
            font=font3,
            style="background-color: #006646"
        )
        self.view_equipment_back_button.clicked.connect(self.show_equipment_page)
        self.view_equipment_edit_button.clicked.connect(lambda: self.edit_equipment_button())

    def edit_equipment_button(self):
        # Get the equipment details from the UI labels
        equipment_id = self.view_equipment_id_output_label.text()
        equipment_name = self.view_equipment_name_input.text()
        equipment_serial_number = self.view_equipment_serial_number_input.text()
        equipment_category = self.view_equipment_category_combo_box.text()
        equipment_purchase_date = self.view_equipment_purchase_date.text()
        equipment_warranty_expiry = self.view_equipment_warranty_date.text()
        equipment_price = self.view_equipment_price_input.text()
        equipment_manufacturer = self.view_equipment_manufacturer_input.text()
        equipment_location = self.view_equipment_location_input.text()
        equipment_status = self.view_equipment_status_combo_box.text()

        # Convert string dates to datetime objects
        equipment_purchase_date = datetime.strptime(equipment_purchase_date, '%Y-%m-%d')
        equipment_warranty_expiry = datetime.strptime(equipment_warranty_expiry, '%Y-%m-%d')

        # Set the fetched data into the corresponding input fields for editing
        self.edit_equipment_id_output_label.setText(equipment_id)
        self.edit_equipment_name_input.setText(equipment_name)
        self.edit_equipment_serial_number_input.setText(equipment_serial_number)
        self.edit_equipment_category_combo_box.setCurrentText(equipment_category)
        self.edit_equipment_purchase_date.setDate(equipment_purchase_date)
        self.edit_equipment_warranty_date.setDate(equipment_warranty_expiry)
        self.edit_equipment_price_input.setText(equipment_price)
        self.edit_equipment_manufacturer_input.setText(equipment_manufacturer)
        self.edit_equipment_location_input.setText(equipment_location)
        self.edit_equipment_status_combo_box.setCurrentText(equipment_status)

        # Update the table widget if necessary
        update_table_widget("Equipments", self.equipment_table_widget, self.show_view_equipment_page)
        # Show the edit equipment page
        self.show_edit_equipment_page()


    def show_view_equipment_temp(self, row):
        # Get the equipment_id from the table widget
        equipment_id = self.equipment_table_widget.item(row, 0).text()

        # Execute SQL query to fetch equipment details
        cursor.execute(
            """
            SELECT * 
            FROM Equipments
            WHERE equipment_id = ?
            """,
            (equipment_id,)
        )

        results = cursor.fetchone()

        # Unpack the results into corresponding variables
        (
            equipment_id, 
            equipment_name, 
            equipment_serial_number, 
            equipment_category, 
            equipment_purchase_date, 
            equipment_warranty_expiry, 
            equipment_price, 
            equipment_manufacturer, 
            equipment_location, 
            equipment_status,
            void
        ) = results

        # Update the UI elements with the fetched data
        self.view_equipment_id_output_label.setText(equipment_id)
        self.view_equipment_name_input.setText(equipment_name)
        self.view_equipment_serial_number_input.setText(equipment_serial_number)
        self.view_equipment_category_combo_box.setText(equipment_category)
        self.view_equipment_purchase_date.setText(equipment_purchase_date)
        self.view_equipment_warranty_date.setText(equipment_warranty_expiry)
        self.view_equipment_price_input.setText(str(equipment_price))
        self.view_equipment_manufacturer_input.setText(equipment_manufacturer)
        self.view_equipment_location_input.setText(equipment_location)
        self.view_equipment_status_combo_box.setText(equipment_status)

        # Show the equipment details view
        self.show_view_equipment_page()
        

    def backup_path(self):
        options = QFileDialog.Options()
        path = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        print(path)

        time = datetime.now().strftime("%Y-%m-%d _ %H-%M")
        source_path = "Software-Engineer-master/database.db"
        backup_path = f"{path}/backup_{time}.db"
        self.backup(source_path, backup_path)

    def restore_path(self):


        options = QFileDialog.Options()
        restore_path, _ = QFileDialog.getOpenFileName(self, "Select .db File", "", "SQLite Files (*.db)", options=options)
        print(restore_path)
        
        new_path = "Software-Engineer-master/database.db"
        self.restore(restore_path, new_path)

    def backup(self, source_db, backup_db):
        # Connect to the source database
        src_conn = sqlite3.connect(source_db)
        # Connect to the backup database (it will be created if it doesn't exist)
        backup_conn = sqlite3.connect(backup_db)

        with backup_conn:
            src_conn.backup(backup_conn, pages=1, progress=None)

        QMessageBox.information(None, "Success", "Backup Stored")

        # Close the connections
        src_conn.close()
        backup_conn.close()
    
    def restore(self, restore_db, new_db):
        try:
            # Ensure the directory for the new database file exists
            new_db_dir = os.path.dirname(new_db)
            if not os.path.exists(new_db_dir):
                os.makedirs(new_db_dir)

            # Make a copy of the backup file to the new database file
            shutil.copyfile(restore_db, new_db)
            QMessageBox.information(None, "Success", "Database Restored")
        except Exception as e:
            QMessageBox.critical(None, "Error", "Database Restoration Failed")
    

    # ======================================================================================================================

    def open_payment_page(self):
        self.main_payment_page = QWidget()
        self.main_payment_page.setObjectName("main_payment_page")

        # Labels and input for main payment page
        self.payment_text_label = createLabel(
            parent=self.main_payment_page,
            name="payment_members_text",
            geometry=QRect(120, 40, 350, 40),
            text="Manage Payments",
            font=font4,
            style="font: bold"
        )

        self.payment_search_text_label = createLabel(
            parent=self.main_payment_page,
            name="payment_members_text",
            geometry=QRect(30, 140, 90, 40),
            text="Search:",
            font=font1,
            style=""
        )

        self.payment_search_input = createLineInput(
            parent=self.main_payment_page,
            geometry=QRect(130, 140, 580, 40),
        )
        
        self.payment_search_input.setPlaceholderText("Payment ID / Name")

        self.payment_table_widget = QTableWidget(self.main_payment_page)
        self.payment_table_widget.setGeometry(QRect(10, 200, 930, 590))
        self.payment_table_widget.setRowCount(0)
        self.payment_table_widget.setColumnCount(5)

        self.payment_table_widget.setHorizontalHeaderLabels(
            ["Payment ID", "Member ID", "File Path", "Date Recorded", "Actions"]
        )
        self.payment_search_input.textChanged.connect(lambda: search_entity("Payments", self.payment_search_input, self.payment_table_widget, self.show_view_payment_temp))
        
        self.stackedWidget.addWidget(self.main_payment_page)
        self.payment_table_widget.resizeColumnsToContents()
        self.payment_table_widget.resizeRowsToContents()
        self.payment_table_widget.horizontalHeader().setStretchLastSection(True)
        self.payment_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.payment_back_button = createButton(
            parent=self.main_payment_page,
            name="back_button",
            geometry=QRect(20, 40, 70, 50),
            text="Back",
            font=font2,
            style=""
        )

        self.payment_back_button.clicked.connect(self.show_main_page)
        self.update_payment_table_widget()

    def view_payment_page(self):
        self.view_payment_page = QWidget()
        self.view_payment_page.setObjectName("view_payment_page")

        labels_data = [
            {"geometry": QRect(360, 60, 400, 40), "text": "View Payment Details"},
            {"geometry": QRect(60, 160, 230, 40), "text": "Reference Number"},
            {"geometry": QRect(60, 270, 230, 40), "text": "Member ID Holder"},
            {"geometry": QRect(510, 270, 230, 40), "text": "Date Recorded"}
        ]

        for label_data in labels_data:
            createLabel(
                parent=self.view_payment_page,
                geometry=label_data["geometry"],
                text=label_data["text"]
            )

        self.view_payment_ref_number_input = createOutputLabel(
            parent=self.view_payment_page,
            geometry=QRect(60, 210, 330, 40),
        )

        self.view_payment_member_id_input = createOutputLabel(
            parent=self.view_payment_page,
            geometry=QRect(60, 330, 420, 40),
        )

        self.view_payment_date_input = createOutputLabel(
            parent=self.view_payment_page,
            geometry=QRect(510, 330, 420, 40),
        )

        self.view_payment_back_button = createButton(
            parent=self.view_payment_page,
            name="view_payment_back_button",
            geometry=QRect(50, 60, 70, 50),
            text="Back",
            font=font2,
            style="background-color: #000000; color: #FFFFFF"
        )

        self.view_payment_edit_button = createButton(
            parent=self.view_payment_page,
            name="view_payment_edit_button",
            geometry=QRect(710, 730, 220, 40),
            text="Edit",
            font=font2,
            style="background-color: #007bff; color: #FFFFFF"
        )

        self.view_payment_contract_button = createButton(
            parent=self.view_payment_page,
            name="view_payment_edit_button",
            geometry=QRect(60, 420, 220, 40),
            text="View Contract",
            font=font2,
            style="background-color: #007bff; color: #FFFFFF"
        )
        self.view_payment_back_button.clicked.connect(self.show_payment_page)
        self.view_payment_edit_button.clicked.connect(self.edit_payment_button)
        self.stackedWidget.addWidget(self.view_payment_page)
    
        update_table_widget("Payments", self.payment_table_widget, self.show_view_payment_temp)

    def edit_payment_page(self):
        self.edit_payment_page_nigg = QWidget()
        self.edit_payment_page_nigg.setObjectName("edit_payment_page")
        self.stackedWidget.addWidget(self.edit_payment_page_nigg)

        labels_data = [
        {"geometry": QRect(360, 60, 400, 40), "text": "Edit Payment Details"},
        {"geometry": QRect(60, 160, 230, 40), "text": "Reference Number"},
        {"geometry": QRect(60, 270, 230, 40), "text": "Member ID Holder"},
        {"geometry": QRect(510, 270, 230, 40), "text": "Date Recorded"}
        ]

        for label_data in labels_data:
            createLabel(
                parent=self.edit_payment_page_nigg,
                geometry=label_data["geometry"],
                text=label_data["text"]
            )

        self.edit_payment_ref_number_input = createOutputLabel(
            parent=self.edit_payment_page_nigg,
            geometry=QRect(60, 210, 330, 40),
        )

        self.edit_payment_member_id_input = createOutputLabel(
            parent=self.edit_payment_page_nigg,
            geometry=QRect(60, 330, 420, 40),
        )

        self.edit_payment_date_input = createDate(
            parent=self.edit_payment_page_nigg,
            geometry=QRect(510, 330, 420, 40),
        )

        self.edit_payment_back_button = createButton(
            parent=self.edit_payment_page_nigg,
            name="edit_payment_back_button",
            geometry=QRect(50, 60, 70, 50),
            text="Back",
            font=font2,
            style="background-color: #000000; color: #FFFFFF"
        )

        self.edit_payment_confirm_button = createButton(
            parent=self.edit_payment_page_nigg,
            name="edit_payment_edit_button",
            geometry=QRect(710, 730, 220, 40),
            text="Confirm",
            font=font2,
            style="background-color: #007bff; color: #FFFFFF"
        )

        self.edit_payment_contract_button = createButton(
            parent=self.edit_payment_page_nigg,
            name="edit_payment_edit_button",
            geometry=QRect(60, 420, 220, 40),
            text="Edit Contract",
            font=font2,
            style="background-color: #007bff; color: #FFFFFF"
        )

        self.softcopy = createLabel(
            parent = self.edit_payment_page_nigg,
            name = "record_softcopy",
            geometry = QRect(50, 373, 361, 151),
            text = "",
            font = font6,
            style = "background: white; border: 1px solid black; font-style: italic; color: #A9A9AC"
        )
        self.copy = None

        self.insert_button = createButton(
            parent = self.edit_payment_page_nigg,
            name = "record_insert_button",
            geometry = QRect(50, 520, 361, 61),
            text = "Search",
            font = font5,
            style = "background: red; color: white"
        )
        
        self.edit_payment_confirm_button.clicked.connect(lambda: update_payment(self.assigned_input("Update Contract"), self.show_view_payment_page))
        self.insert_button.clicked.connect(self.insert)

    def insert(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_name:
            self.copy = file_name 
            print(self.copy)
            self.softcopy.setText("File Inserted")
            self.softcopy.setAlignment(Qt.AlignCenter)
        else: 
            self.softcopy.setText("Missing File")
            self.softcopy.setAlignment(Qt.AlignCenter)


    def update_payment_table_widget(self):
        data = fetch_entity("Payments")
        self.payment_table_widget.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                self.payment_table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        for row in range(self.payment_table_widget.rowCount()):
            view_button = QPushButton("View")
            view_button.clicked.connect(partial(self.show_view_payment_temp, row))
            self.payment_table_widget.setCellWidget(row, 4, view_button)

    def show_view_payment_temp(self, row):
        payment_id = self.payment_table_widget.item(row, 0).text()

        cursor.execute(
            """
            SELECT reference_number, member_id, softcopy_contract, date_recorded
            FROM Contracts
            WHERE reference_number = ?
            """,
            (payment_id,)  # Note the comma to make it a single-element tuple
        )

        results = cursor.fetchone()
        if results:
            ref_number, member_id, softcopy, date = results

            self.view_payment_ref_number_input.setText(str(ref_number))
            self.view_payment_member_id_input.setText(str(member_id))
            self.view_payment_date_input.setText(date)
            self.view_payment_contract_button.clicked.connect(lambda: self.run_script(softcopy))

            self.show_view_payment_page()
        else:
            print(f"No results found for payment ID {payment_id}")
    
    def edit_payment_button(self):
        ref_number = self.view_payment_ref_number_input.text()
        member_id = self.view_payment_member_id_input.text()
        date = self.view_payment_date_input.text()

        format_date = datetime.strptime(date, '%Y-%m-%d')

        self.edit_payment_date_input.setDate(format_date)
        self.edit_payment_ref_number_input.setText(ref_number)
        self.edit_payment_member_id_input.setText(member_id)
        print("hello")
        self.show_edit_payment_page()
  
    def run_script(self, file_path):
        if os.path.isfile(file_path):
            os.startfile(file_path)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Maintenance()
    window.show()
    sys.exit(app.exec_())