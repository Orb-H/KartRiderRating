import json
import time
import requests
import datetime

pcg = json.load(open('key.json'))['PlatinumCapsuleGear']
gt = json.load(open('metadata/gameType.json'))


class QueryObject:
    def __init__(self, url: str, **kwargs):
        self.url = url
        self.headers = {}
        self.params = kwargs

    def __str__(self):
        return "url: {0}\nheaders: {1}\nparams: {2}".format(self.url, self.headers, self.params)

    # query-dependent, qc means current calling QueryCaller
    def handler(self, qc: QueryCaller, *args, **kwargs):
        raise NotImplementedError()

    # query-independent
    def onExecute(self, *args, **kwargs):
        raise NotImplementedError()


class QueryQueue:
    def __init__(self):
        self.q = []

    def enqueue(self, qo: QueryObject):
        qo.headers['Authorization'] = pcg
        self.q.append(qo)

    def dequeue(self):
        if len(self.q) == 0:
            return None
        return self.q.pop(0)


class QueryCaller:
    def __init__(self, i: float):
        if i <= 0:
            raise ValueError()
        self.interval = i
        self.paused = False
        self.stopped = True
        self.q = QueryQueue()

    def start(self):
        self.stopped = False
        self.run()

    def stop(self):
        self.stopped = True

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):
        while not self.stopped:
            while not self.paused:
                qo = self.q.dequeue()
                if qo != None:
                    r = requests.get(
                        url=qo.url, headers=qo.headers, params=qo.params)
                    print(r.json())
            time.sleep(self.interval)

    def add_query(self, qo: QueryObject):
        self.q.enqueue(qo)


class DetailQueryObject(QueryObject):
    def __init__(self, id: str):
        QueryObject.__init__(
            self, 'https://api.nexon.co.kr/kart/v1.0/matches/{0}'.format(id))

    def handler(self, qc, *args, **kwargs):
        pass  # database access needed / DBMS .py needed

    def onExecute(self, *args, **kwargs):
        pass  # log needed


# Find all matching games with given gametype and function in specific date
class DailyQueryObject(QueryObject):
    def __init__(self, date: datetime.date, gametype: str, f: function):
        self.d_end = datetime.datetime(
            date.year, date.month, date.day, 23, 59, 59)
        self.d_start = datetime.datetime(
            date.year, date.month, date.day, 0, 0, 0)
        self.f = f
        QueryObject.__init__(self, 'https://api.nexon.co.kr/kart/v1.0/matches/all',
                             match_types=gt[gametype], start_date=self.d_start.isoformat(' '), end_date=self.d_end.isoformat(' '), limit=500)

    def handler(self, qc, *args, **kwargs):
        pass  # for every game, check if f match and create new QueryObject

    def onExecute(self, *args, **kwargs):
        pass  # log needed
