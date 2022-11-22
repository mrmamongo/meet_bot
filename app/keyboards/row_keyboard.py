from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def row_keyboard(items: list[str], resize: bool = True, one_time: bool = True) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[row], one_time_keyboard=True)
