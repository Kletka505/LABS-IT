import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="postgres",
                                     user="postgres",
                                     password="3478",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")
        self.sunday_gbox = QGroupBox("Sunday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()
        self.shbox6 = QHBoxLayout()
        self.shbox7 = QHBoxLayout()
        self.shbox_up = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.svbox.addLayout(self.shbox5)
        self.svbox.addLayout(self.shbox6)
        self.svbox.addLayout(self.shbox7)
        self.svbox.addLayout(self.shbox_up)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox2.addWidget(self.tuesday_gbox)
        self.shbox3.addWidget(self.wednesday_gbox)
        self.shbox4.addWidget(self.thursday_gbox)
        self.shbox5.addWidget(self.friday_gbox)
        self.shbox6.addWidget(self.saturday_gbox)
        self.shbox7.addWidget(self.sunday_gbox)

        self._create_tables()

        self.update_shedule_button = QPushButton("Update")
        self.shbox_up.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        # self.tuesday_table = QTableWidget()
        # self.wednesday_table = QTableWidget()
        # self.thursday_table = QTableWidget()
        # self.friday_table = QTableWidget()
        # self.saturday_table = QTableWidget()
        # self.sunday_table = QTableWidget()

        self.shedule_tab.setLayout(self.svbox)
        # self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.sunday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    def _create_tables(self):
        self.monday_table = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='wednesday'")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 3, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.monday_table.resizeRowsToContents()

    def _update_shedule(self):
        self._update_monday_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())



