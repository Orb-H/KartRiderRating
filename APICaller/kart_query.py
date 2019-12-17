import json
import time
import requests

pcg = json.load(open('key.json'))['PlatinumCapsuleGear']


class QueryObject:
    def __init__(self, url: str, **kwargs):
        self.url = url
        self.headers = {}
        self.params = kwargs

    def __str__(self):
        return "url: {0}\nheaders: {1}\nparams: {2}".format(self.url, self.headers, self.params)


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
