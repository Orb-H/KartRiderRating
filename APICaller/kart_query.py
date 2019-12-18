import json
import time
import requests
import datetime
import threading

pcg = json.load(open('key.json'))['PlatinumCapsuleGear']
gt = json.load(open('metadata/gameType.json'))
l = open('log_{0}'.format(datetime.datetime.now().isoformat()))


class QueryObject:
    def __init__(self, url: str, **kwargs) -> QueryObject:
        self.url = url
        self.headers = {}
        self.params = kwargs

    def __str__(self) -> str:
        return "url: {0}\nheaders: {1}\nparams: {2}".format(self.url, self.headers, self.params)

    # query-dependent, qc means current calling QueryCaller
    def handler(self, qc: QueryCaller, r: requests.Response, *args, **kwargs) -> None:
        raise NotImplementedError()

    # query-independent
    def onExecute(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class QueryQueue:
    def __init__(self) -> QueryQueue:
        self.q = []

    def enqueue(self, qo: QueryObject) -> None:
        qo.headers['Authorization'] = pcg
        self.q.append(qo)

    def dequeue(self) -> QueryObject:
        if len(self.q) == 0:
            return None
        return self.q.pop(0)


class QueryCaller:
    def __init__(self, i: float) -> QueryCaller:
        if i <= 0:
            raise ValueError()
        self.interval = i
        self.paused = False
        self.stopped = True
        self.q = QueryQueue()

    def start(self) -> None:
        self.stopped = False
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self) -> None:
        self.stopped = True

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def run(self) -> None:
        while not self.stopped:
            if not self.paused:
                qo = self.q.dequeue()
                if qo != None:
                    r = requests.get(
                        url=qo.url, headers=qo.headers, params=qo.params)
                    print(r.json())
            time.sleep(self.interval)

    def add_query(self, qo: QueryObject) -> None:
        self.q.enqueue(qo)


class DetailQueryObject(QueryObject):
    def __init__(self, match_id: str) -> DetailQueryObject:
        self.m = match_id
        QueryObject.__init__(
            self, 'https://api.nexon.co.kr/kart/v1.0/matches/{0}'.format(match_id))

    def handler(self, qc: QueryCaller, r: requests.Response, *args, **kwargs) -> None:
        pass  # database access needed / DBMS .py needed

    def onExecute(self, *args, **kwargs) -> None:
        log('{0}: Match detail query with id {1}'.format(
            datetime.datetime.now().isoformat(), self.m))


# Find all matching games with given gametype and function in specific date
class DailyQueryObject(QueryObject):
    def __init__(self, date: datetime.date, gametype: str, f: dict) -> DailyQueryObject:
        self.d_end = datetime.datetime(
            date.year, date.month, date.day, 23, 59, 59)
        self.d_start = datetime.datetime(
            date.year, date.month, date.day, 0, 0, 0)
        self.g = gametype
        self.f = f
        QueryObject.__init__(self, 'https://api.nexon.co.kr/kart/v1.0/matches/all',
                             match_types=gt[gametype], start_date=self.d_start.isoformat(' '), end_date=self.d_end.isoformat(' '), limit=500)

    def handler(self, qc: QueryCaller, r: requests.Response, *args, **kwargs) -> None:
        pass  # for every game, check if f match and create new QueryObject

    def onExecute(self, *args, **kwargs) -> None:
        log('{0}: Daily query between {1} ~ {2}, gametype {3}, filter: {4}'.format(
            datetime.datetime.now().isoformat(), self.d_start.isoformat(), self.d_end.isoformat(), self.g, self.f))


def log(s: str) -> None:
    print(s)
    l.write(s)
