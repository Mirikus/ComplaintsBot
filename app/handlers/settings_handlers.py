from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re

from app.middlewares import Ban_check
from app.database.models import User
from app.keyboards import *

router = Router()
router.message.middleware(Ban_check())

class Setting(StatesGroup):
    name = State()
    number = State()

CYRILLIC_PATTERN = re.compile(r"^[а-яёА-ЯЁ\s]+$")

@router.message(F.text == "⚙️Настройки")
async def settings(message: Message):
    await message.answer("⚙️Тут Вы сможете поменять <b>Имя</b> и <b>Фамилию</b> в Базе данных нашего бота или же можете поменять Ваш <b>номер телефона</b>, если Вы изначально вводили что-то неверно. Выберите, что хотите поменять или вернитесь назад в <b>главное меню:</b>", parse_mode="HTML", reply_markup=settings_kb)



@router.callback_query(F.data == "change_name")
async def change_name(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Меняем имя")
    await cb.message.answer("<i>🛠Отправьте своё Имя и Фамилию, чтобы поменять настройки:</i>", parse_mode="HTML")
    await state.set_state(Setting.name)

@router.message(Setting.name)
async def get_new_name(message: Message, state: FSMContext):
    violation = False
    if message.text:
        list_words = message.text.split(" ")

        if not (len(list_words) == 2 and CYRILLIC_PATTERN.fullmatch(message.text)):
            violation = True

        for word in list_words:
            if not word[0].isupper():
                violation = True
    else:
        violation = True

    if violation:
        await message.answer("⛔️📛<b>Имя</b> и <b>Фамилия</b> должны быть введены через один <i>пробел</i>, и должны быть написаны через <i>кириллицу</i>. Также должны быть <i>заглавные буквы</i>. <b>Учтите формат и попробуйте снова:</b>", parse_mode="HTML")
    else:
        user = await User.get(tg_id=message.from_user.id)
        user.name = message.text
        await user.save()
        await state.clear()

        await message.answer("🛠✅🛠Настройки <b>имени</b> успешно применены!", parse_mode="HTML")


@router.callback_query(F.data == "change_number")
async def change_number(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Меняем номер")
    await cb.message.answer("<i>🛠Отправьте свой номер телефона, чтобы поменять настройки:</i>", parse_mode="HTML")
    await state.set_state(Setting.number)

@router.message(Setting.number)
async def get_new_number(message: Message, state: FSMContext):
    violation = False
    if message.text:
        if not (len(message.text) == 12 and message.text[0] == "+" and message.text[1:].isdigit()):
            violation = True
    else:
        violation = True

    if violation:
        await message.answer("⛔️📛⛔️<b>Номер телефона</b> должен содержать 11 цифр и должен обязательно содержать в начале <b>+7. Учтите формат и попробуйте снова:</b>", parse_mode="HTML")
    else:
        user = await User.get(tg_id=message.from_user.id)
        user.number = message.text
        await user.save()
        await state.clear()

        await message.answer("🛠✅🛠Настройки <b>номера</b> успешно применены!", parse_mode="HTML")