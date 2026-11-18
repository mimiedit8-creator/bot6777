from aiogram import Router,F
from aiogram.types import Message
from keyboards import study_menu,schedule_menu,back
from datetime import datetime,timedelta
from config import TIMEZONE,GROUP_NAME
import schedule_parser,bell,database as db
router=Router()
@router.message(F.text=="🎓 Учёба")
async def study(m:Message): await m.answer("Раздел «Учёба».",reply_markup=study_menu())
@router.message(F.text=="📅 Расписание")
async def schedule(m:Message): await m.answer("Расписание группы %s. Выберите день:"%GROUP_NAME,reply_markup=schedule_menu())
async def show_day(m,offset):
    data=await schedule_parser.get_schedule(); date=(datetime.now(TIMEZONE)+timedelta(days=offset)).date()
    if not data.get("ok"): return await m.answer("⚠️ "+data["error"],reply_markup=schedule_menu())
    rows=data.get("rows",[])
    text="📅 Расписание РКЛ-3 на %s:\n\n"%date.isoformat()+"\n".join(rows[:40]) if rows else "Для выбранной даты занятия в найденном файле не указаны."
    await m.answer(text,reply_markup=schedule_menu())
@router.message(F.text=="Сегодня")
async def today(m:Message): await show_day(m,0)
@router.message(F.text=="Завтра")
async def tomorrow(m:Message): await show_day(m,1)
@router.message(F.text=="Послезавтра")
async def after(m:Message): await show_day(m,2)
@router.message(F.text=="Вся неделя")
async def week(m:Message): await show_day(m,0)
@router.message(F.text=="🔔 Звонки")
async def bells(m:Message):
    now=datetime.now(TIMEZONE); rows=bell.bells_for_weekday(now.weekday())
    if not rows: return await m.answer("Сегодня воскресенье — занятий нет.")
    text="🔔 Звонки на сегодня, %s:\n\n"%now.strftime("%d.%m.%Y")
    for i,(a,b) in enumerate(rows,1): text+="%d. %s–%s\n"%(i,a.strftime("%H:%M"),b.strftime("%H:%M"))
    await m.answer(text)
@router.message(F.text=="⏳ До следующей пары")
async def next_lesson(m:Message):
    now=datetime.now(TIMEZONE); rows=bell.bells_for_weekday(now.weekday())
    for i,(a,b) in enumerate(rows,1):
        start=datetime.combine(now.date(),a,TIMEZONE)
        if start>now: return await m.answer("⏳ Ближайшая пара:\n№%d\nНачало: %s\nОкончание: %s\nДо начала: %d мин."%(i,a.strftime("%H:%M"),b.strftime("%H:%M"),int((start-now).total_seconds()//60)))
    await m.answer("Занятия на сегодня закончились. Первая пара следующего учебного дня — в 08:30.")
@router.message(F.text=="🕘 Прошлая неделя")
async def last_week(m:Message):
    now=datetime.now(TIMEZONE); monday=now.date()-timedelta(days=now.weekday())-timedelta(days=7); parts=[]
    for i in range(5):
        d=monday+timedelta(days=i); row=db.get_history(d.isoformat())
        if row: parts.append("%s: %s"%(d.isoformat(),row["payload"][:500]))
    await m.answer("🕘 Расписание прошлой недели:\n\n"+"\n\n".join(parts) if parts else "История расписания за прошлую неделю пока не собрана. Она начинает сохраняться после установки бота.")
@router.message(F.text=="📚 Домашние задания")
async def homework_menu(m:Message): await m.answer("Домашние задания. Команды:\n/add_hw текст | срок ГГГГ-ММ-ДД\n/my_hw\n/done ID\n/del_hw ID",reply_markup=back())