from flet import *
from datetime import datetime
import time
import threading
from modules import *


def main(page: Page):
    page.title = 'Pomodoro'
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Settings Assets
    # def retrieve_settings():
    #     pomodoro_settings = {
    #         'focus_period': focus_period.value,
    #         'short_break': short_break.value,
    #         'long_break': long_break.value
    #     }
    #     print(f'''Settings updated!
    # Focus -> {pomodoro_settings["focus_period"]}
    # Short Break -> {pomodoro_settings["short_break"]}
    # Long Break -> {pomodoro_settings["long_break"]}''')

    #     return pomodoro_settings

    # def reset_settings(e):
    #     focus_period.value = 30
    #     short_break.value = 10
    #     long_break.value = 20
    #     retrieve_settings()
    #     page.update()

    # focus_period = TextField(
    #     value=30,
    #     label='Focus Period',
    #     color='gray',
    #     # border_color='transparent',
    #     suffix_text='min',
    #     # on_change=retrieve_settings,
    #     hint_text='Time in minutes',
    #     hint_style=TextStyle(
    #         size=11,
    #         color='gray'
    #     )
    # )

    # short_break = TextField(
    #     value=10,
    #     label='Short Break',
    #     color='gray',
    #     # border_color='transparent',
    #     suffix_text='min',
    #     # on_change=retrieve_settings,
    #     hint_text='Time in minutes',
    #     hint_style=TextStyle(
    #         size=11,
    #         color='gray'
    #     )
    # )

    # long_break = TextField(
    #     value=20,
    #     label='Long Break',
    #     color='gray',
    #     # border_color='transparent',
    #     suffix_text='min',
    #     # on_change=retrieve_settings,
    #     hint_text='Time in minutes',
    #     hint_style=TextStyle(
    #         size=11,
    #         color='gray'
    #     )
    # )

    # btn_reset_settings = OutlinedButton(
    #     text='Reset Settings',
    #     on_click=reset_settings
    # )

    # settings_container = Container(
    #     alignment=alignment.center,
    #     margin=20,
    #     content=Column(
    #         # alignment=MainAxisAlignment.SPACE_BETWEEN,
    #         controls=[
    #             focus_period,
    #             short_break,
    #             long_break,
    #             btn_reset_settings
    #         ],
    #     ),

    # )

    # settings = Tab(
    #     text='Setings',
    #     content=settings_container,
    # )

    # Aplication

    divider = Divider(
        color='GREY'
    )

    header = Text(
        'Pomodoro',
        text_align='center',
        style=TextThemeStyle.DISPLAY_MEDIUM,
    )

    # settings_dict = {
    #     'focus_period': focus_period.value,
    #     'short_break': short_break.value,
    #     'long_break': long_break.value
    # }

    # print('Calling into the variable')
    # pomodoro_module = PomodoroModule(page)

    # pomodoro_settings = pomodoro_module.SettingsDisplay()

    # pomodoro_timer = pomodoro_module.PomodoroTimer()

    print('Calling into the main body')
    main_body = Tabs(
        tab_alignment=TabAlignment.CENTER,
        indicator_tab_size=True,
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            # Tab(
            #     text='Pomodoro',
            #     content=pomodoro_timer
            # ),
            # Tab(
            #     text='Settings',
            #     content=pomodoro_settings
            # ),
            Tab(
                text='Teste',
                content=PomodoroModule(page)
            )
        ]
    )

    print('before page.add')
    page.add(
        header,
        divider,
        main_body
    )


app(target=main)
