from flet import *
from datetime import datetime
import time
import threading


class PomodoroModule(UserControl):
    def __init__(self, settings):
        print(settings)
        self.settings = settings
        self.focus_time = self.settings['focus_period'] * 60
        self.short_break_time = self.settings['short_break'] * 60
        self.long_break_time = self.settings['long_break'] * 60
        self.phase_cycle = {
            0: ['Focus', self.focus_time],
            1: ['Short Break', self.short_break_time],
            2: ['Focus', self.focus_time],
            3: ['Short Break', self.short_break_time],
            4: ['Focus', self.focus_time],
            5: ['Long Break', self.long_break_time],
        }
        self.current_phase = 0
        self.current_phase_name = Text(self.phase_cycle[self.current_phase][0])
        self.current_counter = self.phase_cycle[self.current_phase][1]
        self.display_mins = Text(divmod(self.current_counter, 60)[0])
        self.display_secs = Text(divmod(self.current_counter, 60)[1])
        self.is_running = False
        self.update_ui = True
        # self.btn_text = 'Start'

        super().__init__()

    # Threading
    def did_mount(self):
        self.th = threading.Thread(
            target=self.run_timer, args=(), daemon=True
        )
        self.th.start()

    def will_unmount(self):
        self.running = False

    # UI
    def TimerDisplay(self):
        return Row(
            controls=[
                self.display_mins,
                self.display_secs
            ]
        )

    # Logic
    def switch_phase(self):
        self.current_phase += 1
        if self.current_phase < 6:
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
            print(f'A - Phase -> {self.current_phase}')
        elif self.current_phase == 6:
            print(f'B - Phase -> {self.current_phase}')
            self.current_phase = 0
            print(f'C - Phase -> {self.current_phase}')
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]

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
        self.is_running = not self.is_running
        e.control.text = 'Stop' if self.is_running else 'Start'
        self.update()

    def build(self):
        start_stop_button = OutlinedButton(
            'Start',
            on_click=self.start_stop_timer
        )
        return Column(
            controls=[
                self.TimerDisplay(),
                start_stop_button,
                self.current_phase_name
            ]
        )
