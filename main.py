import flet as ft
from views.AgentTab import AgentView
from defs.defs_data import *




def main(page: ft.Page):
    tab_general = ft.Tabs(
        selected_index=0,
        animation_duration=100,
        tabs=[
            ft.Tab(
                text="AGENTES",
                content= AgentView(),
            ),
            ft.Tab(
                text="LICENCIAS",
            ),
            ft.Tab(
                text="DIAS DISPONIBLES"
            ),
        ],
        expand=2
    )

    page.add(tab_general)  # Access the date_picker attribute

ft.app(target=main)