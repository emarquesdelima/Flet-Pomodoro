import flet
from flet import IconButton, Page, Row, TextField, icons


def main(page: Page):
    page.title = 'Counter'
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    txt_header = flet.Text(
        'Counter',
        size=20,
        text_align='center',
        style=flet.TextThemeStyle.DISPLAY_MEDIUM,
    )

    txt_number = TextField(
        value='0',
        text_align='right',
        width=100
    )

    def minus_click(e):
        print(f'Counter from -> {txt_number.value}')
        txt_number.value = int(txt_number.value) - 1
        print(f'To -> {txt_number.value}')
        page.update()

    def plus_click(e):
        print(f'Counter from -> {txt_number.value}')
        txt_number.value = int(txt_number.value) + 1
        print(f'To -> {txt_number.value}')
        page.update()

    page.add(
        txt_header,
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click)
            ],
            alignment='center',
        )
    )


flet.app(target=main)
