from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDateEdit, \
    QDialog, QDialogButtonBox
from PyQt5.QtCore import QDate
import sqlite3
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_RIGHT
import sys
import os
from datetime import datetime
from assets import *
from session_manager import *

# Define the output directory for PDF reports
OUTPUT_DIR = 'reports'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

ADDRESS = "49A, Main Building SM City, North Avenue corner, Bagong Pag-asa, Quezon City"
CONTACT = "(02) 8929 5424"


# Date selection dialog
class DateSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Date")
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.date_edit)
        layout.addWidget(buttons)

    def getDate(self):
        return self.date_edit.date().toString("yyyy-MM-dd")


class Reports(QWidget):
    def __init__(self, parent=None):
        super(Reports, self).__init__(parent)
        self.setObjectName("Form")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #FFFFFF")
        self.setWindowTitle('Slimmer World Reports')
        self.open_reports_maintenance()

    def open_reports_maintenance(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(20)  # Adjust spacing between buttons
        self.verticalLayout.setContentsMargins(300, 20, 300, 20)  # Adjust margins

        self.membership_btn = QPushButton("Membership Report")
        self.membership_btn.setStyleSheet("background-color: #004F9A; color: #FFFFFF; height: 70px;")  # Adjust button height
        self.membership_btn.setFont(font3)
        self.membership_btn.clicked.connect(self.generate_membership_report)

        self.scheduling_btn = QPushButton("Schedule Report")
        self.scheduling_btn.setStyleSheet("background-color: #004F9A; color: #FFFFFF; height: 70px;")
        self.scheduling_btn.setFont(font3)
        self.scheduling_btn.clicked.connect(self.generate_scheduling_report)

        self.equipment_btn = QPushButton("Equipment Report")
        self.equipment_btn.setStyleSheet("background-color: #004F9A; color: #FFFFFF; height: 70px;")
        self.equipment_btn.setFont(font3)
        self.equipment_btn.clicked.connect(self.generate_equipment_report)

        self.stock_btn = QPushButton("Stock Report")
        self.stock_btn.setStyleSheet("background-color: #004F9A; color: #FFFFFF; height: 70px;")
        self.stock_btn.setFont(font3)
        self.stock_btn.clicked.connect(self.generate_stock_report)

        self.attendance_btn = QPushButton("Attendance Report")
        self.attendance_btn.setStyleSheet("background-color: #004F9A; color: #FFFFFF; height: 70px;")
        self.attendance_btn.setFont(font3)
        self.attendance_btn.clicked.connect(self.generate_attendance_report)

        # Add buttons to layout
        self.verticalLayout.addWidget(self.membership_btn)
        self.verticalLayout.addWidget(self.scheduling_btn)
        self.verticalLayout.addWidget(self.equipment_btn)
        self.verticalLayout.addWidget(self.stock_btn)
        self.verticalLayout.addWidget(self.attendance_btn)
        
    def generate_membership_report(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        query = """
        SELECT member_id, first_name, middle_name, last_name, address, gender, birthdate, phone_number, 
               membership_type, membership_start_date, membership_end_date
        FROM Members
        ORDER BY
            CASE
                WHEN membership_type = 'Lifetime' THEN 1
                WHEN membership_type = 'Standard' THEN 2
                ELSE 3
            END,
            first_name
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        full_name = session_manager.get_full_name()

        pdf_file = os.path.join(OUTPUT_DIR, f'Membership_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')

        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
        elements = []

        styles = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

        # Center the title
        title_style = styles['Title']
        title_style.alignment = TA_CENTER
        title = Paragraph("<font name='TimesNewRoman' color='blue' size=18>Slimmer World</font>", styles['Title'])

        # Center the address
        address_style = styles['Normal']
        address_style.alignment = TA_CENTER
        address = Paragraph(f"<font name='TimesNewRoman' size=12>{ADDRESS}</font>", styles['Normal'])

        # Center the contact
        contact_style = styles['Normal']
        contact_style.alignment = TA_CENTER
        contact = Paragraph(f"<font name='TimesNewRoman' size=12>{CONTACT}</font>", styles['Normal'])
        elements.append(title)
        elements.append(address)
        elements.append(contact)

        # Add spacer to title
        elements.append(Spacer(1, 12))
        report_title = Paragraph("<font name='TimesNewRoman' size=14>Membership Report</font>", styles['Title'])
        elements.append(report_title)

        # Add space
        elements.append(Spacer(1, 12))

        # Table Header
        table_data = [
            ["Member ID", "First Name", "Middle Name", "Last Name", "Address", "Gender", "Birthdate", "Phone Number",
             "Membership Type", "Start Date", "End Date"]
        ]

        # Adding data to table
        for row in rows:
            table_data.append(list(row))

        # Specifying smaller column widths to fit the table
        col_widths = [70, 60, 60, 60, 190, 40, 60, 70, 80, 70, 70]

        # Creating table with smaller font size and styles
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
            ('GRID', (0, 0), (-1, -1), 1, 'black'),
            ('WORDWRAP', (0, 0), (-1, -1), 'ON'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        right_aligned_style = ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT)

        timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
        generated_time = Paragraph(f"Generated on: {timestamp} by {full_name}", right_aligned_style)
        elements.append(Spacer(1, 1))
        elements.append(generated_time)

        doc.build(elements)

        QMessageBox.information(None, 'Success', f'Equipment Report generated successfully!\nSaved at: {pdf_file}')

    # Function to generate Equipment Report
    def generate_equipment_report(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = """
        SELECT equipment_id, equipment_name, equipment_serial_number, equipment_category, 
               equipment_purchase_date, equipment_warranty_expiry, equipment_price, equipment_manufacturer, 
               equipment_location, equipment_status
        FROM Equipments
        ORDER BY equipment_name
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        full_name = session_manager.get_full_name()


        pdf_file = os.path.join(OUTPUT_DIR, f'Equipment_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')

        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
        elements = []

        styles = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

        # Center the title
        title_style = styles['Title']
        title_style.alignment = TA_CENTER
        title = Paragraph("<font name='TimesNewRoman' color='blue' size=18>Slimmer World</font>", styles['Title'])

        # Center the address
        address_style = styles['Normal']
        address_style.alignment = TA_CENTER
        address = Paragraph(f"<font name='TimesNewRoman' size=12>{ADDRESS}</font>", styles['Normal'])

        # Center the contact
        contact_style = styles['Normal']
        contact_style.alignment = TA_CENTER
        contact = Paragraph(f"<font name='TimesNewRoman' size=12>{CONTACT}</font>", styles['Normal'])

        elements.append(title)
        elements.append(address)
        elements.append(contact)

        # Add spacer to title
        elements.append(Spacer(1, 12))
        report_title = Paragraph("<font name='TimesNewRoman' size=14>Equipment Report</font>", styles['Title'])
        elements.append(report_title)

        # Add space
        elements.append(Spacer(1, 12))

        # Table Header
        table_data = [
            ["Equipment ID", "Name", "Serial Number", "Category", "Purchase Date", "Warranty Expiry",
             "Price", "Manufacturer", "Location", "Status"]
        ]

        # Adding data to table
        for row in rows:
            table_data.append(list(row))

        # Specifying smaller column widths to fit the table
        col_widths = [80, 100, 100, 80, 80, 80, 60, 100, 80, 60]

        # Creating table with smaller font size and styles
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
            ('GRID', (0, 0), (-1, -1), 1, 'black'),
            ('WORDWRAP', (0, 0), (-1, -1), 'ON'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        right_aligned_style = ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT)

        timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
        generated_time = Paragraph(f"Generated on: {timestamp} by {full_name}", right_aligned_style)
        elements.append(Spacer(1, 1))
        elements.append(generated_time)

        doc.build(elements)

        QMessageBox.information(None, 'Success', f'Equipment Report generated successfully!\nSaved at: {pdf_file}')

    # Function to generate Scheduling Report
    def generate_scheduling_report(self):
        dialog = DateSelectionDialog()
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.getDate()

            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                query = """
                SELECT schedule_id, member_id, employee_id, appointment_type, appointment_name, appointment_date,
                appointment_start_time, appointment_end_time, status 
                FROM Schedule WHERE appointment_date = ?
                """

                cursor.execute(query, (selected_date,))
                rows = cursor.fetchall()
                conn.close()

                full_name = session_manager.get_full_name()

                pdf_file = os.path.join(OUTPUT_DIR, f'Scheduling_Report_{selected_date}.pdf')

                doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
                elements = []

                styles = getSampleStyleSheet()
                pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

                # Center the title
                title_style = styles['Title']
                title_style.alignment = TA_CENTER
                title = Paragraph("<font name='TimesNewRoman' color='blue' size=18>Slimmer World</font>",
                                  styles['Title'])

                # Center the address
                address_style = styles['Normal']
                address_style.alignment = TA_CENTER
                address = Paragraph(f"<font name='TimesNewRoman' size=12>{ADDRESS}</font>", styles['Normal'])

                # Center the contact
                contact_style = styles['Normal']
                contact_style.alignment = TA_CENTER
                contact = Paragraph(f"<font name='TimesNewRoman' size=12>{CONTACT}</font>", styles['Normal'])
                elements.append(title)
                elements.append(address)
                elements.append(contact)

                # Add spacer to title
                elements.append(Spacer(1, 12))
                report_title = Paragraph("<font name='TimesNewRoman' size=14>Scheduling Report</font>", styles['Title'])
                elements.append(report_title)

                # Add space
                elements.append(Spacer(1, 12))

                # Table Header
                table_data = [["Schedule ID", "Member ID", "Employee ID", "Appointment Type", "Appointment Name",
                               "Appointment Date", "Appointment Start Time", "Appointment End Time", "Status"]]

                # Adding data to table
                for row in rows:
                    table_data.append(list(row))

                # Specifying smaller column widths to fit the table
                col_widths = [60, 100, 100, 100, 100, 100, 100, 100, 80]

                # Creating table with smaller font size and styles
                table = Table(table_data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
                    ('GRID', (0, 0), (-1, -1), 1, 'black')
                ]))

                elements.append(table)
                elements.append(Spacer(1, 12))

                styles = getSampleStyleSheet()
                right_aligned_style = ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT)

                timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
                generated_time = Paragraph(f"Generated on: {timestamp} by {full_name}", right_aligned_style)
                elements.append(Spacer(1, 1))
                elements.append(generated_time)

                doc.build(elements)

                QMessageBox.information(None, 'Success',
                                        f'Scheduling Report generated successfully!\nSaved at: {pdf_file}')

            except Exception as e:
                QMessageBox.critical(None, 'Error', f'An error occurred: {str(e)}')

    # Function to generate Stock Report
    def generate_stock_report(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = """
        SELECT product_id, name, quantity, price, expiry_date, purchase_date, supplier, brand, status, sku
        FROM Products
        ORDER BY name
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        full_name = session_manager.get_full_name()

        pdf_file = os.path.join(OUTPUT_DIR, f'Stock_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')

        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
        elements = []

        styles = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

        # Center the title
        title_style = styles['Title']
        title_style.alignment = TA_CENTER
        title = Paragraph("<font name='TimesNewRoman' color='blue' size=18>Slimmer World</font>", styles['Title'])

        # Center the address
        address_style = styles['Normal']
        address_style.alignment = TA_CENTER
        address = Paragraph(f"<font name='TimesNewRoman' size=12>{ADDRESS}</font>", styles['Normal'])

        # Center the contact
        contact_style = styles['Normal']
        contact_style.alignment = TA_CENTER
        contact = Paragraph(f"<font name='TimesNewRoman' size=12>{CONTACT}</font>", styles['Normal'])
        elements.append(title)
        elements.append(address)
        elements.append(contact)

        # Add spacer to title
        elements.append(Spacer(1, 12))
        report_title = Paragraph("<font name='TimesNewRoman' size=14>Stock Report</font>", styles['Title'])
        elements.append(report_title)

        # Add space
        elements.append(Spacer(1, 12))

        # Table Header
        table_data = [
            ["Product ID", "Name", "Quantity", "Price", "Expiry Date", "Purchase Date", "Supplier", "Brand", "Status",
             "SKU"]
        ]

        # Adding data to table
        for row in rows:
            table_data.append(list(row))

        # Specifying smaller column widths to fit the table
        col_widths = [80, 100, 60, 60, 80, 80, 80, 60, 60, 80]

        # Creating table with smaller font size and styles
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
            ('GRID', (0, 0), (-1, -1), 1, 'black'),
            ('WORDWRAP', (0, 0), (-1, -1), 'ON'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        right_aligned_style = ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT)

        timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
        generated_time = Paragraph(f"Generated on: {timestamp} by {full_name}", right_aligned_style)
        elements.append(Spacer(1, 1))
        elements.append(generated_time)

        doc.build(elements)

        QMessageBox.information(None, 'Success', f'Stock Report generated successfully!\nSaved at: {pdf_file}')

    def generate_attendance_report(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = """
        SELECT attendance_id, member_id, entry_time, exit_time, date
        FROM Attendance
        ORDER BY attendance_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        full_name = session_manager.get_full_name()

        pdf_file = os.path.join(OUTPUT_DIR, f'Attendance_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')

        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
        elements = []

        styles = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

        # Center the title
        title_style = styles['Title']
        title_style.alignment = TA_CENTER
        title = Paragraph("<font name='TimesNewRoman' color='blue' size=18>Slimmer World</font>", styles['Title'])

        # Center the address
        address_style = styles['Normal']
        address_style.alignment = TA_CENTER
        address = Paragraph(f"<font name='TimesNewRoman' size=12>{ADDRESS}</font>", styles['Normal'])

        # Center the contact
        contact_style = styles['Normal']
        contact_style.alignment = TA_CENTER
        contact = Paragraph(f"<font name='TimesNewRoman' size=12>{CONTACT}</font>", styles['Normal'])
        elements.append(title)
        elements.append(address)
        elements.append(contact)

        # Add spacer to title
        elements.append(Spacer(1, 12))
        report_title = Paragraph("<font name='TimesNewRoman' size=14>Attendance Report</font>", styles['Title'])
        elements.append(report_title)

        # Add space
        elements.append(Spacer(1, 12))

        # Table Header
        table_data = [
            ["Attendance ID", "Member ID", "Entry Time", "Exit Time", "Date"]
        ]

        # Adding data to table
        for row in rows:
            table_data.append(list(row))

        # Specifying smaller column widths to fit the table
        col_widths = [80, 100, 60, 60, 80, 80, 80, 60, 60, 80]

        # Creating table with smaller font size and styles
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
            ('GRID', (0, 0), (-1, -1), 1, 'black'),
            ('WORDWRAP', (0, 0), (-1, -1), 'ON'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        right_aligned_style = ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT)

        timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
        generated_time = Paragraph(f"Generated on: {timestamp} by {full_name}", right_aligned_style)
        elements.append(Spacer(1, 1))
        elements.append(generated_time)

        doc.build(elements)

        QMessageBox.information(None, 'Success', f'Attendance Report generated successfully!\nSaved at: {pdf_file}')
