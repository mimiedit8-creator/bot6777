import aiohttp,asyncio,json,datetime,re,io
from bs4 import BeautifulSoup
from config import TIMETABLE_URL,CACHE_TTL_MINUTES,GROUP_NAME,INSTITUTION
import database as db
try: import openpyxl
except ImportError: openpyxl=None
async def fetch_page():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=25)) as s:
        async with s.get(TIMETABLE_URL) as r:
            r.raise_for_status(); return await r.text()
def find_links(html):
    soup=BeautifulSoup(html,"lxml"); found=[]
    for a in soup.find_all("a",href=True):
        text=re.sub(r"\s+"," ",a.get_text(" ",strip=True)); href=a["href"]; low=(text+" "+href).lower()
        if "ркл-3" in low or "ркл 3" in low:
            if "расписан" in low or href.lower().endswith((".xlsx",".xls",".pdf")):
                found.append({"text":text,"href":href})
    return found
def parse_xlsx(content):
    if not openpyxl: return None
    try:
        wb=openpyxl.load_workbook(io.BytesIO(content),data_only=True,read_only=True); rows=[]
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                vals=[str(v) for v in row if v is not None]; line=" | ".join(vals)
                if GROUP_NAME.lower() in line.lower(): rows.append(line)
        if rows: return {"ok":True,"source":"xlsx","rows":rows[:200]}
    except Exception: return None
    return None
async def get_schedule(force=False):
    cache=db.get_cache()
    if cache and not force:
        try:
            data=json.loads(cache["payload"]); age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(cache["updated_at"])).total_seconds()
            if age<CACHE_TTL_MINUTES*60: return data
        except Exception: pass
    try:
        html=await fetch_page(); links=find_links(html)
        if not links: return {"ok":False,"error":"На сайте %s пока не найдена ссылка на расписание занятий группы РКЛ-3. Бот не показывает выдуманные занятия."%INSTITUTION}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as s:
            async with s.get(links[0]["href"]) as r:
                if r.status!=200: return {"ok":False,"error":"Файл расписания недоступен (HTTP %s)."%r.status}
                content=await r.read()
        parsed=parse_xlsx(content)
        if parsed:
            db.set_cache(json.dumps(parsed,ensure_ascii=False)); return parsed
        return {"ok":False,"error":"Найден документ, но его формат пока не удалось надёжно разобрать. Ссылка: "+links[0]["href"]}
    except Exception as e:
        return {"ok":False,"error":"Сайт техникума временно недоступен или не удалось получить данные: %s"%type(e).__name__}
