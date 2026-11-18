from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
def kb(rows): return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=x) for x in r] for r in rows],resize_keyboard=True)
def main_menu(): return kb([["🎓 Учёба","🤖 Бот"],["📝 Мои заметки","📦 Мои посылки"],["🤝 Друзья","💡 Факты"]])
def study_menu(): return kb([["📅 Расписание","🔔 Звонки"],["⏳ До следующей пары","📚 Домашние задания"],["🕘 Прошлая неделя","↩️ Назад"]])
def schedule_menu(): return kb([["Сегодня","Завтра"],["Послезавтра","Вся неделя"],["Назад"]])
def bot_menu(): return kb([["🧹 Очистить кеш","🔄 Обновить данные"],["ℹ️ О боте","↩️ Назад"]])
def back(): return kb([["↩️ Назад"]])
