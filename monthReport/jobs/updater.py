from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,timedelta
from monthReport.models import MonthData , RecordData
from monthReport.Serializer import RecordDataSerializer, MonthDataSerializer
import time 

sched = BackgroundScheduler()
#테스트
# @sched.scheduled_job('interval',seconds=30,id = "update")
# 매달 1일 실행 
@sched.scheduled_job('interval',days=1,id = "update")
def save_list():
    now = datetime.now() - timedelta(days=1) # 전 날 발급 
    print(now) 
    lastKeyDate = ""
    if now.month<10:
        lastKeyDate = str(now.year)+".0"+str(now.month)
    else:
        lastKeyDate = str(now.year)+"."+str(now.month)
    
    dataList = MonthData.objects.filter(keyDate=lastKeyDate).order_by('-totalPoint')

    # 기존 데이터가 없고 이전 달의 데이터가 있는경우만 실행 
    if not RecordData.objects.filter(keyDate=lastKeyDate) and dataList:
        # 점수 순으로 받기 
        for i in range(0,len(dataList)):
            data = MonthDataSerializer(dataList[i]).data
            print(i+1,data["totalPer"],data["totalPoint"])
            RecordData.objects.create(
                ranking = (i+1),
                userId = dataList[i].userId,
                keyDate = lastKeyDate,
                totalPer = data["totalPer"],
                totalPoint = data["totalPoint"],
                activityNum = data["taskCount"]+data["dayRoutineCount"],
                clearNum = data["doneTask"] + data["clearRoutine"]
            )

def start():
    sched.start()

