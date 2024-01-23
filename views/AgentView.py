import flet as ft
import defs.defs_data as defs_data
from defs.classes import Agent, License
import datetime

class AgentView(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.add_agent_button = ft.ElevatedButton('AÑADIR AGENTE', on_click=self.add_agent)
        self.view_agents_button = ft.ElevatedButton('VER AGENTES', on_click=self.view_agent)
        self.add_licenses_button = ft.ElevatedButton('AÑADIR LICENCIA')
        self.view_licenses_button = ft.ElevatedButton('VER LICENCIAS')
        self.buttons = ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.add_agent_button,
                        self.view_agents_button,
                        ft.Divider(),
                        self.add_licenses_button,
                        self.view_licenses_button
                    ]
            )
        self.view = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.view.controls.append(self.buttons)
        return self.view
    
    def add_agent(self,e):
        self.agent_form = AgentForm()
        self.view.controls.clear()
        self.view.controls.append(self.buttons)
        self.view.controls.append(ft.Divider())
        self.view.controls.append(self.agent_form)
        self.view.update()

    def view_agent(self,e):
        self.agent_table = AgentTable(self.view_detail)
        self.view.controls.clear()
        self.view.controls.append(self.buttons)
        self.view.controls.append(ft.Divider())
        self.view.controls.append(self.agent_table)
        self.view.update()

    def view_detail(self,e):
        self.license_view = LicenseView(e)
        self.view.controls.clear()
        self.view.controls.append(self.buttons)
        self.view.controls.append(ft.Divider())
        self.view.controls.append(self.license_view)
        self.view.update()

class AgentForm(ft.UserControl):
    def __init__(self):
        super().__init__()

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
                            # self.close_button,
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
            self.error_text.value = 'Agente Cargado'
            self.error_container.bgcolor = ft.colors.GREEN
            self.error_container.visible = True
            self.update()
            self.update()
        except ValueError:
            self.clean(e)
            self.error_container.bgcolor = ft.colors.RED
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


        
class AgentTable(ft.UserControl):
    def __init__(self, detail):
        super().__init__()
        self.detail = detail
    
    def build(self):
        self.query_txt =  ft.TextField(label='Filtro',on_change=self.query_changed)
        self.agent_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('Cuil')),
                ft.DataColumn(ft.Text('Nombre')),
                ft.DataColumn(ft.Text('Apellido')),
                ft.DataColumn(ft.Text('Ingreso')),
                ft.DataColumn(ft.Text('Area')),
                ft.DataColumn(ft.Text('Dias 2021')),
                ft.DataColumn(ft.Text('Dias 2022')),
                ft.DataColumn(ft.Text('Dias 2023')),
                ft.DataColumn(ft.Text('Dias 2024')),
                ft.DataColumn(ft.Text('Dias 2025')),
                ft.DataColumn(ft.Text('Detalle')),
                ft.DataColumn(ft.Text('Eliminar'))
            ]
        )
        self.update_table()
        return ft.Column(
            controls=[
                self.query_txt,
                ft.ListView(
                    height=600,
                    controls=[self.agent_table]
                )
            ]
        )
    
    def delete_agent(self,agent):
        conn, cursor = defs_data.connect_start('./data/dataBase.db')
        defs_data.delete_agent(conn,cursor,agent.agent)
        defs_data.connect_end(conn)
        self.update_table()
        self.update()
        print('Agente Borrado')
    
    def update_table(self,query = ''):
        self.agent_table.rows.clear()
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        fetched_rows = defs_data.fetch_agent(conn,cursor,self.query_txt.value)
        for row in fetched_rows:
            self.agent_table.rows.append(AgentRow(Agent(row[1],row[2],row[3],row[4],row[5]),self.delete_agent, self.detail).build())

    def query_changed(self,e):
        self.update_table()
        self.update()
        
