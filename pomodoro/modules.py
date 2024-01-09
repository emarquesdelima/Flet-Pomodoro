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
        self.current_counter = self.focus_time
        self.is_running = False
        self.btn_text = 'Start'
        super().__init__()

        self.start_stop_btn = OutlinedButton(
            self.btn_text,
            on_click=self.toggle_timer
        )

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(
            target=self.counter_update,
            args=(),
            daemon=True
        )
        self.th.start()

    def will_unmount(self):
        self.running = False

    def toggle_timer(self, e):
        self.is_running = not self.is_running  # Toggle the running state
        if self.is_running:
            e.control.text = "Stop"
            if not hasattr(self, 'th') or not self.th.is_alive():
                # Start the thread only if it hasn't been started or if it's not alive
                self.th = threading.Thread(
                    target=self.counter_update, daemon=True)
                self.th.start()
        else:
            e.control.text = "Start"
        self.update()
        print(e)

    def counter_update(self):
        counter = self.current_counter
        while counter > 0 and self.is_running:
            mins, secs = divmod(self.time, 60)
            self.min_display.value = "{:02d}".format(mins)
            self.sec_display.value = "{:02d}".format(secs)
            self.update()
            time.sleep(1)
            counter -= 1

    def counter_module(self):
        mins, secs = divmod(self.current_counter, 60)
        self.min_display = Text("{:02d}".format(mins))
        self.sec_display = Text("{:02d}".format(secs))
        mounted_display = Column(
            controls=[
                Row([self.min_display, self.sec_display]),
                self.start_stop_btn
            ]
        )

        self.main_display = mounted_display
        return self.main_display

    def tab(self, text: str):
        self.focus = Tab(
            text=text,
            content=self.counter_module()
        )

        return self.focus

    def pomodoro_tabs(self):
        self.tabs = Tabs(
            tab_alignment=TabAlignment.CENTER,
            indicator_tab_size=True,
            animation_duration=300,
            expand=1,
            tabs=[
                self.tab(text='Focus'),
                self.tab(text='Short Break'),
                self.tab(text='Long Break'),
            ]
        )

    def build(self):
        return Container(
            alignment=alignment.center,
            margin=20,
            content=self.pomodoro_tabs()
        )
