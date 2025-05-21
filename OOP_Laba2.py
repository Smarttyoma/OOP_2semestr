import json
import sys
from enum import Enum
from typing import Tuple

class AnsiColor(Enum):
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37
    DEFAULT = 0

class AsciiArtRenderer:
    _char_map = {}
    _font_loaded = False

    @classmethod
    def _init_font(cls, font_file: str = 'text1.txt') -> None:
        if cls._font_loaded:
            return
        try:
            with open(font_file, 'r', encoding='utf-8') as file:
                cls._char_map = json.load(file)
        except Exception as error:
            sys.stderr.write(f"Не удалось загрузить шрифт: {error}\n")
            cls._char_map = {}
        cls._font_loaded = True

    @staticmethod
    def render_text(text: str, color: AnsiColor, offset: Tuple[int, int]) -> None:
        AsciiArtRenderer._init_font()
        row_start, col_start = offset

        if not AsciiArtRenderer._char_map:
            return

        sample_letter = next(iter(AsciiArtRenderer._char_map.values()))
        char_height = len(sample_letter)
        char_width = len(sample_letter[0])

        output_rows = ['' for _ in range(char_height)]

        for symbol in text.upper():
            pattern = AsciiArtRenderer._char_map.get(symbol, [' ' * char_width] * char_height)
            for i in range(char_height):
                line = ''.join('*' if pixel != ' ' else ' ' for pixel in pattern[i])
                output_rows[i] += line + ' '

        # Очистить экран и установить курсор в начало
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        # Вертикальный отступ
        sys.stdout.write('\n' * (row_start - 1))

        # Печать строк с горизонтальным отступом и цветом
        for row in output_rows:
            sys.stdout.write(' ' * (col_start - 1))
            sys.stdout.write(f"\033[{color.value}m{row}\033[{AnsiColor.DEFAULT.value}m\n")

        sys.stdout.flush()

    def __init__(self, color: AnsiColor, position: Tuple[int, int]):
        AsciiArtRenderer._init_font()
        self._color = color
        self._row_offset, self._col_offset = position

    def draw(self, message: str) -> None:
        AsciiArtRenderer.render_text(message, self._color, (self._row_offset, self._col_offset))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write(f"\033[{AnsiColor.DEFAULT.value}m\n")
        sys.stdout.flush()

if __name__ == '__main__':
    user_text = input("Введите слово: ").strip()
    print("Выберите цвет текста:")
    for color_option in AnsiColor:
        if color_option != AnsiColor.DEFAULT:
            print(f"{color_option.name.title()}")

    chosen_color = input("Цвет: ").strip().upper()
    selected_color = AnsiColor.__members__.get(chosen_color, AnsiColor.WHITE)

    with AsciiArtRenderer(selected_color, (5, 5)) as renderer:
        renderer.draw(user_text)
