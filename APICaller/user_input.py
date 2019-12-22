from . import kart_query as kq

qc = kq.QueryCaller(5)

while True:
    s = input()
    t = s.split()
    if t[0].lower() == 'stop':
        break
qc.stop()
