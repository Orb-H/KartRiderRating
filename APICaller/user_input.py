from . import kart_query as kq
import datetime

qc = kq.QueryCaller(5)
qc.start()

while True:
    s = input()
    t = s.split()
    if t[0].lower() == 'stop':
        break
    if t[0].lower() == 'daily':
        try:
            y, m, d = t[1].split('-')
            dqo = kq.DailyQueryObject(datetime.date(y, m, d), '스피드 개인전')
            qc.add_query(dqo)
        except:
            pass
qc.stop()
