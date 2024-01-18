import flet as ft
import defs.defs_data as defs_data
from defs.classes import Agent
import datetime

class AgentView(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.agent_form = AgentForm()
        return ft.Column(
            controls=[
                ft.Divider(),
                ft.IconButton(icon=ft.icons.ADD,
                              on_click=self.add_clicked),
                self.agent_form
            ]
        )
    
    def add_clicked(self,e):
        self.agent_form.visible = True
        self.agent_form.disabled = False
        self.agent_form.txt_cuil.focus()
        self.update()


class AgentForm(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.visible = False
        self.disabled = True

    def build(self):
        self.txt_cuil = ft.TextField(label='Cuil')
        self.txt_first = ft.TextField(label='Nombre')
        self.txt_last = ft.TextField(label='Apellido')
        self.txt_admission = ft.TextField(label='Ingreso', expand=1)
        self.txt_area = ft.TextField(label='Area')
       
        self.date_picker = ft.DatePicker(
            expand=3,
            first_date=datetime.datetime(1910,1,1),
            last_date=datetime.datetime(2030,1,1),
            on_change=self.datepicker_change,
            on_dismiss=self.datepicker_dismiss
        )
        self.date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
        )
       
        self.close_button = ft.IconButton(
            icon=ft.icons.CLOSE,
            on_click=self.close_clicked
        )
        self.confirm_button = ft.IconButton(
            icon=ft.icons.CHECK,
            on_click=self.confirm_clicked
        )

        self.error_text = ft.Text()
        self.error_container = ft.Container(
            bgcolor=ft.colors.RED,
            visible=False,
            content=self.error_text
        )

        return ft.Column(
                width=400,
                controls=[
                    self.txt_cuil,
                    self.txt_first,
                    self.txt_last,
                    ft.Row(
                        controls=[
                            self.txt_admission,
                            self.date_picker,
                            self.date_button
                        ]
                    ),
                    self.txt_area,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            self.close_button,
                            self.confirm_button
                        ]
                    ),
                    self.error_container
                ]
            )
    
    def datepicker_change(self,e):
        self.txt_admission.value = self.date_picker.value.strftime(r'%d/%m/%Y')
        self.update()
    
    def datepicker_dismiss(self,e):
        pass

    def close_clicked(self, e):
        self.txt_cuil.value = ""
        self.txt_first.value = ""
        self.txt_last.value = ""
        self.txt_area.value = ""
        self.txt_admission.value = ""
        self.visible = False
        self.disabled = True
        self.update()
    
    def confirm_clicked(self,e):
        try:
            agent_instance = Agent(
                cuil=self.txt_cuil.value,
                first=self.txt_first.value,
                last=self.txt_last.value,
                admission=self.txt_admission.value
            )

            conn, cursor = defs_data.connect_start('data/dataBase.db')
            defs_data.push_agent(conn,cursor,agent_instance)
            defs_data.connect_end(conn)
        except ValueError:
            self.error_text.value = ValueError
            self.error_container.visible = True
            self.update()


    
    