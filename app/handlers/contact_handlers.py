from aiogram import F, Router
from aiogram.types import Message

from app.middlewares import Ban_check
from app.keyboards import *

router = Router()
router.message.middleware(Ban_check())

@router.message(F.text == "☎️Полезные контакты")
async def contact_information(message: Message):
    await message.answer("<u>Управляющая компания:</u>\n<b>Диспетчерская служба  ООО «УЭР-ЮГ»</b>\n+7 4722 35-50-06\n<b>Инженеры ООО «УЭР-ЮГ»</b>\n+7 920 566-28-86\n<b>Бухгалтерия ООО «УЭР-ЮГ»</b>\n+7 4722 35-50-06\n<i>Белгород, Свято-Троицкий б-р, д. 15, подъезд No 1</i>\n\n<u>Телефоны для открытия ворот и шлагбаума:</u> \n<b>Шлагбаум «Набережная»</b>\n+7 920 554-87-74\n<b>Ворота «Харьковские»</b>\n+7920 554-87-40\n<b>Ворота «Мост»</b>\n+7 920 554-64-06\n<b>Калитка 1 «Мост»</b>\n+7 920 554-42-10\n<b>Калитка 2 «Мост»</b>\n+7 920 554-89-04\n<b>Калитка 3 «Харьковская»</b>\n+7 920 554-87-39\n<b>Калитка 4 «Харьковская»</b>\n+7 920 554-89-02\n\n<b>Охрана</b>\n+7 915 57-91-457\n\n<b>Участковый</b>\nКуленцова Марина Владимировна\n+7 999 421-53-72", parse_mode="HTML")
