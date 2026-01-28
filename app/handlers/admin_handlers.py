from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from config import GROUP_ID
from app.database.models import User
from app.keyboards import *

router = Router()

class Admin(StatesGroup):
    info = State()
    block = State()
    broadcast = State()


@router.message(F.chat.id == int(GROUP_ID), Command("admin"))
async def test_handler(message: Message):
    await message.answer("Выберите действие:", reply_markup=admin_kb)


@router.callback_query(F.data == "info")
async def info_user(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.info)
    await cb.answer("Режим информации")
    await cb.message.answer("Введите никнейм или ID пользователя для просмотра информации")

@router.message(Admin.info)
async def search_info(message: Message, state: FSMContext):
    if message.text.isdigit():
        user = await User.get(tg_id=message.text)
        if user.username:
            name = "@" + f"{user.username}"
        else:
            name = "нет"
    else:
        user = await User.get(username=message.text[1:])
        name = message.text
    
    if user.block:
        status = "Пользователь заблокирован"
    else:
        status = "Пользователь разблокирован"

    await message.answer(f"ID: {user.tg_id}\nНикнейм: {name}\nИмя и Фамилия: {user.name}\nТелефон: {user.number}\n{status}")
    await state.clear()


@router.callback_query(F.data == "block")
async def block_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.block)
    await cb.answer("Режим блокировки")
    await cb.message.answer("Введите никнейм или ID пользователя для блокировки, повторно вызовите команду для разблокировки")

@router.message(Admin.block)
async def block_user(message: Message, state: FSMContext):
    if message.text.isdigit():
        user = await User.get(tg_id=message.text)
        if user.username:
            name = "@" + f"{user.username}"
        else:
            name = user.tg_id
    else:
        user = await User.get(username=message.text[1:])
        name = message.text
    if not user.block:
        user.block = True
        await message.answer(f"Пользователь {name} заблокирован")
    else:
        user.block = False
        await message.answer(f"Пользователь {name} разблокирован")
    await user.save()
    await state.clear()


@router.callback_query(F.data == "broadcast")
async def broadcast_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.broadcast)
    await cb.answer("Режи рассылки")
    await cb.message.answer("Введите сообщение для рассылки среди всех не заблокированных пользователей:")

@router.message(Admin.broadcast)
async def broadcast_users(message: Message, state: FSMContext):
    users = await User.filter(block=False).values_list("tg_id", flat=True)
    print(users)
    count = 0

    for user in users:
        try:
            await message.send_copy(chat_id=user)
            count += 1
        except:
            pass
    await message.answer(f"{count} пользователей получило ваше сообщение")

    await state.clear()