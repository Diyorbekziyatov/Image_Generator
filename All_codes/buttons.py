from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


diyorbek = InlineKeyboardMarkup(row_width=2)
diyorbek.add(
    InlineKeyboardButton("Netflix kinolar", url="https://t.me/kursishi1234"),
    InlineKeyboardButton("Tekshirish!", callback_data="diyorbeke")
)