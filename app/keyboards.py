from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types

main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📛Оставить заявку"), KeyboardButton(text="📞Связаться")],
                                        [KeyboardButton(text="⚙️Настройки")],
                                        [KeyboardButton(text="☎️Полезные контакты")]],
                            resize_keyboard=True)





choice_category_request_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📛Оставить заявку", callback_data="leave_bid"), InlineKeyboardButton(text="💡Поделиться предложением", callback_data="leave_offer")], 
                                                               [InlineKeyboardButton(text="🔙Назад", callback_data="tomain")]])

def step_kb(hide: bool):
    builder = InlineKeyboardBuilder()
    if hide:
        builder.row(types.InlineKeyboardButton(text="🔙Назад", callback_data="back"))
    else:
        builder.row(types.InlineKeyboardButton(text="▶️Пропустить", callback_data="skip"))
        builder.row(types.InlineKeyboardButton(text="🔙Назад", callback_data="back"))
    return builder.as_markup()




call_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📞Перезвоните мне", callback_data="call_me")],
                                                [InlineKeyboardButton(text="📞Свяжитесь со мной в чат-боте", callback_data="chat_me")],
                                                [InlineKeyboardButton(text="🔙Назад", callback_data="tomain")]])

call_me_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅Да", callback_data="recall"), InlineKeyboardButton(text="🔙Оставить номер телефона", callback_data="back_call_category")]])

chat_me_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌📞Завершить диалог", callback_data="end_chat")]])




settings_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛠Поменять имя", callback_data="change_name"), InlineKeyboardButton(text="🛠Сменить номер", callback_data="change_number")],
                                                    [InlineKeyboardButton(text="🔙Назад", callback_data="tomain")]])





admin_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Инфо", callback_data="info")],
                                                 [InlineKeyboardButton(text="Блокировка", callback_data="block")],
                                                 [InlineKeyboardButton(text="Рассылка", callback_data="broadcast")]])