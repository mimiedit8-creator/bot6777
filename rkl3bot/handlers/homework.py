from aiogram import Router,F
from aiogram.types import Message
import database as db
router=Router()
@router.message(F.text.startswith("/add_hw "))
async def add_hw(m:Message):
    parts=m.text[len("/add_hw "):].split("|"); text=parts[0].strip(); due=parts[1].strip() if len(parts)>1 else None
    if not text: return await m.answer("Введите текст задания.")
    db.add_homework(m.from_user.id,text,due); await m.answer("Домашнее задание добавлено.")
@router.message(F.text=="/my_hw")
async def my_hw(m:Message):
    rows=db.get_homework(m.from_user.id)
    await m.answer("\n".join("%d. [%s] %s (до %s)"%(r["id"],"выполнено" if r["done"] else "активно",r["text"],r["due_date"] or "—") for r in rows) if rows else "Заданий нет.")
@router.message(F.text.startswith("/done "))
async def done(m:Message):
    try: nid=int(m.text.split()[1])
    except Exception: return await m.answer("Укажите ID задания.")
    await m.answer("Отмечено." if db.set_homework_done(m.from_user.id,nid,1) else "Задание не найдено.")
@router.message(F.text.startswith("/del_hw "))
async def del_hw(m:Message):
    try: nid=int(m.text.split()[1])
    except Exception: return await m.answer("Укажите ID задания.")
    await m.answer("Удалено." if db.delete_homework(m.from_user.id,nid) else "Задание не найдено.")