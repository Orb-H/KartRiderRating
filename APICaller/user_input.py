import datetime
import importlib

kq = importlib.import_module('kart_query')

qc = kq.QueryCaller(5)
qc.start()

while True:
    s = input()
    t = s.split()
    if t[0].lower() == 'stop':
        break
    if t[0].lower() == 'daily':
        y, m, d = [int(x) for x in t[1].split('-')]
        dqo = kq.DailyQueryObject(datetime.date(y, m, d), '스피드 개인전')
        qc.add_query(dqo)
qc.stop()
