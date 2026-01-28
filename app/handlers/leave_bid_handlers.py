from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.middlewares import Ban_check
from config import GROUP_ID
from app.database.models import User
from app.keyboards import *

router = Router()
router.message.middleware(Ban_check())

class Request(StatesGroup):
    bid = State()

    offer = State()


# отправка жалобы режим
async def status(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("current_step")

    if step == 1:
        await message.answer("<b>Шаг 1/3.</b> 📝Напишите адрес или ориентир проблемы (улицу, номер дома, подъезд, этаж и квартиру) или пропустите этот пункт:", parse_mode="HTML", reply_markup=step_kb(False))

    elif step == 2:
        await message.answer("<b>Шаг 2/3.</b> 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:", parse_mode="HTML", reply_markup=step_kb(False))
    
    elif step == 3:
        await message.answer("<b>Шаг 3/3.</b> 📛Напишите причину обращения в подробностях:", parse_mode="HTML", reply_markup=step_kb(True))

async def send_information(message: Message, state: FSMContext, bot: Bot):
    user = await User.filter(tg_id=message.from_user.id).first()
    data = await state.get_data()
    
    adress = data.get("adress")
    if not adress:
        adress = "Не указан"
    reason = data.get("reason")

    try:
        media_type = data.get("media_type")
    except:
        media_type = ""

    st = f"""⛔️<b>Поступила новая жалоба:</b>\n
    @{message.from_user.username}\n
    <b><i>Имя и Фамилия: {user.name}</i></b>\n
    <b><i>Номер телефона: {user.number}</i></b>\n
    <b><i>Адрес:</i></b> {adress}\n
    <b><i>Содержание:</i></b> {reason}"""

    if media_type:
        if media_type == "photo":
            sent_photo = data.get("photo")
            await bot.send_photo(chat_id=GROUP_ID, photo=sent_photo, caption=st, parse_mode="HTML")
        elif media_type == "video":
            sent_video = data.get("video")
            await bot.send_video(chat_id=GROUP_ID, video=sent_video, caption=st, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=GROUP_ID, text=st, parse_mode="HTML")
    
    await state.clear()



# старт
@router.message(F.text == "📛Оставить заявку")
async def leave_request(message: Message, state: FSMContext):
    await state.update_data(current_step=1)
    await message.answer("📛👇📛<i>Выберите категорию, по которой Вы хотите оставить заявку в УК:</i>", parse_mode="HTML", reply_markup=choice_category_request_kb)

@router.callback_query(F.data == "leave_bid")
async def leave_bid_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Request.bid)
    
    await cb.answer("Шаг 1")
    await status(cb.message, state)



#пропуск и возвращение
@router.callback_query(F.data == "back")
async def step_back(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data.get("current_step")

    step -= 1
    if step <= 0:
        await state.clear()
        await leave_request(cb.message, state)
        await cb.answer("Переход в меню категорий")
    elif step > 0:
        await state.update_data(current_step=step)
        await cb.answer("Возвращаемся на шаг назад")
        await status(cb.message, state)

@router.callback_query(F.data == "skip")
async def step_skip(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data.get("current_step")

    if step < 3:
        step += 1
        await state.update_data(current_step=step)
        await cb.answer("Пропускаем шаг")
        await status(cb.message, state)



# проверка на сообщения
@router.message(Request.bid, F.text)
async def text_steps(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    step = data.get("current_step")

    if step == 1:
        await state.update_data(adress=message.text)

        step += 1
        await state.update_data(current_step=step)

        await status(message, state)
    elif step == 3:
        await state.update_data(reason=message.text)

        await send_information(message, state, bot)
    elif step == 2:
        await message.answer("⛔️📛В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> в виде медиа-сообщения. <b><i>Попробуйте ещё раз:</i></b>", parse_mode="HTML")

@router.message(Request.bid, F.photo)
async def photo_step(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("current_step")

    if step == 2:
        if message.photo:
            await state.update_data(photo=message.photo[-1].file_id)
        else:
            await state.update_data(photo=message.video)
        await state.update_data(media_type=message.content_type)

        step += 1
        await state.update_data(current_step=step)

        await status(message, state)




# отправка предложения режим
@router.callback_query(F.data == "leave_offer")
async def leave_offer_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Категория предложения")
    await cb.message.answer("<b><i>💡Распишите Ваше предложение в подробностях: (Добавьте фотографию, если есть)</i></b>", parse_mode="HTML", reply_markup=step_kb(True))
    await state.set_state(Request.offer)

@router.message(Request.offer, F.photo)
async def leave_offer_photo(message: Message, state: FSMContext, bot: Bot):
    if message.caption:
        user = await User.filter(tg_id=message.from_user.id).first()
        await bot.send_photo(chat_id=GROUP_ID, photo=message.photo[-1].file_id, caption=f"<b>💡Поступило новое предложение:</b>\n{message.from_user.username}\n<b><i>Имя и Фамилия: </i></b>{user.name}\n<b><i>Номер телефона: </i></b>{user.number}\n<b><i>Содержание: </i></b>{message.caption}", parse_mode="HTML")
        await state.clear()
    else:
        await message.answer("⛔️📛Предложение должно содержать только текст")

@router.message(Request.offer, F.text)
async def leave_offer_get(message: Message, state: FSMContext, bot: Bot):
    user = await User.filter(tg_id=message.from_user.id).first()
    await bot.send_message(chat_id=GROUP_ID, text=f"<b>💡Поступило новое предложение:</b>\n{message.from_user.username}\n<b><i>Имя и Фамилия: </i></b>{user.name}\n<b><i>Номер телефона: </i></b>{user.number}\n<b><i>Содержание: </i></b>{message.text}", parse_mode="HTML")
    await state.clear()