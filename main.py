import flet as ft
import requests
import time

def fetch_word_list():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?number=25")
        return response.json()
    except Exception as e:
        print(f"Error fetching word list: {e}")
        return []

def main(page: ft.Page):
    page.title = 'Type Master'
    page.window.width = 700
    page.window.height = 600
    page.window.resizable = False
    page.theme = ft.Theme(color_scheme_seed=ft.colors.YELLOW_300)
    page.theme_mode = ft.ThemeMode.LIGHT
    
    title = ft.Text("Type Master", color=ft.colors.GREEN_800, size=40)
    words = fetch_word_list()
    words_text = " ".join(words)
    
    start_time = [None]
    status_text = ft.Text("", size=20, color=ft.colors.BLUE)
    current_index = [0]
    
    display_text = ft.Row(wrap=True, spacing=5)

    def update_display():
        spans = []
        for i, char in enumerate(words_text):
            if i == current_index[0]:
                spans.append(ft.Text(char, style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, color=ft.colors.BLUE), size=20))
            elif i < current_index[0]:
                spans.append(ft.Text(char, style=ft.TextStyle(color=ft.colors.GREEN), size=20))
            else:
                spans.append(ft.Text(char, style=ft.TextStyle(color=ft.colors.BLACK), size=20))
        display_text.controls = spans
        page.update()
    
    update_display()
    
    def check_typing(e):
        if start_time[0] is None:
            start_time[0] = time.time()
        typed_char = e.control.value[-1] if e.control.value else ""
        if typed_char == words_text[current_index[0]]:
            current_index[0] += 1
            if current_index[0] >= len(words_text):
                elapsed_time = round(time.time() - start_time[0], 2)
                status_text.value = f"Completed in {elapsed_time} seconds"
                page.update()
            update_display()
    
    def restart_test(e):
        nonlocal words, words_text
        words = fetch_word_list()
        words_text = " ".join(words)
        current_index[0] = 0
        status_text.value = ""
        start_time[0] = None
        input_field.value = ""
        update_display()
    
    input_field = ft.TextField(
        width=650,
        height=60,
        on_change=check_typing,
        text_size=20,
        color=ft.colors.BLACK,
        bgcolor=ft.colors.WHITE,
        cursor_color=ft.colors.BLACK
    )
    
    page.add(
        ft.Column(
            [
                title,
                ft.Container(height=30),
                ft.Container(content=display_text, width=650),
                input_field,
                status_text,
                ft.Row([
                    ft.TextButton(text="Try Again", icon=ft.icons.CACHED_SHARP, on_click=restart_test)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(main)

