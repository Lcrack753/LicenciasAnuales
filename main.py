import flet as ft
from views.AgentTab import AgentTable
from defs.defs_data import *




def main(page: ft.Page):

    
    def search_agent(e):
        

    txt_query_agent = ft.TextField(label='query', on_change=search_agent)

    tab_general = ft.Tabs(
        selected_index=0,
        animation_duration=100,
        tabs=[
            ft.Tab(
                text="AGENTES",
                content = ft.Column(
                    [txt_query_agent,
                     table_agent]
                ),
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