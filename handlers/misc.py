from aiogram import Router,F
from aiogram.types import Message
from keyboards import main_menu,bot_menu,back
import random
from config import GROUP_NAME,INSTITUTION,TIMETABLE_URL
import schedule_parser,database as db
from facts import FACTS
router=Router()
@router.message(F.text=="🤖 Бот")
async def bot_menu_handler(m:Message): await m.answer("Настройки бота:",reply_markup=bot_menu())
@router.message(F.text=="🧹 Очистить кеш")
async def clear(m:Message):
    db.clear_cache(); await m.answer("Временный кеш расписания очищен. Заметки, задания и история не удалены.",reply_markup=bot_menu())
@router.message(F.text=="🔄 Обновить данные")
async def refresh(m:Message):
    data=await schedule_parser.get_schedule(force=True)
    await m.answer("Данные обновлены." if data.get("ok") else "⚠️ "+data["error"],reply_markup=bot_menu())
@router.message(F.text=="ℹ️ О боте")
async def about(m:Message): await m.answer("Бот группы %s (%s).\n\nВозможности: звонки, таймер до пары, заметки, домашние задания, факты.\n\nРасписание берётся только с официального сайта техникума: %s. Если источник недоступен или формат не распознан, бот не показывает выдуманные занятия.\n\nGitHub Actions запускается периодически, поэтому ответы и напоминания могут приходить с задержкой."%(GROUP_NAME,INSTITUTION,TIMETABLE_URL))
@router.message(F.text=="📦 Мои посылки")
async def parcels(m:Message): await m.answer("Отслеживание посылок ещё не подключено.",reply_markup=main_menu())
@router.message(F.text=="🤝 Друзья")
async def friends(m:Message): await m.answer("Раздел «Друзья» будет добавлен позже.",reply_markup=main_menu())
@router.message(F.text=="💡 Факты")
async def fact(m:Message): await m.answer("💡 "+random.choice(FACTS)+"\n\nНажмите ещё раз для следующего факта.",reply_markup=main_menu())
@router.message(F.text=="↩️ Назад")
async def back_handler(m:Message): await m.answer("Главное меню:",reply_markup=main_menu())