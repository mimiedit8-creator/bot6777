from aiogram import Router,F
from aiogram.types import Message
from keyboards import back
import database as db
router=Router()
@router.message(F.text=="📝 Мои заметки")
async def notes_menu(m:Message): await m.answer("Заметки. Команды:\n/add_note текст\n/my_notes\n/del_note ID",reply_markup=back())
@router.message(F.text.startswith("/add_note "))
async def add_note(m:Message):
    text=m.text[len("/add_note "):].strip()
    if not text: return await m.answer("Введите текст после команды.")
    db.add_note(m.from_user.id,text); await m.answer("Заметка сохранена.")
@router.message(F.text=="/my_notes")
async def my_notes(m:Message):
    rows=db.get_notes(m.from_user.id)
    await m.answer("\n".join("%d. %s"%(r["id"],r["text"]) for r in rows) if rows else "Заметок нет.")
@router.message(F.text.startswith("/del_note "))
async def del_note(m:Message):
    try: nid=int(m.text.split()[1])
    except Exception: return await m.answer("Укажите ID заметки.")
    await m.answer("Удалено." if db.delete_note(m.from_user.id,nid) else "Заметка не найдена.")