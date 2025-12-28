import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message


BOT_TOKEN = "8223081390:AAFV0KbkVOqey3jw9tqGNWExXZ3WJJKiuQQ"
CHAT_ID = -1003514039550
TARGET_DATE = datetime(2026, 1, 1, 0, 0, 0)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


message_id = None

async def send_initial_message():
    """Отправляет первое сообщение и сохраняет его ID."""
    global message_id
    text = "⏳ Инициализация обратного отсчёта до Нового года 2026..."
    msg = await bot.send_message(chat_id=CHAT_ID, text=text)
    message_id = msg.message_id
    print(f"[+] Сообщение отправлено. ID: {message_id}")

async def update_countdown():
    """Обновляет сообщение каждые 10 секунд."""
    global message_id
    while True:
        now = datetime.now()
        if now >= TARGET_DATE:
            await bot.send_message(
                chat_id=CHAT_ID,
                message_id=message_id,
                text="С Новым годом"
            )
            print("[+] Обратный отсчёт завершён!")
            break

        diff = TARGET_DATE - now
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        text = (
            f" до нового года осталось:\n\n"
            f"{days} дня, "
            f"{hours} часов, "
            f"{minutes} минут, "
            f"{secs} секунд"
        )

        try:
            await bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=message_id,
                text=text
            )
        except Exception as e:
            print(f"[!] Ошибка при редактировании: {e}")

        await asyncio.sleep(5)  

@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Бот запущен! Следите за сообщением с обратным отсчётом.")

async def main():
    """Основная функция запуска."""
    print("🚀 Запуск бота на Aiogram...")
    
   
    await send_initial_message()
    
    
    countdown_task = asyncio.create_task(update_countdown())
    
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
