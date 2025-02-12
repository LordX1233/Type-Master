import flet as ft 
import requests
import random

def fetch_word_list():
    try:
        words = []
        response = requests.get("https://random-word-api.herokuapp.com/word?number=30")
        words = [word for word in response.json()]
        return words
    except Exception as e:
        print(f"Error fetching word list: {e}")
        return []

def main(page: ft.Page):
    page.title = 'Type Master'
    page.window.width = 700
    page.window.height = 600
    page.window.resizable = False
    
    # rows = [
    #     [ft.TextField(text_align=ft.TextAlign.CENTER, width=50, max_length=1, fill_color=ft.colors.YELLOW_50, 
    #     visible = False, color=ft.colors.BLACK, disabled=True,) for i in range(5)]for i in range(5)
    # ]
    
    # button = ft.ElevatedButton(text="Check", width=200, disabled=True, visible = False)
    # reset = ft.ElevatedButton(text="Reset", width=90, visible = False)
    # job = ft.Text("", visible = False)
    # loading = ft.ProgressRing(width=300, height=300, stroke_width=4)
    # title = ft.Text("WORDLE", color=ft.colors.GREEN_800, size=30, visible = False)

    # current_index = 0
    # row = 0

    # def change_row():
    #     nonlocal row, current_index
    #     rows[row][current_index].focus()
    #     if row > 0:
    #         for square in rows[row - 1]:
    #             square.disabled = True
    #     current_index = 0
    #     if row < len(rows):
    #         for square in rows[row]:
    #             square.disabled = False
    #             square.on_change = lambda e, i=square: handle_input(e, rows[row], i)
    #     page.update()

    # def validate():
    #     guessed_word = ''.join([square.value for square in rows[row]]).lower() # type: ignore
    #     button.disabled = not (len(guessed_word) == 5 and guessed_word in words)
    #     page.update()

    # def check(e):
    #     button.disabled = True
    #     nonlocal row
    #     guessed_word = ''.join([square.value for square in rows[row]]).lower() # type: ignore
    #     if guessed_word == word:
    #         job.value = "Correct!"
    #         for square in rows[row]:
    #             square.fill_color = ft.colors.GREEN
    #     else:
    #         job.value = "Incorrect!"
    #         for i, square in enumerate(rows[row]):
    #             if guessed_word[i] == word[i]: # type: ignore
    #                 square.fill_color = ft.colors.GREEN
    #             elif guessed_word[i] in word:
    #                 square.fill_color = ft.colors.YELLOW
    #         row += 1
    #         if (row == 5):
    #             job.value = "The word was: " + word # type: ignore
    #         if row < len(rows):
    #             change_row()
    #     page.update()



    # def handle_input(e, current_row, current_square):
    #     nonlocal current_index
    #     if len(current_square.value) == 1:
    #         current_index = current_row.index(current_square)
    #         if current_index < len(current_row) - 1:
    #             current_row[current_index + 1].focus()
    #     validate()
    #     page.update()



    # def on_keyboard(e: ft.KeyboardEvent):
    #     nonlocal current_index
    #     if e.key == "Enter" and not button.disabled:
    #         current_index = 0
    #         for square in rows[row]:
    #             square.disabled = False
    #         check(e)
    #     if e.key == "Backspace":
    #         print(current_index)
    #         if current_index > 0 :
    #             rows[row][current_index].value = ""
    #             current_index = current_index - 1
    #             rows[row][current_index].focus()
    #         page.update()
    #     if e.key == '1':
    #         rows[row][current_index].focus()

    # def resets(e):
    #     nonlocal word, row, current_index
    #     current_index = 0
    #     word = get_random_word()
    #     print(word)
    #     row = 0 

    #     for i, row_list in enumerate(rows):
    #         for square in row_list:
    #             square.value = ""
    #             square.disabled = True if i != 0 else False
    #             square.fill_color = ft.colors.YELLOW_50
    #     job.value = ""
    #     button.disabled = True
    #     rows[row][current_index].focus()
    #     page.update()

    # reset.on_click = resets
    # button.on_click = check
    # page.on_keyboard_event = on_keyboard
        

    def shuffle_words(e):
        words = fetch_word_list()
        print(words)
        page.update()

    words = fetch_word_list()
    print(words)
    
    page.add(
        ft.Column(
            [   
                ft.Text("  ".join(words), size=25),
                ft.Row(
                    [      
                        ft.TextButton(text="Try Again", icon=ft.icons.CACHED_SHARP, on_click=shuffle_words)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(main)