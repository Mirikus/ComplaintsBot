from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.middlewares import Ban_check
from config import GROUP_ID
from app.database.models import User
from app.keyboards import *
from app.handlers.start_handlers import main_menu

router = Router()
router.message.middleware(Ban_check())


class Call(StatesGroup):
    get_number = State()
    chat = State()

async def send_information_user(cb: CallbackQuery, bot: Bot):
    user = await User.filter(tg_id=cb.from_user.id).first()
    if cb.from_user.username:
        name = "@" + f"{cb.from_user.username}"
    else:
        name = "нет"
    await bot.send_message(chat_id=GROUP_ID, text=f"<b>От пользователя {cb.from_user.id}\nИмя: {user.name}\nТелефон: {user.number}\nНикнейм: {name}</b>", parse_mode="HTML")


@router.message(F.text == "📞Связаться")
async def call_start(message: Message):
    await message.answer("👇<i>Выберите способ связи из нижеперечисленного списка:</i>", parse_mode="HTML", reply_markup=call_kb)

@router.callback_query(F.data == "call_me")
async def contact_me(cb: CallbackQuery,):
    user = await User.get_or_none(tg_id=cb.from_user.id)
    await cb.answer("Выбор действия")
    await cb.message.answer(f"<b>Это Ваш верный номер телефона</b> {user.number}? <i>Если да, нажмите соответствующую кнопку<b>, если нет,</b></i> впишите свой актуальный номер телефона здесь", parse_mode="HTML", reply_markup=call_me_kb)
    

@router.callback_query(F.data == "chat_me")
async def chat_me(cb: CallbackQuery, state: FSMContext, bot: Bot):
    await cb.answer("Режим чаттинга")
    await cb.message.answer('✅📞✅Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ", готов помочь Вам. Напишите, пожалуйста, интересующий Вас вопрос и ожидайте нашего ответа', reply_markup=chat_me_kb)
    await send_information_user(cb, bot)
    await state.set_state(Call.chat)




@router.callback_query(F.data == "recall")
async def call_me(cb: CallbackQuery, bot: Bot):
    user = await User.filter(tg_id=cb.from_user.id).first()
    await bot.send_message(chat_id=GROUP_ID, text=f"<b>Нужно перезвонить пользователю: {user.number}</b>\n{cb.from_user.username}\n{user.name}", parse_mode="HTML")
    await cb.answer("Пользователь найден")
    await cb.message.answer("<b>✅Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время.", parse_mode="HTML")

@router.callback_query(F.data == "one_number")
async def back_call_categoty(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Режим смены номера")
    await state.set_state(Call.get_number)

@router.message(Call.get_number, F.text)
async def remember_st(message: Message, state: FSMContext, bot: Bot):
    violation = False
    if not (len(message.text) == 12 and message.text[0] == "+" and message.text[1:].isdigit()):
        violation = True

    if violation:
        await message.answer("⛔️📛⛔️<b>Номер телефона</b> должен содержать 11 цифр и должен обязательно содержать в начале <b>+7. Учтите формат и попробуйте снова:</b>", parse_mode="HTML")
    else:
        user = await User.get(tg_id=message.from_user.id)
        await bot.send_message(chat_id=GROUP_ID, text=f"<b>Нужно перезвонить пользователю: {message.text}</b>\n{message.from_user.username}\n{user.name}", parse_mode="HTML")
        await state.clear()
        await message.answer("<b>✅Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время.", parse_mode="HTML")



@router.callback_query(F.data == "end_chat")
async def end_chat(cb: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await cb.answer("Конец диалога")
    await cb.message.answer("<b>❌📞Диалог с администратором завершён...</b>", parse_mode="HTML")

    if cb.from_user.username:
        name = "@" + f"{cb.from_user.username}"
    else:
        name = "нет"
    await bot.send_message(chat_id=GROUP_ID, text=f"Пользователь {name} <b>закончил диалог</b>\nID {cb.from_user.id}", parse_mode="HTML")

    await main_menu(cb.message)

@router.message(F.reply_to_message)
async def admin_reply(message: Message):
    st = message.reply_to_message.text.split(" ")
    user = await User.get(tg_id=st[-1])
    await message.send_copy(chat_id=user.tg_id)

@router.message(Call.chat)
async def send_message_chat(message: Message, bot: Bot):
    if message.from_user.username:
        name = "@" + f"{message.from_user.username}"
    else:
        name = "нет"
    await bot.send_message(chat_id=GROUP_ID, text=f"{name}: {message.text}\nID {message.from_user.id}")