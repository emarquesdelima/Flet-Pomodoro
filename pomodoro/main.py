from flet import *
from datetime import datetime
import time
import threading
from modules import *


def main(page: Page):
    print(
        '\n \n_____Starting Application_______________________________________________________')
    page.title = 'Pomodoro'
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Aplication

    divider = Divider(
        color='GREY'
    )

    header = Text(
        'Pomodoro',
        text_align='center',
        style=TextThemeStyle.DISPLAY_MEDIUM,
    )

    print('Instantiating PomodoroModule')
    pomodoro = PomodoroModule(page)

    print(pomodoro)

    # print('Calling into the main body')
    # main_body = Tabs(
    #     tab_alignment=TabAlignment.CENTER,
    #     indicator_tab_size=True,
    #     selected_index=0,
    #     animation_duration=300,
    #     expand=True,
    #     tabs=[
    #         # Tab(
    #         #     text='Pomodoro',
    #         #     content=pomodoro.controls[0]
    #         # ),
    #         # Tab(
    #         #     text='Settings',
    #         #     content=pomodoro.controls[1]
    #         # ),
    #         Tab(
    #             text='Teste',
    #             content=pomodoro
    #         )
    #     ]
    # )

    print(pomodoro)

    print('before page.add')
    page.add(
        header,
        divider,
        pomodoro,
        # PomodoroModule(page)
    )

    print(type(pomodoro))


app(target=main)
