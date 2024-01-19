import flet as ft
import defs.defs_data as defs_data
from defs.classes import Agent
import datetime

class AgentView(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.agent_form = AgentForm()
        self.agent_table = AgentTable()
        return ft.Column(
            controls=[
                ft.Divider(),
                ft.IconButton(icon=ft.icons.ADD,
                              on_click=self.add_clicked),
                self.agent_form,
                self.agent_table
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

        self.error_text = ft.Text(size=20, text_align=ft.TextAlign.CENTER)
        self.error_container = ft.Container(
            bgcolor=ft.colors.RED,
            visible=False,
            alignment=ft.alignment.center,
            padding=5,
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
        self.clean(e)
        self.visible = False
        self.disabled = True
        self.update()
    
    def confirm_clicked(self,e):
        try:
            if self.txt_cuil.value == '' and len(self.txt_cuil.value) != 11 and self.txt_admission.value == '':
                raise ValueError('')
            agent_instance = Agent(
                cuil=self.txt_cuil.value,
                first=self.txt_first.value,
                last=self.txt_last.value,
                admission=self.txt_admission.value,
                area=self.txt_area.value
            )
            conn, cursor = defs_data.connect_start('data/dataBase.db')
            defs_data.push_agent(conn,cursor,agent_instance)
            defs_data.connect_end(conn)
            self.clean(e)
        except ValueError:
            self.error_text.value = 'Datos Invalidos'
            self.error_container.visible = True
            self.update()

    def clean(self,e):
        self.txt_cuil.value = ""
        self.txt_first.value = ""
        self.txt_last.value = ""
        self.txt_area.value = ""
        self.txt_admission.value = ""
        self.error_container.visible = False

    
# class AgentTable(ft.UserControl):
#     def __init__(self):
#         super().__init__()

#     def build(self):
        
#         self.table = ft.DataTable()
#         self.filter = ft.TextField(label='Filtro', value='', on_change=self.fetch)
#         # self.lv = ft.ListView(
#         #     expand=1,
#         #     auto_scroll=True
#         # )
#         return ft.Column(
#             controls=[
#                 self.filter,
#                 self.table
#             ]
#         )

    
#     def fetch(self,e):
#         conn, cursor = defs_data.connect_start('data/dataBase.db')
#         fetched_headers = defs_data.fetch_agent(conn,cursor,fetch_headers=True)
#         fetched_rows = defs_data.fetch_agent(conn,cursor,query=self.filter.value)

#         headers = [ft.DataColumn(ft.Text(header)) for header in fetched_headers]
#         days_avalible = [
#             ft.DataColumn(ft.Text('2021')),
#             ft.DataColumn(ft.Text('2022')),
#             ft.DataColumn(ft.Text('2023')),
#             ft.DataColumn(ft.Text('2024')),
#             ft.DataColumn(ft.Text('2025')),
#         ]
#         for col in days_avalible:
#             headers.append(col)

#         rows = []
#         for row in fetched_rows:
#             agent_instance = Agent(row[1],row[2],row[3],row[4],row[5])
#             fetched_license = defs_data.fetch_license(conn,cursor,agent_instance.cuil,reduce=True)
#             days = agent_instance.days_available(fetched_license,to_dict=True)
#             z = ft.DataRow(
#                 cells=[
#                     ft.DataCell(ft.Text(agent_instance.cuil)),
#                     ft.DataCell(ft.Text(agent_instance.first)),
#                     ft.DataCell(ft.Text(agent_instance.last)),
#                     ft.DataCell(ft.Text(agent_instance.admission)),
#                     ft.DataCell(ft.Text(agent_instance.area)),
#                     ft.DataCell(ft.Text(str(days['2021-12-01']))),
#                     ft.DataCell(ft.Text(str(days['2022-12-01']))),
#                     ft.DataCell(ft.Text(str(days['2023-12-01']))),
#                     ft.DataCell(ft.Text(str(days['2024-12-01']))),
#                     ft.DataCell(ft.Text(str(days['2025-12-01']))),
#                 ]
#             )
#             rows.append(z)

#         self.table.columns = headers
#         self.table.rows = rows
#         defs_data.connect_end(conn)
        
class AgentTable(ft.UserControl):
    def __init__(self):
        super().__init__()
    
    def build(self):
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        fetched_rows = defs_data.fetch_agent(conn,cursor)
        col = ft.Column(width=1200)
        for row in fetched_rows:
            col.controls.append(AgentRow(Agent(row[1],row[2],row[3],row[4],row[5])))
            col.controls.append(ft.Divider())
        return col 
        

class AgentRow(ft.UserControl):
    def __init__(self, agent: Agent, licenses: list() = []):
        self.agent = agent
        super().__init__()
        w = 100
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        fetched_licenses = defs_data.fetch_license(conn,cursor,self.agent.cuil,reduce=True)
        self.z = self.agent.days_available(fetched_licenses,to_dict=True)

    
    def build(self):
        w = 125
        self.cuil = ft.Text(self.agent.cuil, text_align=ft.TextAlign.CENTER,width=w)
        self.first = ft.Text(self.agent.first, text_align=ft.TextAlign.CENTER,width=w)
        self.last = ft.Text(self.agent.last, text_align=ft.TextAlign.CENTER,width=w)
        self.admission = ft.Text(self.agent.admission, text_align=ft.TextAlign.CENTER,width=w)
        self.area = ft.Text(self.agent.area, text_align=ft.TextAlign.CENTER,width=w)
        self.year_2021 = ft.Text(self.z['2021-12-01'], width=w//2)
        self.year_2022 = ft.Text(self.z['2022-12-01'], width=w//2)
        self.year_2023 = ft.Text(self.z['2023-12-01'], width=w//2)
        self.year_2024 = ft.Text(self.z['2024-12-01'], width=w//2)
        self.year_2025 = ft.Text(self.z['2025-12-01'], width=w//2)
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT,width=w)
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE,width=w)
        
        return ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.cuil,
                    self.first,
                    self.last,
                    self.admission,
                    self.area,
                    self.year_2021,
                    self.year_2022,
                    self.year_2023,
                    self.year_2024,
                    self.year_2025,
                    self.edit_button,
                    self.delete_button
                    ]
                )