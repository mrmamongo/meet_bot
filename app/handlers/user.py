from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.filters import RoleFilter
from app.keyboards.row_keyboard import row_keyboard
from app.models.base import session as s
from app.models.user import User, UserRole
from app.states.form import Form

router = Router()
router.message.filter(
    RoleFilter(role=UserRole.USER, session=s()),
)


@router.message(F.text.in_(['Отмена']))
async def form_quit(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Ну лады, пока"
    )
    await state.clear()


@router.message(Command(commands=['start']))
async def form_start(message: Message, state: FSMContext, session: Session) -> None:
    user = session.execute(select(User).where(User.id == message.from_user.id)).one_or_none()
    if user:
        await message.answer(
            text=f"С возвращением, {message.from_user.first_name if message.from_user.first_name != '' else message.from_user.username}!\n "
        )
        await state.clear()
    else:
        await message.answer(
            text="Привет! Давай для начала создадим твой профиль\n"
                 "Для начала давай сюда свою фоточку",
            reply_markup=row_keyboard(["quit"])
        )
        await state.set_state(Form.avatar_enter)


@router.message(Form.avatar_enter, content_types=['photo'])
async def form_avatar_enter(message: Message, state: FSMContext) -> None:
    await state.update_data(avatar=message.photo[-1].file_id)
    await message.answer(
        text="Теперь давай сюда свое имя",
        reply_markup=row_keyboard(["quit"])
    )
    await state.set_state(Form.name_enter)


@router.message(Form.name_enter)
async def form_name_enter(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        text="Теперь давай сюда свой возраст",
        reply_markup=row_keyboard(["quit"])
    )
    await state.set_state(Form.age_enter)


async def form_age_enter(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer(
        text="Теперь давай сюда свое описание",
        reply_markup=row_keyboard(["quit"])
    )
    await state.set_state(Form.description_enter)


@router.message(Form.description_enter)
async def form_description_enter(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await message.answer(
        text="Теперь давай сюда свое местоположение",
        reply_markup=row_keyboard(["quit"])
    )
    await state.set_state(Form.location_enter)


@router.message(Form.location_enter)
async def form_location_enter(message: Message, state: FSMContext) -> None:
    await state.update_data(location=message.location.json())
    user_data = await state.get_data()

    await message.answer(
        text=f"Вот что ты ввел:\n"
             f"Фото: {user_data['avatar']}\n"
             f"Имя: {user_data['name']}\n"
             f"Возраст: {user_data['age']}\n"
             f"Описание: {user_data['description']}\n"
             f"Местоположение: {user_data['location']}\n"
             "Если все верно, то нажми на кнопку \"Готово\"",
        reply_markup=row_keyboard(["Готово", "Отмена"])
    )
    await state.set_state(Form.confirm)


@router.message(Form.confirm)
async def form_done(message: Message, state: FSMContext, session: Session) -> None:
    user_data = await state.get_data()
    user = User(
        id=message.from_user.id,
        avatar=user_data['avatar'],
        name=user_data['name'],
        age=user_data['age'],
        description=user_data['description'],
        location=user_data['location']
    )
    session.add(user)
    session.commit()

    await message.answer(
        text="Все готово! Теперь ты можешь пользоваться ботом"
    )
    await state.clear()


@router.message(Command(commands=['poll']))
async def poll(message: Message, session: Session):
    user = session.execute(select(User).where(User.id == message.from_user.id)).one_or_none()
    if user:
        await message.answer(
            text=f"С возвращением, {message.from_user.first_name if message.from_user.first_name != '' else message.from_user.username}!\n "
                 f""
        )


@router.message(Command(commands=['upgrade']))
async def upgrade_subscription(message: Message):
    await message.answer(
        text="Для того, чтобы подписаться на платную подписку, нажми на кнопку ниже",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подписаться",
                        url="https://t.me/storebot?start=bot_name"
                    )
                ]
            ]
        )
    )
