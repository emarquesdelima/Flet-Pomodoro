from flet import *
from datetime import datetime
import time
import threading


class PomodoroModule(UserControl):
    def __init__(self, page):
        # UI nedded in logic
        print(
            'Starting PomodoroModule_______________________________________________________')
        super().__init__()
        self.focus_period_field = TextField(value=0)
        self.short_break_field = TextField(value=0)
        self.long_break_field = TextField(value=0)

        # Logic
        self.page = page
        self.focus_time = int(self.focus_period_field.value) * 60
        self.short_break_time = int(self.short_break_field.value) * 60
        self.long_break_time = int(self.long_break_field.value) * 60
        self.phase_cycle = [
            ['Focus', lambda: self.focus_time],
            ['Short Break', lambda: self.short_break_time],
            ['Focus', lambda: self.focus_time],
            ['Short Break', lambda: self.short_break_time],
            ['Focus', lambda: self.focus_time],
            ['Long Break', lambda: self.long_break_time],
        ]
        self.current_phase = 0
        self.current_counter = self.phase_cycle[self.current_phase][1]()
        self.is_running = False
        self.update_ui = True

        # UI dependent from logic
        self.display_mins = Text(divmod(self.current_counter, 60)[0])
        self.display_secs = Text(divmod(self.current_counter, 60)[1])
        self.current_phase_name = Text(self.phase_cycle[self.current_phase][0])
        self.start_stop_button = OutlinedButton(
            'Start', on_click=self.start_stop_timer)
        self.update_settings_timer()

    # Threading
    def did_mount(self):
        self.th = threading.Thread(
            target=self.run_timer, args=(), daemon=True
        )
        self.th.start()
        print('Thread Mounted')
        print(self.th)

    def will_unmount(self):
        self.running = False

    # Settings logic
    def reset_timer(self):
        self.current_phase = 0
        self.current_counter = self.phase_cycle[self.current_phase][1]()

        self.update_timer_display()

        self.is_running = False
        self.start_stop_button.text = 'Start'
        self.start_stop_button.update()

    def refresh_timer_display(self):
        if self.is_running:
            print(f'Rodou o reset_timer -> is_running: {self.is_running}')
            self.reset_timer()
        else:
            print(
                f'Rodou o update_timer_display -> is_running: {self.is_running}')
            self.update_timer_display()

    def update_settings_timer(self, optional_arg=None):
        self.focus_time = int(self.focus_period_field.value) * 60
        self.short_break_time = int(self.short_break_field.value) * 60
        self.long_break_time = int(self.long_break_field.value) * 60
        self.current_counter = self.phase_cycle[self.current_phase][1]()
        self.refresh_timer_display()
        self.update()

    def reset_settings(self, e):
        self.focus_period_field.value = 30
        self.short_break_field.value = 10
        self.long_break_field.value = 20
        self.focus_period_field.update()
        self.short_break_field.update()
        self.long_break_field.update()
        self.update_settings_timer()
        print('Settings Reset!___________________')

    # Settings UI
    def settings_text_field(self):
        return TextField(
            on_change=self.update_settings_timer,
            suffix_text='min',
            hint_text='Time in minutes',
            hint_style=TextStyle(
                size=11,
                color='grey'
            )
        )

    def SettingsDisplay(self):
        self.focus_period_field = self.settings_text_field()
        self.focus_period_field.label = 'Focus'
        self.focus_period_field.value = 30

        self.short_break_field = self.settings_text_field()
        self.short_break_field.label = 'Short Break'
        self.short_break_field.value = 10

        self.long_break_field = self.settings_text_field()
        self.long_break_field.label = 'Long Break'
        self.long_break_field.value = 20

        self.btn_reset_settings = OutlinedButton(
            text='Reset Settings',
            on_click=self.reset_settings
        )

        return Container(
            alignment=alignment.center,
            margin=20,
            content=Column(
                # alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.focus_period_field,
                    self.short_break_field,
                    self.long_break_field,
                    self.btn_reset_settings
                ],
            ),
        )

    # Pomodoro Logic

    def switch_phase(self):
        self.current_phase += 1
        if self.current_phase < 6:
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]()
            print(f'A - Phase -> {self.current_phase}')
            print(f'A - Counter -> {self.current_counter}')
            print(f'Thread - {self.th}')
        elif self.current_phase == 6:
            print(f'B - Phase -> {self.current_phase}')
            print(f'B - Counter -> {self.current_counter}')
            print(f'Thread - {self.th}')
            self.current_phase = 0
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]()

    def update_timer_display(self):
        self.display_mins.value, self.display_secs.value = divmod(
            self.current_counter, 60)
        self.update()

    def run_timer(self):
        while self.update_ui:
            if self.is_running:
                if self.current_counter > 0:
                    self.current_counter -= 1
                else:
                    self.switch_phase()
                self.update_timer_display()
            time.sleep(1)

    def start_stop_timer(self, e):
        print(f'is_running was -> {self.is_running}')
        self.is_running = not self.is_running
        e.control.text = 'Stop' if self.is_running else 'Start'
        self.update()
        print(f'is_running is -> {self.is_running}')

    # PomodoroUI
    def TimerDisplay(self):
        return Row(
            controls=[
                self.display_mins,
                self.display_secs
            ]
        )

    def PomodoroTimer(self):
        return Column(
            controls=[
                self.TimerDisplay(),
                self.start_stop_button,
                self.current_phase_name
            ]
        )

    # Build
    def build(self):
        return Column(
            controls=[
                self.PomodoroTimer(),
                self.SettingsDisplay()
            ]
        )
