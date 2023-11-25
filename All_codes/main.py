import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor
from PIL import Image
from openai import OpenAI
import wget
import os
from buttons import diyorbek


logging.basicConfig(level=logging.INFO)


client = OpenAI(api_key="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")


TOKEN = '6636034372:AAFzQcJHfIhTyKopRncsD0Tj88_NVOMJ0Jo' 
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Assalomu alaykum yangi foydalanuvchi rasimni generatsiya qiladigan botimizga xush kelipsiz. Ushbu botdan foydalanish uchun quydagi kannalarga a'zo bulishingiz kerak!", reply_markup=diyorbek)



@dp.callback_query_handler(lambda C: C.data)
async def diyorbeke(callback: types.CallbackQuery):
    try:
        user_status = await bot.get_chat_member(chat_id="-1001944380866", user_id=callback.message.chat.id)
        if user_status.status in ["creator", "administrator", "member"]:
            await callback.answer(show_alert=True, text="😃Obunangiz uchun tashakur siz endi botdan foydalanishiniz mumkin🙃") 
        else:
            await callback.answer(show_alert=True, text="😒Hurmatli foydalanuvchi siz kannalga a'zo bulmagansiz👈")
    except:
        await callback.answer(show_alert=True, text="😒Hurmatli foydalanuvchi siz kannalga a'zo bulmagansiz👈")


@dp.message_handler(lambda message: message.text.startswith('/generate_image'))
async def generate_image(message: types.Message):
   
        user_status = await bot.get_chat_member(chat_id="-1001944380866", user_id=message.chat.id)
        if user_status.status in ["creator", "administrator", "member"]:
            await bot.send_message(message.chat.id, text="Sizning so'rovingiz bajarilmoqda. Iltimos kuting...") 
        
            command, *args = message.text.split(maxsplit=1)
            if len(args) == 1:
                prompt = args[0]
                logging.info(f"Received command: /generate_image {prompt}")
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",  
                    quality="standard",
                    n=1
                )
                image_url = response.data[0].url
                filename = wget.download(image_url)

                
                with open(filename, 'rb') as photo:
                    await bot.send_photo(message.chat.id, photo)

               
                os.remove(filename)
            else:
                await message.reply("Invalid command format. Please use /generate_image <prompt>")

        else:
            await bot.send_message(message.chat.id, text="😒Hurmatli foydalanuvchi siz kannalga a'zo bulmagansiz👈", reply_markup=diyorbek)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
