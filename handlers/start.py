from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import main_menu
import database as db
router=Router()
@router.message(CommandStart())
async def start(m:Message):
    db.upsert_user(m.from_user)
    await m.answer("Привет! Это бот группы РКЛ-3 Волжского политехнического техникума.\n\nВыберите раздел:",reply_markup=main_menu())