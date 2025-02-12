import flet as ft 
import requests

def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
        word = response.json()[0]
        return word
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_word_list():
    try:
        words = []
        response = requests.get("https://random-word-api.herokuapp.com/all")
        words = [word for word in response.json() if len(word) == 5]
        return words
    except Exception as e:
        print(f"Error fetching word list: {e}")
        return []

def main(page: ft.Page):
    page.title = 'Loading'
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False
    
    rows = [
        [ft.TextField(text_align=ft.TextAlign.CENTER, width=50, max_length=1, fill_color=ft.colors.YELLOW_50, 
        visible = False, color=ft.colors.BLACK, disabled=True,) for i in range(5)]for i in range(5)
    ]
    
    button = ft.ElevatedButton(text="Check", width=200, disabled=True, visible = False)
    reset = ft.ElevatedButton(text="Reset", width=90, visible = False)
    job = ft.Text("", visible = False)
    loading = ft.ProgressRing(width=300, height=300, stroke_width=4)
    title = ft.Text("WORDLE", color=ft.colors.GREEN_800, size=30, visible = False)

    current_index = 0
    row = 0

    def change_row():
        nonlocal row, current_index
        rows[row][current_index].focus()
        if row > 0:
            for square in rows[row - 1]:
                square.disabled = True
        current_index = 0
        if row < len(rows):
            for square in rows[row]:
                square.disabled = False
                square.on_change = lambda e, i=square: handle_input(e, rows[row], i)
        page.update()

    def validate():
        guessed_word = ''.join([square.value for square in rows[row]]).lower() # type: ignore
        button.disabled = not (len(guessed_word) == 5 and guessed_word in words)
        page.update()

    def check(e):
        button.disabled = True
        nonlocal row
        guessed_word = ''.join([square.value for square in rows[row]]).lower() # type: ignore
        if guessed_word == word:
            job.value = "Correct!"
            for square in rows[row]:
                square.fill_color = ft.colors.GREEN
        else:
            job.value = "Incorrect!"
            for i, square in enumerate(rows[row]):
                if guessed_word[i] == word[i]: # type: ignore
                    square.fill_color = ft.colors.GREEN
                elif guessed_word[i] in word:
                    square.fill_color = ft.colors.YELLOW
            row += 1
            if (row == 5):
                job.value = "The word was: " + word # type: ignore
            if row < len(rows):
                change_row()
        page.update()



    def handle_input(e, current_row, current_square):
        nonlocal current_index
        if len(current_square.value) == 1:
            current_index = current_row.index(current_square)
            if current_index < len(current_row) - 1:
                current_row[current_index + 1].focus()
        validate()
        page.update()



    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal current_index
        if e.key == "Enter" and not button.disabled:
            current_index = 0
            for square in rows[row]:
                square.disabled = False
            check(e)
        if e.key == "Backspace":
            print(current_index)
            if current_index > 0 :
                rows[row][current_index].value = ""
                current_index = current_index - 1
                rows[row][current_index].focus()
            page.update()
        if e.key == '1':
            rows[row][current_index].focus()

    def resets(e):
        nonlocal word, row, current_index
        current_index = 0
        word = get_random_word()
        print(word)
        row = 0 

        for i, row_list in enumerate(rows):
            for square in row_list:
                square.value = ""
                square.disabled = True if i != 0 else False
                square.fill_color = ft.colors.YELLOW_50
        
        job.value = ""
        button.disabled = True
        rows[row][current_index].focus()
        page.update()

    reset.on_click = resets
    button.on_click = check
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Column(
            [
                ft.Row(
                    [   
                        ft.Container(width=90),
                        title,
                        reset
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Row(rows[0], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(rows[1], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                loading,
                ft.Row(rows[2], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(rows[3], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(rows[4], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                button,
                job
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    words = fetch_word_list()
    word = get_random_word()
    print(word)
    for row_list in rows:
        for square in row_list:
            square.visible = True
    loading.visible = False
    button.visible = True
    reset.visible = True
    title.visible = True
    job.visible = True
    page.title = 'Wordle'
    
    page.theme = ft.Theme(color_scheme_seed=ft.colors.YELLOW_300)
    for square in rows[row]:
        square.disabled = False
    change_row()

ft.app(main)