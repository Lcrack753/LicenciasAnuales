import flet as ft
from views.AgentView import *

def main(page: ft.Page):
    page.title = 'Licencias Anuales'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    agente_view = AgentView()
    # license_view = LicenseView()

    t = ft.Tabs(
        selected_index=0,
        animation_duration=350,
        tab_alignment=ft.TabAlignment.CENTER,
        tabs=[
            ft.Tab(
                text='Agentes',
                content = agente_view,
            ),
            ft.Tab(
                text='Licencias',
                # content=license_view
            )
            
        ]
    )

    page.add(agente_view)

ft.app(target=main)