class AgentRow(ft.UserControl):
    def __init__(self, agent: Agent,delete_agent,detail):
        self.agent = agent
        super().__init__()
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        fetched_licenses = defs_data.fetch_license(conn,cursor,self.agent.cuil,reduce=True)
        self.z = self.agent.days_available(fetched_licenses,to_dict=True)
        self.delete_agent = delete_agent
        self.detail = detail
    
    def build(self):
        self.cuil = ft.Text(self.agent.cuil)
        self.first = ft.Text(self.agent.first)
        self.last = ft.Text(self.agent.last)
        self.admission = ft.Text(self.agent.admission)
        self.area = ft.Text(self.agent.area)
        self.year_2021 = ft.Text(self.z['2021-12-01'])
        self.year_2022 = ft.Text(self.z['2022-12-01'])
        self.year_2023 = ft.Text(self.z['2023-12-01'])
        self.year_2024 = ft.Text(self.z['2024-12-01'])
        self.year_2025 = ft.Text(self.z['2025-12-01'])
        self.edit_button = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=self.detail_clicked)
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete_clicked)
        
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(self.agent.cuil)),
                ft.DataCell(ft.Text(self.agent.first)),
                ft.DataCell(ft.Text(self.agent.last)),
                ft.DataCell(ft.Text(self.agent.admission)),
                ft.DataCell(ft.Text(self.agent.area)),
                ft.DataCell(ft.Text(self.z['2021-12-01'])),
                ft.DataCell(ft.Text(self.z['2022-12-01'])),
                ft.DataCell(ft.Text(self.z['2023-12-01'])),
                ft.DataCell(ft.Text(self.z['2024-12-01'])),
                ft.DataCell(ft.Text(self.z['2025-12-01'])),
                ft.DataCell(self.edit_button),
                ft.DataCell(self.delete_button)
            ]
        )
    
    def delete_clicked(self,e):
        self.delete_agent(self)

    def detail_clicked(self,e):
        self.detail(self)


class LicenseView(ft.UserControl):
    def __init__(self, obj):
        super().__init__()
        self.agent_obj = obj.agent
        

    def build(self):
        self.license_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('Desde')),
                ft.DataColumn(ft.Text('Hasta')),
                ft.DataColumn(ft.Text('Dias')),
                ft.DataColumn(ft.Text('Nota')),
                ft.DataColumn(ft.Text('Eliminar')),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text('prueba')),
                        ft.DataCell(ft.Text('prueba')),
                        ft.DataCell(ft.Text('prueba')),
                        ft.DataCell(ft.Text('prueba')),
                    ]
                )
            ]
        )

        self.view = ft.Column(
            width=600,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text('Cuil:',
                                weight=ft.FontWeight.BOLD),
                        ft.Text(self.agent_obj.cuil)
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text('Nombre:',
                                weight=ft.FontWeight.BOLD),
                        ft.Text(f"{self.agent_obj.last}, {self.agent_obj.first}")
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text('Ingreso:',
                                weight=ft.FontWeight.BOLD),
                        ft.Text(self.agent_obj.admission)
                    ]
                ),
                ft.ListView(
                    height=300,
                    controls=[self.license_table]
                )
            ]
        )

        return self.view
    
    def did_mount(self):
        self.update_table()


    def delete_license(self,e):
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        defs_data.delete_license(conn,cursor,License(e.cuil,e.start,e.end))
        defs_data.connect_end(conn)
        self.update_table()
        self.update()
        print('Licencia Eliminada')
    
    def update_table(self):
        conn, cursor = defs_data.connect_start('data/dataBase.db')
        fetched_licenses = defs_data.fetch_license(conn,cursor,self.agent_obj.cuil)
        self.license_table.rows.clear()
        if len(fetched_licenses) > 0:
            for row in fetched_licenses:
                self.license_table.rows.append(LicenseRow(row,self.delete_license).build())
        self.update()
    
    
class LicenseRow(ft.UserControl):
    def __init__(self, license_tuple, delete):
        super().__init__()
        self.delete_license = delete
        self.cuil = license_tuple[1]
        self.start = license_tuple[2]
        self.end = license_tuple[3]
        self.days_btw = license_tuple[4]
        self.note = license_tuple[5]


    def build(self):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(self.start)),
                ft.DataCell(ft.Text(self.end)),
                ft.DataCell(ft.Text(self.days_btw)),
                ft.DataCell(ft.Text(self.note)),
                ft.DataCell(ft.IconButton(icon=ft.icons.DELETE,
                                          on_click=self.delete))
            ]
        )
    
    def delete(self,e):
        self.delete_license(self)

    