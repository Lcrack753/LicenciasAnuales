import flet as ft
import datetime
from defs.defs_data import *


class AgentView(ft.UserControl):
    def __init__(self):
        super().__init__()
        conn, cursor = connect_start('./data/dataBase.db')
        self.rows = self.fetch(conn,cursor)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cuil")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Ingreso")),
                ft.DataColumn(ft.Text("Area")),

            ],
            rows= self.rows
        )
        connect_end(conn)
    

    def fetch(self,conn,cursor):
        rowlist = []
        for row in fetch_agent(conn,cursor):
            datarow = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row[1]))),
                    ft.DataCell(ft.Text(str(row[2]))),
                    ft.DataCell(ft.Text(str(row[3]))),
                    ft.DataCell(ft.Text(str(row[4]))),
                    ft.DataCell(ft.Text(str(row[5])))
                ]
            )
            rowlist.append(datarow)
        return rowlist

    def build(self):
        return self.table
    


class AgentForm(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.txt_cuil = ft.TextField(label='Cuil', width=200)
        self.txt_first = ft.TextField(label='Nombre')
        self.txt_last = ft.TextField(label='Apellido')
        self.txt_admission = ft.TextField(label='Ingreso',keyboard_type='DATETIME')
        self.date_picker = ft.DatePicker(
                                on_change= self.change_date,
                                first_date=datetime.datetime(1910, 1, 1),
                                last_date=datetime.datetime(2027, 1, 1)
        )
        self.date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: self.date_picker.pick_date(),
    )
        self.area = ft.TextField(label='Area')
        self.btn_push = ft.IconButton(icon=ft.icons.CHECK)
    
    def change_date(self, e):
        date = self.date_picker.value
        self.txt_admission.value = date.strftime(r'%d/%m/%Y')
        self.txt_admission.update()

    def build(self):
        self.row = ft.Column(
            [self.txt_cuil,
                self.txt_first,
                self.txt_last,
                ft.Row(
                    [self.txt_admission,
                     self.date_button
                     ]
                ),
                self.area,
                self.btn_push],
            height=500,
            
        )
        return self.row