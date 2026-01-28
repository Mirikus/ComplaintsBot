from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re

from app.middlewares import Ban_check
from app.database.models import User
from app.keyboards import *

router = Router()
router.message.middleware(Ban_check())

class Reg(StatesGroup):
    name = State()
    number = State()

CYRILLIC_PATTERN = re.compile(r"^[а-яёА-ЯЁ\s]+$")

async def main_menu(message: Message):
    await message.answer('✈️<b>Добро пожаловать</b> <i>в главное меню чат-бота Управляющей компании "УЭР-ЮГ".</i> Здесь Вы можете оставить заявку для управляющей компании или направить свое предложение по управлению домом. Просто воспользуйтесь кнопками <b>меню</b>, чтобы взаимодействовать с функциями бота:', parse_mode="HTML", reply_markup=main_kb)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await User.get_or_none(tg_id=message.from_user.id):
        await main_menu(message)
    else:
        await message.answer(f"☀️<b>Доброго времени суток</b>, бот создан, чтобы обрабатывать заявки и обращения пользователей. Чтобы воспользоваться этим, пришлите для начала Ваше <b>Имя</b> и <b>Фамилию</b>", parse_mode="HTML")
        await state.set_state(Reg.name)

@router.message(Reg.name)
async def get_name(message: Message, state: FSMContext):
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
        await message.answer("📞Теперь отправьте Ваш <b>номер телефона</b> через <b>+7</b> следующим сообщением:", parse_mode="HTML")
        await state.update_data(name=message.text)
        await state.set_state(Reg.number)

@router.message(Reg.number)
async def get_number(message: Message, state: FSMContext):
    violation = False

    if message.text:
        if not (len(message.text) == 12 and message.text[0] == "+" and message.text[1:].isdigit()):
            violation = True
    else:
        violation = True
    
    if violation:
        await message.answer("⛔️📛⛔️<b>Номер телефона</b> должен содержать 11 цифр и должен обязательно содержать в начале <b>+7. Учтите формат и попробуйте снова:</b>", parse_mode="HTML")
    else:
        user_data = await state.get_data()
        if message.from_user.username:
            await User.create(tg_id=message.from_user.id, name=user_data.get("name"), number=message.text, username=message.from_user.username)
        else:
            await User.create(tg_id=message.from_user.id, name=user_data.get("name"), number=message.text)
        
        await state.clear()
        await main_menu(message)

@router.callback_query(F.data == "tomain")
async def back_main_menu(cb: CallbackQuery):
    await cb.answer("Переход в главное меню...")
    await main_menu(cb.message)