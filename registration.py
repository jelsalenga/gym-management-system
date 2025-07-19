from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from assets import *
import sqlite3
import re
from datetime import datetime
import uuid

# ==============================================================================
# ==============================================================================
#                           REGISTRATION     CLASS
# ==============================================================================
# ==============================================================================

class Registration(QWidget):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)
        self.setObjectName("Form")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #FFFFFF")
        self.open_registration_interface()

    def open_registration_interface(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")

        self.open_main_page()               # MAIN PAGE
        self.open_create_member_page()      # MEMBER PAGE
        self.open_create_attendance_page()  # ATTENDANCE PAGE

        self.verticalLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def show_member_page(self):
        generate_id("Members", self.member_id_output_label)
        clear_inputs(self.member_page)
        self.stackedWidget.setCurrentIndex(1)
        
    def show_attendance_page(self):
        clear_inputs(self.attendance_page)
        self.stackedWidget.setCurrentIndex(2)


# =============================================================
#                     STAFF MAIN PAGE
# ============================================================= 
    def open_main_page(self):
        self.main_page = QWidget()
        self.main_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.main_page)
        # ===========================================
        #             MAIN PAGE BUTTONS
        # ===========================================
        self.switch_member_page_button = createButton(
            parent = self.main_page,
            name = "member_page_button",
            geometry = QRect(300, 250, 350, 100),
            text = "Register Member",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_attendance_page_button = createButton(
            parent = self.main_page,
            name = "attendance_page_button",
            geometry = QRect(300, 440, 350, 100),
            text = "Register Attendance",
            font = font3,
            style = "background-color: #004F9A; color: #FFFFFF"
        )

        self.switch_member_page_button.clicked.connect(self.show_member_page)
        self.switch_attendance_page_button.clicked.connect(self.show_attendance_page)

# =============================================================
#                     CREATE MEMBER PAGE
# =============================================================    
    def open_create_member_page(self):
        self.member_page = QWidget()
        self.member_page.setObjectName("member_page")
    
        # ===========================================
        #             MEMBER PAGE LABELS
        # ===========================================

        # Labels configuration
        labels = [
            {"name": "member_id_label", "geometry": QRect(40, 150, 191, 40), "text": "Membership ID:"},
            {"name": "member_first_name_label", "geometry": QRect(40, 210, 130, 40), "text": "First Name"},
            {"name": "member_middle_name_label", "geometry": QRect(380, 210, 160, 40), "text": "Middle Name"},
            {"name": "member_last_name_label", "geometry": QRect(40, 310, 130, 40), "text": "Last Name"},
            {"name": "member_gender_label", "geometry": QRect(380, 310, 130, 40), "text": "Gender"},
            {"name": "member_address_label", "geometry": QRect(40, 420, 130, 40), "text": "Address"},
            {"name": "member_birthdate_label", "geometry": QRect(380, 420, 130, 40), "text": "Birthdate"},
            {"name": "member_phone_number_label", "geometry": QRect(40, 530, 180, 40), "text": "Phone Number"},
            {"name": "member_membership_type_label", "geometry": QRect(380, 530, 210, 40), "text": "Membership Type"},
            {"name": "member_start_date_label", "geometry": QRect(40, 630, 180, 40), "text": "Start Date"},
            {"name": "member_end_date_label", "geometry": QRect(280, 630, 180, 40), "text": "End Date"},
        ]

        # Create labels using a loop
        for label in labels:
            setattr(self, label["name"], createLabel(
                parent= self.member_page,
                geometry=label["geometry"],
                text=label["text"],
            ))

        self.member_registration_text_label = createLabel(
            parent = self.member_page,
            geometry = QRect(310, 50, 380, 40), 
            text = "Member Registration", 
            font = font4, 
            style = "font: bold"
        )
        
        # MEMBER ID OUTPUT LABEL
        self.member_id_output_label = createOutputLabel(
            parent=self.member_page,
            geometry=QRect(240, 150, 410, 40),
            name="unique_id_member"
        )

        # IMAGE LABEL 
        self.member_image_label = createOutputLabel(
            parent=self.member_page,
            geometry=QRect(680, 140, 250, 250),
        )
        
        # SIGNATURE LABEL
        self.member_signature_label = createOutputLabel(
            parent=self.member_page,
            geometry=QRect(750, 460, 180, 90),
        )
        
        # ===========================================
        #             MEMBER PAGE INPUTS
        # ===========================================

        # Input fields configuration
        inputs = [
            {"name": "member_first_name_input", "geometry": QRect(40, 260, 330, 40)},
            {"name": "member_middle_name_input", "geometry": QRect(380, 260, 280, 40)},
            {"name": "member_last_name_input", "geometry": QRect(40, 360, 330, 40)},
            {"name": "member_address_input", "geometry": QRect(40, 470, 330, 40)},
            {"name": "member_phone_number_input", "geometry": QRect(40, 570, 330, 40)},
        ]

        # Create input fields using a loop
        for input_field in inputs:
            setattr(self, input_field["name"], createLineInput(
                parent=self.member_page,
                geometry=input_field["geometry"],
            ))

        # ===========================================
        #            MEMBER PAGE COMBO BOX
        # ===========================================

        # Create combo boxes
        self.member_gender_combo_box = createComboBox(
            parent=self.member_page,
            name="gender_combo_box",
            geometry=QRect(380, 360, 140, 40),
            font=font4,
            item=['Male', 'Female'],
            style="background-color: #F9F7FF; border: 1px solid black"
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

        # Create date fields
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

        # Create buttons
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

        # Connect signals and slots
        self.member_insert_image_button.clicked.connect(lambda: insert_image(self.member_image_label))
        self.member_insert_signature_button.clicked.connect(lambda: insert_image(self.member_signature_label))
        self.member_register_button.clicked.connect(lambda: register_member(self.assigned_input("Members"), self.member_page, self.member_id_output_label))
        self.member_clear_button.clicked.connect(lambda: clear_inputs(self.member_page))
        self.member_back_button.clicked.connect(self.show_main_page)
        
        self.stackedWidget.addWidget(self.member_page)


# =============================================================
#                   CREATE ATTENDANCE PAGE
# ============================================================= 
    def open_create_attendance_page(self):
        self.attendance_page = QWidget()
        self.attendance_page.setObjectName("attendance_page")
        self.stackedWidget.addWidget(self.attendance_page)

        # ===========================================
        #             ATTENDANCE  LABELS
        # ===========================================

        labels_info = [
            {"geometry": QRect(270, 50, 430, 40), "text": "Attendance Registration", "font": font4, "style": "font: bold"},
            {"geometry": QRect(40, 150, 190, 40), "text": "Member Name:"},
            {"geometry": QRect(40, 210, 190, 40), "text": "Membership ID"},
            {"geometry": QRect(40, 320, 180, 40), "text": "Phone Number"},
            {"geometry": QRect(380, 210, 130, 40), "text": "Gender"},
            {"geometry": QRect(380, 320, 210, 40), "text": "Membership Type"},
            {"geometry": QRect(40, 420, 130, 40), "text": "Start Date"},
            {"geometry": QRect(270, 420, 180, 40), "text": "End Date"},
            {"geometry": QRect(490, 420, 130, 40), "text": "Time"},
            {"geometry": QRect(690, 420, 230, 40), "text": "Type of Attendance"},
            {"geometry": QRect(40, 520, 230, 40), "text": "Date of Attendance"},
        ]

        for label_info in labels_info:
            createLabel(
                parent=self.attendance_page,
                geometry=label_info["geometry"],
                text=label_info["text"],
                font=label_info.get("font", font1),
                style=label_info.get("style", "")
            )

        self.attendance_membership_id_output_label = createLabel(
            parent=self.attendance_page,
            name="membership_id_output",
            geometry=QRect(40, 260, 330, 40),
            
        )

        self.attendance_gender_output_label = createLabel(
            parent=self.attendance_page,
            name="gender_output",
            geometry=QRect(380, 260, 140, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.attendance_phone_number_output_label = createLabel(
            parent=self.attendance_page,
            name="phone_number_output",
            geometry=QRect(40, 360, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.attendance_membership_type_output_label = createLabel(
            parent=self.attendance_page,
            name="membership_type_output",
            geometry=QRect(380, 360, 260, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.attendance_start_date_output_label = createLabel(
            parent=self.attendance_page,
            name="start_date_output",
            geometry=QRect(40, 470, 200, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.attendance_end_date_output_label = createLabel(
            parent=self.attendance_page,
            name="end_date_output",
            geometry=QRect(270, 470, 200, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.attendance_image_output_label = createLabel(
            parent=self.attendance_page,
            name="image_output",
            geometry=QRect(680, 140, 250, 250),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )


        # ===========================================
        #            ATTENDANCE  INPUTS
        # ===========================================

        self.attendance_member_name_input = createLineInput(
            parent=self.attendance_page,
            name="member_name_input",
            geometry=QRect(240, 150, 410, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )
        self.attendance_member_name_input.setPlaceholderText("Search Member Name")
        self.attendance_member_name_input.textChanged.connect(self.update_search_results)

        self.search_results = QListWidget(self)
        self.search_results.hide()  # Hide initially
        self.search_results.setGeometry(240, 190, 410, 400)
        self.search_results.setFont(font2)
        # Connect signals
        self.search_results.itemClicked.connect(self.handle_item_selection)

        # ===========================================
        #            ATTENDANCE  TIME
        # ===========================================
        self.attendance_time_input = createTime(
            parent=self.attendance_page,
            name="time_input",
            geometry=QRect(490, 470, 190, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        # ===========================================
        #           ATTENDANCE COMBO BOX
        # ===========================================

        self.attendance_type_combo_box = createComboBox(
            parent=self.attendance_page,
            name='type_of_attendance_input',
            geometry=QRect(690, 470, 140, 40),
            font=font2,
            item=['Entry', 'Exit'],
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        # ===========================================
        #               ATTENDANCE DATES
        # ===========================================

        self.attendance_date_input = createDate(
            parent=self.attendance_page,
            name="date",
            geometry=QRect(40, 560, 190, 40),
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        # ===========================================
        #           ATTENDANCE PAGE BUTTONS
        # ===========================================

        # CLEAR BUTTON
        self.attendance_clear_button = createButton(
            parent=self.attendance_page,
            name="clear_button",
            geometry=QRect(510, 730, 170, 50),
            text="Clear",
            font=font3,
            style="background-color: #882400; color: #FFFFFF"
        )

        # REGISTER BUTTON
        self.attendance_register_button = createButton(
            parent=self.attendance_page,
            name="register_button",
            geometry=QRect(690, 730, 250, 50),
            text="Register",
            font=font3,
            style="background-color: #006646; color: #FFFFFF"
        )

        # BACK BUTTON
        self.attendance_back_button = createButton(
            parent=self.attendance_page,
            name="back_button",
            geometry=QRect(40, 50, 70, 50),
            text="Back",
            font=font3,
            style="background-color: #004F9A; color: #FFFFFF"
        )

        self.attendance_register_button.clicked.connect(lambda: register_attendance(self.assigned_input("Attendance"), self.attendance_page))
        self.attendance_back_button.clicked.connect(self.show_main_page)
        self.attendance_clear_button.clicked.connect(lambda: clear_inputs(self.attendance_page))

    def assigned_input(self, input):
        if input == "Attendance":
            INPUTS = {
                "date": self.attendance_date_input.date(),
                "member_id": self.attendance_membership_id_output_label.text(),
                "time": self.attendance_time_input.time(),
                "attendance": self.attendance_type_combo_box.currentText(),
            }
        elif input == "Members":
            image = pixmap_to_bytes(self.member_image_label.pixmap())
            signature = pixmap_to_bytes(self.member_signature_label.pixmap())

            INPUTS = {
                "member_id": self.member_id_output_label.text(),
                "first_name": self.member_first_name_input.text(),
                "middle_name":self.member_middle_name_input.text(),
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
        return INPUTS
    

# =============================================================
#                      BACK-END FUNCTIONS
# ============================================================= 
    def update_end_date(self):
        membership_type = self.member_membership_type_combo_box.currentText()
        if membership_type == "Lifetime":
            self.member_end_date.setDate(QDate(9999, 12, 31))  # Set to a far future date
            self.member_end_date.setDisabled(True)  # Optionally disable the end date field
        else:
            self.member_end_date.setDisabled(False)
            self.member_end_date.setDate(QDate.currentDate())  # Reset to the current date


    def update_search_results(self):
        search_text = self.attendance_member_name_input.text()
        self.search_results.clear()

        if search_text:
            # Fetch members from database based on search text
            query = "SELECT first_name, last_name FROM Members WHERE first_name || ' ' || last_name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            results = cursor.fetchall()
            # Add results to list widget
            for first_name, last_name in results:
                full_name = f"{first_name} {last_name}"
                self.search_results.addItem(full_name)
            self.search_results.show()  # Show list widget when there are results
        else:
            self.search_results.hide()  # Hide list widget if search text is empty


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
            SELECT member_id, gender, phone_number, membership_type, membership_start_date, membership_end_date, photo
            FROM Members
            WHERE first_name = ? AND last_name = ?
        ''', (first_name, last_name))

        # Fetch the results
        results = cursor.fetchone()

        # Check if the results are found
        if results:
            membership_id, gender, phone_number, membership_type, start_date, end_date, photo= results

            pixmap = QPixmap()
            if photo:
                pixmap.loadFromData(photo, 'PNG')  # 'PNG' is the format of the image. Change if necessary.
                self.attendance_image_output_label.setPixmap(pixmap)
                self.attendance_image_output_label.show()
            else:
                print("No photo found.")

        else:
            print("No matching member found.")

        self.attendance_membership_id_output_label.setText(str(membership_id))
        self.attendance_gender_output_label.setText(gender)
        self.attendance_phone_number_output_label.setText(phone_number)
        self.attendance_membership_type_output_label.setText(membership_type)
        self.attendance_start_date_output_label.setText(start_date)
        self.attendance_end_date_output_label.setText(end_date)


    def handle_item_selection(self, item):
        selected_name = item.text()
        # Handle item selection (e.g., perform an action with the selected name)
        self.attendance_member_name_input.setText(selected_name)
        self.search_member(selected_name)

        self.search_results.hide()  # Hide list widget after selection

    def generate_member_id(self):
        current_time = datetime.now()
        formatted_time = current_time.strftime('%m%d%y%H%M%S')
        prefix = '10'

        generated_id = f"{prefix}{formatted_time}"
        self.member_id_output_label.setText(generated_id)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec_())
