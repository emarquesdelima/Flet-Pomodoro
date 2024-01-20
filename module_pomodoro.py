from flet import *
from datetime import datetime
import time
import threading
import inspect
import sys

'''
To do list:
    - If the timer is running and you change the phase the start/stop button doesn't update value as the timer stop when you change phase
    - Need to implement the entire settings functionality properly
        - Need to create input validation function
        - Need to create apply settings function
'''


class PomodoroModule(UserControl):
    def __init__(self, page, debug: bool = False):
        print('\n___Starting PomodoroModule__________________________')
        super().__init__()
        self.page = page
        self.debug = debug
        self.verbose()

        # Logic Itens
        self.focus_time = 30 * 60
        self.short_break_time = 10 * 60
        self.long_break_time = 20 * 60
        self.current_phase = 0
        self.cycle_lenght = 4
        self.phase_cycle = self.cycle_generator()
        self.current_counter = self.phase_cycle[self.current_phase][1]
        self.is_running = False
        self.update_ui = True
        self.focus_counter = 0

        # UI Itens - Settings
        self.focus_period_field = TextField(value=int(self.focus_time / 60))
        self.short_break_field = TextField(
            value=int(self.short_break_time / 60))
        self.long_break_field = TextField(value=int(self.long_break_time / 60))
        self.cycle_lenght_field = TextField(value=self.cycle_lenght)
        self.reset_settings_button = OutlinedButton(
            'Reset Settings'
        )
        self.apply_setting_button = OutlinedButton(
            'Apply'
        )
        self.settings_container = BottomSheet()
        self.open_settings_button = IconButton(icon=icons.SETTINGS)
        self.close_settings_button = IconButton()

        # UI Itens - Pomodoro Timer
        self.display_mins = Text(f'{divmod(self.current_counter, 60)[0]:02d}')
        self.display_secs = Text(f'{divmod(self.current_counter, 60)[1]:02d}')
        self.current_phase_name = Text(self.phase_cycle[self.current_phase][0])
        self.start_stop_button = OutlinedButton(
            'Start'
        )
        self.set_focus_button = OutlinedButton(
            'Focus', disabled=True
        )
        self.set_short_break_button = OutlinedButton(
            'Short Break'
        )
        self.set_long_break_button = OutlinedButton(
            'Long Break'
        )
        self.timer_container = Row()
        self.phase_buttons_container = Row()
        self.start_stop_settings_container = Row()
        self.final_timer_container = Column()

        self.print_attributes()

    # Functions - Debug Tools
    def verbose(self, observations=None):
        if self.debug:
            frame = inspect.currentframe()
            caller_frame = frame.f_back
            function_name = caller_frame.f_code.co_name

            verbose_text = f' -> {function_name} '
            if observations:
                verbose_text += f' | {observations}...'
            else:
                verbose_text += '...'

            print(verbose_text)

    def update_time(self):
        if self.debug:
            return 0.0001
        else:
            return 1

    def print_attributes(self):
        """
        Prints the main attributes of the PomodoroModule for debugging purposes.
        """
        print("PomodoroModule Attributes:")
        print(f"  Focus Time: {self.focus_time} seconds")
        print(f"  Short Break Time: {self.short_break_time} seconds")
        print(f"  Long Break Time: {self.long_break_time} seconds")
        print(f"  Current Phase: {self.current_phase}")
        print(f"  Cycle Length: {self.cycle_lenght}")
        print(f"  Phase Cycle: {self.phase_cycle}")
        print(f"  Current Counter: {self.current_counter}")
        print(f"  Is Running: {self.is_running}")
        print(f"  Update UI: {self.update_ui}")
        print(f"  Focus Counter: {self.focus_counter}")

    # Functions - Threading
    def did_mount(self):
        self.verbose()
        self.th = threading.Thread(
            target=self.run_timer, args=(), daemon=True
        )
        self.th.start()
        self.verbose(self.th)

    def will_unmount(self):
        self.verbose()
        self.is_running = False

    # Functions - Settings
    def cycle_generator(self):
        self.verbose(self.cycle_lenght)
        lenght = self.cycle_lenght
        phase_cycle = []

        focus = ['Focus', self.focus_time]
        short_break = ['Short Break', self.short_break_time]
        long_break = ['Long Break', self.long_break_time]

        for x in range(lenght):
            if x + 1 < lenght:
                phase_cycle.append(focus)
                phase_cycle.append(short_break)
            elif x+1 == lenght:
                phase_cycle.append(focus)
                phase_cycle.append(long_break)
            else:
                self.verbose('Error: lenght > cycle_lenght')
        self.phase_cycle = phase_cycle
        self.verbose(self.phase_cycle)

        return phase_cycle

    def reset_settings(self, e):
        self.verbose()
        self.focus_period_field.value = 30
        self.short_break_field.value = 10
        self.long_break_field.value = 20
        self.focus_period_field.update()
        self.short_break_field.update()
        self.long_break_field.update()
        # self.cycle_generator()

    def reset_timer(self):
        self.verbose()
        self.current_phase = 0
        self.current_counter = self.phase_cycle[self.current_phase][1]

        self.update_timer_display()

        self.is_running = False
        self.start_stop_button.text = 'Start'
        self.start_stop_button.update()

    def apply_settings(self, args=None):
        self.verbose()

        self.focus_time = int(self.focus_period_field.value) * 60
        self.short_break_time = int(self.short_break_field.value) * 60
        self.long_break_time = int(self.long_break_field.value) * 60
        self.cycle_lenght = int(self.cycle_lenght_field.value)

        self.cycle_generator()
        self.reset_timer()

        self.settings_container.open = False
        self.settings_container.update()

    def validate_input(self):
        raise NotImplemented

    # Functions - Pomodoro Timer

    def start_stop_timer(self, e):
        self.verbose(f'From: {self.is_running}')
        self.is_running = not self.is_running
        e.control.text = 'Stop' if self.is_running else 'Start'
        self.update()
        self.verbose(f'To: {self.is_running}')

    def update_timer_display(self):
        # self.verbose(
        #     f'Current counter -> {self.current_counter}')
        self.display_mins.value, self.display_secs.value = divmod(
            self.current_counter, 60)
        self.display_mins.value = f'{self.display_mins.value:02d}'
        self.display_secs.value = f'{self.display_secs.value:02d}'
        self.update()

    def run_timer(self):
        self.verbose()
        while self.update_ui:
            if self.is_running:
                if self.current_counter > 0:

                    self.current_counter -= 1
                else:
                    if self.phase_cycle[self.current_phase][0] == 'Focus':
                        self.focus_counter += 1
                        self.verbose(
                            f'Focus Period Complete! -> Current Focus Streak [{self.focus_counter}]')
                    self.switch_phase()
                self.update_timer_display()
            time.sleep(self.update_time())

    def update_button_states(self):
        self.verbose()
        focus_active = self.current_phase_name.value == 'Focus'
        short_break_active = self.current_phase_name.value == 'Short Break'
        long_break_active = self.current_phase_name.value == 'Long Break'

        self.set_focus_button.disabled = focus_active
        self.set_short_break_button.disabled = short_break_active
        self.set_long_break_button.disabled = long_break_active
        self.update()

    def switch_phase(self):
        self.verbose(
            f'From: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')
        self.current_phase += 1
        if self.current_phase < len(self.phase_cycle):
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
            self.verbose(
                f'To: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')
        elif self.current_phase == len(self.phase_cycle):
            self.current_phase = 0
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
            self.verbose(
                f'Restarting cycle to: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')
        self.update()
        self.update_button_states()

    def set_phase_cycle(self, e):
        self.verbose(f'Button clicked: {e.control.text}')

        def set_phase(phase_name):
            # self.verbose(f'{phase_name}')
            for phase in self.phase_cycle:
                if phase[0] == phase_name:
                    self.current_phase_name.value = phase_name
                    self.current_counter = phase[1]
                    self.update_button_states()
                    self.update_timer_display()
                    self.is_running = False
                    self.start_stop_button.text = 'Start'
                    self.start_stop_button.update()
                    break

        # Determine which button was clicked and set the phase accordingly
        if e.control.text == 'Focus':
            set_phase('Focus')
        elif e.control.text == 'Short Break':
            set_phase('Short Break')
        elif e.control.text == 'Long Break':
            set_phase('Long Break')
        else:
            self.verbose('Unknown button clicked')

    # Functions - Build

    def SettingsDisplay(self):
        self.verbose()

        def close_settings(e):
            self.verbose()
            self.settings_container.open = False
            self.settings_container.update()

        self.close_settings_button.icon = icons.CLOSE
        self.close_settings_button.on_click = close_settings

        self.apply_setting_button.on_click = self.apply_settings

        self.focus_period_field.label = 'Focus Period'
        self.short_break_field.label = 'Short Break'
        self.long_break_field.label = 'Long Break'
        self.cycle_lenght_field.label = 'Cycle Length'

        self.reset_settings_button.on_click = self.reset_settings

        self.settings_container.content = Container(
            content=Column(
                controls=[
                    self.close_settings_button,
                    self.focus_period_field,
                    self.short_break_field,
                    self.long_break_field,
                    self.cycle_lenght_field,
                    Row(
                        controls=[
                            self.apply_setting_button,
                            self.reset_settings_button
                        ]
                    )
                ]
            )
        )

    def PomodoroDisplay(self):
        self.verbose()

        def show_settings(e):
            self.verbose()
            self.settings_container.open = True
            self.settings_container.update()

        def phase_buttons():
            self.verbose()
            self.set_focus_button.on_click = self.set_phase_cycle
            self.set_short_break_button.on_click = self.set_phase_cycle
            self.set_long_break_button.on_click = self.set_phase_cycle

            self.phase_buttons_container.controls.append(
                self.set_focus_button)
            self.phase_buttons_container.controls.append(
                self.set_short_break_button)
            self.phase_buttons_container.controls.append(
                self.set_long_break_button)

            self.phase_buttons_container.wrap = True
            self.phase_buttons_container.alignment = MainAxisAlignment.CENTER
            self.phase_buttons_container.vertical_alignment = CrossAxisAlignment.CENTER

            return self.phase_buttons_container

        def timer_display():
            self.verbose()
            # Display Mins properties
            self.display_mins.theme_style = TextThemeStyle.DISPLAY_LARGE

            # Display Secs properties
            self.display_secs.theme_style = TextThemeStyle.DISPLAY_MEDIUM

            # Setting Start Stop btn function
            self.start_stop_button.on_click = self.start_stop_timer

            # Setting timer container properties
            self.timer_container.wrap = True
            self.timer_container.alignment = MainAxisAlignment.CENTER
            self.timer_container.vertical_alignment = CrossAxisAlignment.CENTER

            # Adding controls
            self.timer_container.controls.append(self.display_mins)
            self.timer_container.controls.append(self.display_secs)

            return self.timer_container

        def final_timer_display():
            self.verbose()
            # Open Setting Button setup
            self.open_settings_button.on_click = show_settings

            # Setting container properties
            self.final_timer_container.alignment = MainAxisAlignment.CENTER
            self.final_timer_container.horizontal_alignment = CrossAxisAlignment.CENTER
            self.final_timer_container.wrap = True

            self.start_stop_settings_container.controls.append(
                self.start_stop_button)
            self.start_stop_settings_container.controls.append(
                self.open_settings_button)

            # Adding Controls
            self.final_timer_container.controls.append(phase_buttons())
            self.final_timer_container.controls.append(timer_display())
            self.final_timer_container.controls.append(
                self.start_stop_settings_container)

            return self.final_timer_container

        return final_timer_display()

    def build(self):
        self.verbose()
        self.SettingsDisplay()
        self.page.overlay.append(self.settings_container)
        return self.PomodoroDisplay()


def main(page: Page):
    page.title = 'Pomodoro Module'
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    print('\n\n\n\n__________Instatiating Pomodoro Module__________')
    pomodoro = PomodoroModule(page, debug=True)

    # page.add(PomodoroModule(debug=True))
    print('\n__________Adding module to page__________')
    page.add(pomodoro)


if __name__ == '__main__':
    app(target=main)
