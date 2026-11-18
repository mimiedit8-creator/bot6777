from datetime import time
# ВРЕМЕННО: уточните расписание звонков техникума в файле расписания РКЛ-3.
WEEKDAY=[(time(8,30),time(10,0)),(time(10,10),time(11,40)),(time(12,0),time(13,40)),(time(13,50),time(15,20)),(time(15,30),time(17,0)),(time(17,10),time(18,40)),(time(18,50),time(20,20))]
SAT=[(time(8,30),time(10,0)),(time(10,10),time(11,40)),(time(11,50),time(13,20)),(time(13,30),time(15,0)),(time(15,10),time(16,40)),(time(16,50),time(18,20))]
def bells_for_weekday(wd):
    if wd==6: return []
    return SAT if wd==5 else WEEKDAY
