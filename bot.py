import asyncio,logging
from datetime import datetime
from aiogram import Bot,Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN,TIMEZONE,MORNING_HOUR,MORNING_MINUTE
from database import init_db,get_users,mark_morning,mark_lesson_notified,save_history
from handlers import start,study,notes,homework,misc
from bell import bells_for_weekday
import schedule_parser
logging.basicConfig(level=logging.INFO)
async def process_updates(bot,dp):
    offset=None; deadline=asyncio.get_event_loop().time()+45
    while asyncio.get_event_loop().time()<deadline:
        try: updates=await bot.get_updates(offset=offset,timeout=25,allowed_updates=["message","callback_query"])
        except Exception as e:
            logging.warning("get_updates error: %s",e); await asyncio.sleep(3); continue
        for u in updates:
            offset=u.update_id+1
            try: await dp.feed_update(bot,u)
            except Exception: logging.exception("update error")
async def daily_tasks(bot):
    now=datetime.now(TIMEZONE)
    if now.weekday()<5 and now.hour==MORNING_HOUR and MORNING_MINUTE<=now.minute<MORNING_MINUTE+5:
        data=await schedule_parser.get_schedule(); text="🌅 Доброе утро! Расписание РКЛ-3 на %s:\n\n"%now.date().isoformat()
        text+="\n".join(data.get("rows",[])[:40]) if data.get("ok") else data["error"]
        for row in get_users():
            if mark_morning(now.date().isoformat(),row["user_id"]):
                try: await bot.send_message(row["user_id"],text)
                except Exception as e: logging.warning("send error %s",e)
    rows=bells_for_weekday(now.weekday())
    for i,(a,b) in enumerate(rows,1):
        start=datetime.combine(now.date(),a,TIMEZONE); delta=(start-now).total_seconds()
        if 0<=delta<=15*60:
            for row in get_users():
                if mark_lesson_notified(now.date().isoformat(),row["user_id"],i):
                    try: await bot.send_message(row["user_id"],"⏰ Через 15 минут начинается пара №%d в %s."%(i,a.strftime("%H:%M")))
                    except Exception: pass
    if now.weekday()<5:
        data=await schedule_parser.get_schedule()
        if data.get("ok"): save_history(now.date().isoformat(),"\n".join(data.get("rows",[])[:100]))
async def main():
    if not BOT_TOKEN: raise SystemExit("BOT_TOKEN is not set")
    init_db(); bot=Bot(BOT_TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML)); dp=Dispatcher()
    dp.include_routers(start.router,study.router,notes.router,homework.router,misc.router)
    await daily_tasks(bot); await process_updates(bot,dp); await bot.session.close()
if __name__=="__main__": asyncio.run(main())
