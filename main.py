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


def format_countdown(diff):
    """Форматирует оставшееся время с учётом дней/часов/минут/секунд."""
    days = diff.days
    seconds = diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []

    if days > 0:
        # Склонение "день/дня/дней" (упрощённо: 1 — день, 2–4 — дня, остальное — дней)
        if days % 10 == 1 and days % 100 != 11:
            day_word = "день"
        elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
            day_word = "дня"
        else:
            day_word = "дней"
        parts.append(f"{days} {day_word}")

    if hours > 0 or days > 0:
        parts.append(f"{hours} часов")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes} минут")
    parts.append(f"{secs} секунд")

    # Если осталось меньше минуты — оставляем только секунды
    if days == 0 and hours == 0 and minutes == 0:
        return f"{secs} секунд"
    elif days == 0 and hours == 0:
        return f"{minutes} минут, {secs} секунд"
    elif days == 0:
        return f"{hours} часов, {minutes} минут, {secs} секунд"
    else:
        return ", ".join(parts)


async def update_countdown():
    """Обновляет сообщение каждые 5 секунд."""
    global message_id
    while True:
        now = datetime.now()
        if now >= TARGET_DATE:
            try:
                await bot.edit_message_text(
                    chat_id=CHAT_ID,
                    message_id=message_id,
                    text="🎉 С Новым годом!"
                )
            except Exception as e:
                print(f"[!] Не удалось отредактировать сообщение: {e}")
                # На всякий случай — отправим новое
                await bot.send_message(chat_id=CHAT_ID, text="🎉 С Новым годом!")
            print("[+] Обратный отсчёт завершён!")
            break

        diff = TARGET_DATE - now
        text = f"⏳ До Нового года осталось:\n\n{format_countdown(diff)}"

        try:
            await bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=message_id,
                text=text
            )
        except Exception as e:
            print(f"[!] Ошибка при редактировании: {e}")

        await asyncio.sleep(10)


@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Бот запущен! Следите за сообщением с обратным отсчётом.")


async def main():
    """Основная функция запуска."""
    print("🚀 Запуск бота на Aiogram...")
    
    await send_initial_message()
    
    # Запускаем обновление отсчёта в фоне
    countdown_task = asyncio.create_task(update_countdown())

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
