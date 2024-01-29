from flet import *


class TasksModule():
    def __init__(self):
        print('\n___Starting Tasks Module__________________________')
        super().__init__()

    def build(self):
        pass


def main(page: Page):
    page.title = 'Tasks'
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    # page.bgcolor = colors.WHITE

    print('\n\n\n\n__________Instatiating Tasks__________')

    # page.add(PomodoroModule(page, debug=True))
    print('\n__________Adding tasks__________')
    page.add()


if __name__ == '__main__':
    app(target=main)
