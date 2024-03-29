from flet import (Page, app, UserControl, TextField, OutlinedButton,
                  IconButton, Banner, icons, Container, BottomSheet, Text,
                  Row, Column, ButtonStyle, RoundedRectangleBorder, MaterialState,
                  colors, Audio, TextButton, Icon, TextThemeStyle, MainAxisAlignment,
                  CrossAxisAlignment, ScrollMode, TextAlign, Divider, alignment)
from datetime import datetime
import time
import threading
from utility import verbose


class PomodoroModule(UserControl):
    def __init__(self, page, debug: bool = False):
        print('\n___Starting PomodoroModule__________________________')
        super().__init__()
        self.page = page
        self.debug = debug
        verbose(debug=self.debug)

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
        self.cycle_focus_position = 1
        self.cycle_data_storage = []

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
        self.open_settings_button = IconButton(icon=icons.SETTINGS)
        self.close_settings_button = IconButton()
        self.validation_banner = Banner()
        self.settings_container = Container()
        self.settings_bottom_sheet = BottomSheet()

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
        self.restart_button = IconButton()
        self.timer_container = Row()
        self.phase_buttons_container = Column()
        self.reset_timer_settings_container = Row()
        self.final_timer_container = Row()
        self.module_name_phase_cycle = Text(
            f'Pomodoro - {self.cycle_focus_position}/{self.cycle_lenght}')

        self.button_style = ButtonStyle(
            shape=RoundedRectangleBorder(radius=5),
            color={
                MaterialState.HOVERED: colors.WHITE70,
                MaterialState.DISABLED: colors.WHITE10,
                MaterialState.DEFAULT: colors.WHITE,
                MaterialState.SELECTED: colors.RED
            }
        )

        # UI Itens General
        self.main_container = Container()

        # Observer
        self.observers = []

        # Sound assets
        self.beep = Audio(
            src=r'assets\beep beep beep.mp3',
        )

        self.print_attributes()

    # Functions - Debug Tools

    # def verbose(self, observations=None, same_line=False):
    #     if self.debug:
    #         frame = inspect.currentframe()
    #         caller_frame = frame.f_back
    #         function_name = caller_frame.f_code.co_name

    #         verbose_text = f' -> {function_name} '
    #         if observations:
    #             verbose_text += f' | {observations}...'
    #         else:
    #             verbose_text += '...'

    #         if same_line:
    #             print(f'\r{verbose_text}', end='', )
    #             sys.stdout.flush()
    #         else:
    #             print(verbose_text)

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
        print(f"  Focus Counter: {self.cycle_data_storage}")

    # Functions - Threading
    def did_mount(self):
        verbose(self.debug,)
        self.th = threading.Thread(
            target=self.run_timer, args=(), daemon=True
        )
        self.th.start()
        verbose(self.debug, self.th)

    def will_unmount(self):
        verbose(self.debug,)
        self.is_running = False

    # Sound function
    def play_beep(self):
        self.beep.play()

    # Functions - Observer
    def register_observer(self, observer):
        verbose(self.debug,)
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        verbose(self.debug,)
        self.observers.remove(observer)

    def notify_observers(self):
        verbose(self.debug,)
        for observer in self.observers:
            observer.observer_update(self)
            observer.observer_update(self)

    # Functions - Settings

    def cycle_generator(self):
        verbose(self.debug, self.cycle_lenght)
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
                verbose(self.debug, 'Error: lenght > cycle_lenght')
        self.phase_cycle = phase_cycle
        verbose(self.debug, self.phase_cycle)

        return phase_cycle

    def reset_settings(self, e):
        verbose(self.debug,)
        self.focus_period_field.value = 30
        self.short_break_field.value = 10
        self.long_break_field.value = 20
        self.cycle_lenght_field.value = 4
        self.focus_period_field.update()
        self.short_break_field.update()
        self.long_break_field.update()
        self.cycle_lenght_field.update()
        self.validate_input(e)

    def reset_timer(self, full=False):
        verbose(self.debug,)

        if full == 'Yes':
            verbose(self.debug, full)
            self.current_phase = 0
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
        else:
            verbose(self.debug, full)
            verbose(self.debug, self.phase_cycle[self.current_phase])
            self.current_counter = self.phase_cycle[self.current_phase][1]

        self.update_timer_display()

        self.is_running = False
        self.start_stop_button.text = 'Start'
        self.start_stop_button.update()

    def apply_settings(self, args=None):
        verbose(self.debug,)

        self.focus_time = int(self.focus_period_field.value) * 60
        self.short_break_time = int(self.short_break_field.value) * 60
        self.long_break_time = int(self.long_break_field.value) * 60
        self.cycle_lenght = int(self.cycle_lenght_field.value)

        self.cycle_generator()
        self.reset_timer(full='Yes')
        self.update_button_states()

        self.settings_bottom_sheet.open = False
        self.settings_bottom_sheet.update()

        self.cycle_focus_position = 1
        self.module_name_phase_cycle.value = f'Pomodoro - {self.cycle_focus_position}/{self.cycle_lenght}'
        self.module_name_phase_cycle.update()

    def validate_input(self, e):
        verbose(self.debug,)

        def try_convert_to_int(item):
            try:
                return int(item)
            except:
                return False

        field_value_list = [
            self.focus_period_field.value,
            self.short_break_field.value,
            self.long_break_field.value,
            self.cycle_lenght_field.value
        ]
        all_integers = [try_convert_to_int(item) for item in field_value_list]

        verbose(self.debug, f'Items list -> {field_value_list}')
        verbose(self.debug, f'Check if all integers -> {all_integers}')

        if False in all_integers:
            verbose(self.debug, 'Invalid Input')
            self.page.banner.open = True
            self.apply_setting_button.disabled = True
            self.apply_setting_button.update()
            self.page.banner.update()
        else:
            verbose(self.debug, 'Valid Input')
            self.page.banner.open = False
            self.apply_setting_button.disabled = False
            self.apply_setting_button.update()
            self.page.banner.update()

    # Functions - Pomodoro Timer
    def start_stop_timer(self, e):
        verbose(self.debug, f'From: {self.is_running}')
        self.is_running = not self.is_running
        e.control.text = 'Stop' if self.is_running else 'Start'
        self.update()
        verbose(self.debug, f'To: {self.is_running}')

    def data_storage(self):
        verbose(self.debug, 'Starting data storage')
        timestamp = datetime.now()

        # Create a shallow copy of the current phase's data
        data_list = list(self.phase_cycle[self.current_phase])

        # Append the timestamp to the copied list
        data_list.append(timestamp)

        verbose(self.debug, f'Data to append -> {data_list}')

        # Append the modified copy to self.cycle_data_storage
        self.cycle_data_storage.append(data_list)

    def update_timer_display(self):
        # verbose(self.debug,
        #     f'Current counter -> {self.current_counter}', True)
        self.display_mins.value, self.display_secs.value = divmod(
            self.current_counter, 60)
        self.display_mins.value = f'{self.display_mins.value:02d}'
        self.display_secs.value = f'{self.display_secs.value:02d}'
        self.update()

    def run_timer(self):
        verbose(self.debug,)
        while self.update_ui:
            if self.is_running:
                if self.current_counter > 0:

                    self.current_counter -= 1
                else:
                    if self.phase_cycle[self.current_phase][0] == 'Focus':
                        verbose(self.debug,
                                f'Focus Period Complete! -> Current Focus Streak [{len(self.cycle_data_storage)}]')
                    self.switch_phase()
                self.update_timer_display()
            time.sleep(self.update_time())

    def update_button_states(self):
        verbose(self.debug,)
        focus_active = self.current_phase_name.value == 'Focus'
        short_break_active = self.current_phase_name.value == 'Short Break'
        long_break_active = self.current_phase_name.value == 'Long Break'

        self.set_focus_button.disabled = focus_active
        self.set_short_break_button.disabled = short_break_active
        self.set_long_break_button.disabled = long_break_active
        self.update()

    def switch_phase(self):
        verbose(self.debug,
                f'From: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')

        self.data_storage()
        self.notify_observers()
        self.data_storage()
        self.notify_observers()
        self.current_phase += 1

        if self.current_phase < len(self.phase_cycle):
            if self.phase_cycle[self.current_phase][0] == 'Focus':
                self.cycle_focus_position += 1

                self.module_name_phase_cycle.value = f'Pomodoro - {self.cycle_focus_position}/{self.cycle_lenght}'
                self.module_name_phase_cycle.update()

            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
            verbose(self.debug,
                    f'To: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')
        elif self.current_phase == len(self.phase_cycle):
            self.cycle_focus_position = 1
            self.current_phase = 0
            self.current_phase_name.value = self.phase_cycle[self.current_phase][0]
            self.current_counter = self.phase_cycle[self.current_phase][1]
            self.module_name_phase_cycle.value = f'Pomodoro - {self.cycle_focus_position}/{self.cycle_lenght}'
            self.module_name_phase_cycle.update()
            verbose(self.debug,
                    f'Restarting cycle to: {self.current_phase} - {self.phase_cycle[self.current_phase][0]}')
        self.update()
        self.update_button_states()
        self.play_beep()

    def set_phase_cycle(self, e):
        verbose(self.debug, f'Button clicked: {e.control.text}')
        # verbose(self.debug,
        #     f'Set current phase name from: {self.current_phase_name.value}')
        # verbose(self.debug,f'Set current counter from: {self.current_counter}')
        # verbose(self.debug,f'Set current phase from: {self.current_phase}')

        def set_phase(phase_name):
            verbose(self.debug, f'{phase_name}')
            for phase in self.phase_cycle:
                if phase[0] == phase_name:
                    self.current_phase_name.value = phase_name
                    self.current_counter = phase[1]
                    self.current_phase = self.phase_cycle.index(phase)
                    self.update_button_states()
                    self.update_timer_display()
                    self.is_running = False
                    self.start_stop_button.text = 'Start'
                    self.start_stop_button.update()

                    self.cycle_focus_position = 1
                    self.module_name_phase_cycle.value = f'Pomodoro - {self.cycle_focus_position}/{self.cycle_lenght}'
                    self.module_name_phase_cycle.update()
                    break
            # verbose(self.debug,
            #     f'Set current phase name to: {self.current_phase_name.value}')
            # verbose(self.debug,f'Set current counter to: {self.current_counter}')
            # verbose(self.debug,f'Set current phase to: {self.current_phase}')

        # Determine which button was clicked and set the phase accordingly
        if e.control.text == 'Focus':
            set_phase('Focus')
        elif e.control.text == 'Short Break':
            set_phase('Short Break')
        elif e.control.text == 'Long Break':
            set_phase('Long Break')
        else:
            verbose(self.debug, 'Unknown button clicked')

    # Functions - Build
    def SettingsDisplay(self):
        verbose(self.debug,)

        # Creating functions needed to interact
        def close_banner(e):
            verbose(self.debug,)
            self.page.banner.open = False
            self.page.update()

        # Creating close settings function
        def close_settings(e):
            verbose(self.debug,)
            self.settings_bottom_sheet.open = False
            self.settings_bottom_sheet.update()

        def close_settings_button_configs():
            verbose(self.debug,)
            self.close_settings_button.icon = icons.CLOSE
            self.close_settings_button.on_click = close_settings

        def apply_settings_buttons_config():
            verbose(self.debug,)
            self.apply_setting_button.on_click = self.apply_settings
            self.apply_setting_button.style = self.button_style

        def valdation_banner_config():
            verbose(self.debug,)
            self.validation_banner.content = Text(
                'Only use numbers in the settings field.',
                color=colors.BLACK)
            self.validation_banner.actions.append(
                TextButton("Ignore", on_click=close_banner, style=ButtonStyle(color=colors.RED)))
            self.validation_banner
            self.validation_banner.bgcolor = colors.AMBER_100
            self.validation_banner.leading = Icon(
                icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40)

        def settings_text_fields_config():
            verbose(self.debug,)
            self.focus_period_field.label = 'Focus Period'
            self.short_break_field.label = 'Short Break'
            self.long_break_field.label = 'Long Break'
            self.cycle_lenght_field.label = 'Focus before Long Break'

            self.focus_period_field.width = 325
            self.short_break_field.width = 325
            self.long_break_field.width = 325
            self.cycle_lenght_field.width = 325

            self.focus_period_field.on_change = self.validate_input
            self.short_break_field.on_change = self.validate_input
            self.long_break_field.on_change = self.validate_input
            self.cycle_lenght_field.on_change = self.validate_input

            self.reset_settings_button.on_click = self.reset_settings
            self.reset_settings_button.style = self.button_style

        def assemble_settings_container():
            verbose(self.debug,)

            settings_column = Column()
            close_settings_row = Row()
            settings_buttons_row = Row()
            settings_text = Text('Pomodoro Settings',
                                 theme_style=TextThemeStyle.LABEL_SMALL)

            # Settings column configuration
            settings_column.alignment = MainAxisAlignment.START
            settings_column.horizontal_alignment = CrossAxisAlignment.CENTER
            settings_column.tight = True
            settings_column.scroll = ScrollMode.ADAPTIVE
            settings_column.controls = [
                close_settings_row,
                self.focus_period_field,
                self.short_break_field,
                self.long_break_field,
                self.cycle_lenght_field,
                settings_buttons_row
            ]

            # Close settings row configuration
            close_settings_row.alignment = MainAxisAlignment.SPACE_BETWEEN
            close_settings_row.controls = [
                settings_text,
                self.close_settings_button
            ]
            close_settings_row.width = 325

            # Settings button row configurations
            settings_buttons_row.alignment = MainAxisAlignment.END
            settings_buttons_row.controls = [
                self.apply_setting_button,
                self.reset_settings_button
            ]
            settings_buttons_row.width = 325

            # Running assets configuration
            close_settings_button_configs()
            apply_settings_buttons_config()
            valdation_banner_config()
            settings_text_fields_config()

            # Settings container configuration
            self.settings_container.content = settings_column
            self.settings_container.padding = 20
            self.settings_container.width = 400
            # self.settings_container.padding = padding.only(right=40)

            self.settings_bottom_sheet.content = self.settings_container
            self.settings_bottom_sheet.maintain_bottom_view_insets_padding = True
            self.settings_bottom_sheet.use_safe_area = True
            self.settings_bottom_sheet.is_scroll_controlled = False
            # self.settings_bottom_sheet.elevation = 10000

            return self.settings_bottom_sheet

        return assemble_settings_container()

    def PomodoroDisplay(self):
        verbose(self.debug,)

        def show_settings(e):
            verbose(self.debug,)
            self.settings_bottom_sheet.open = True
            self.settings_bottom_sheet.update()

        def phase_buttons():
            verbose(self.debug,)
            self.set_focus_button.on_click = self.set_phase_cycle
            self.set_short_break_button.on_click = self.set_phase_cycle
            self.set_long_break_button.on_click = self.set_phase_cycle

            self.set_focus_button.style = self.button_style
            self.set_short_break_button.style = self.button_style
            self.set_long_break_button.style = self.button_style

            self.phase_buttons_container.controls.append(
                self.set_focus_button)
            self.phase_buttons_container.controls.append(
                self.set_short_break_button)
            self.phase_buttons_container.controls.append(
                self.set_long_break_button)

            self.phase_buttons_container.wrap = True
            self.phase_buttons_container.alignment = MainAxisAlignment.SPACE_EVENLY
            self.phase_buttons_container.horizontal_alignment = CrossAxisAlignment.CENTER

            return self.phase_buttons_container

        def timer_display():
            verbose(self.debug,)
            # Display Mins properties
            self.display_mins.theme_style = TextThemeStyle.DISPLAY_LARGE

            # Display Secs properties
            self.display_secs.theme_style = TextThemeStyle.DISPLAY_SMALL

            # Setting Start Stop btn function
            self.start_stop_button.on_click = self.start_stop_timer
            self.start_stop_button.style = self.button_style

            # Setting restart button
            self.restart_button.icon = icons.RESTART_ALT
            self.restart_button.on_click = self.reset_timer

            # Setting timer container properties
            self.timer_container.wrap = True
            self.timer_container.alignment = MainAxisAlignment.CENTER
            self.timer_container.vertical_alignment = CrossAxisAlignment.BASELINE

            # Adding controls
            self.timer_container.controls.append(self.display_mins)
            self.timer_container.controls.append(self.display_secs)

            column = Column(
                controls=[
                    self.timer_container,
                    self.start_stop_button,
                    self.reset_timer_settings_container
                ]
            )

            column.alignment = MainAxisAlignment.SPACE_EVENLY
            column.horizontal_alignment = CrossAxisAlignment.CENTER
            column.spacing = 150

            return column

        def final_timer_display():
            verbose(self.debug,)
            # Open Setting Button setup
            self.open_settings_button.on_click = show_settings

            self.phase_buttons_container.alignment = MainAxisAlignment.CENTER

            # Setting container properties
            self.final_timer_container.alignment = MainAxisAlignment.CENTER
            # self.final_timer_container.horizontal_alignment = CrossAxisAlignment.CENTER
            # self.final_timer_container.wrap = True

            self.reset_timer_settings_container.wrap = True
            # self.reset_timer_settings_container.controls.append(
            #     self.start_stop_button)
            self.reset_timer_settings_container.controls.append(
                self.restart_button)
            self.reset_timer_settings_container.controls.append(
                self.open_settings_button)

            # Adding Controls
            self.final_timer_container.controls.append(phase_buttons())
            self.final_timer_container.controls.append(timer_display())

            col = Column()

            self.module_name_phase_cycle.theme_style = TextThemeStyle.LABEL_SMALL
            self.module_name_phase_cycle.text_align = TextAlign.CENTER

            # Divider

            col.controls = [
                self.module_name_phase_cycle,
                Divider(height=2),
                self.final_timer_container
            ]
            col.horizontal_alignment = 'center'
            col.spacing = 15
            col.alignment = 'center'

            self.main_container.content = col

            self.main_container.alignment = alignment.center
            self.main_container.bgcolor = colors.BLACK54
            self.main_container.height = 230
            self.main_container.width = 300
            self.main_container.padding = 20
            self.main_container.border_radius = 30
            # self.main_container.blend_mode = BlendMode.PLUS

            return self.main_container

        return final_timer_display()

    def build(self):
        self.page.banner = self.validation_banner
        verbose(self.debug,)
        self.SettingsDisplay()
        self.page.overlay.append(self.settings_bottom_sheet)
        self.page.overlay.append(self.beep)

        return self.PomodoroDisplay()


def main(page: Page):
    page.title = 'Pomodoro Module'
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_height = 600
    page.window_width = 400
    # page.bgcolor = colors.WHITE

    print('\n\n\n\n__________Instatiating Pomodoro Module__________')
    pomodoro = PomodoroModule(page, debug=False)

    # page.add(PomodoroModule(page, debug=True))
    print('\n__________Adding module to page__________')
    page.add(pomodoro)


if __name__ == '__main__':
    app(target=main)
