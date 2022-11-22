from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    avatar_enter = State()
    name_enter = State()
    age_enter = State()
    description_enter = State()
    location_enter = State()
    confirm = State()
    done = State()
