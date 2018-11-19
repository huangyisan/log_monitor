import requests
import threading
import queue
from addict import Dict
import auth_config
import machine

class FuncQuery(object):
    def __init__(self, label):
        self.uri = 'http://10.1.11.23:9000/api/search/universal/relative'
        self.headers = {
            'Authorization': auth_config.http_header.get('Authorization', 0),
        }
        self.payloads = {
            'query': 'label:{0} | stats count(status)'.format(label),
            'range': 90,
            'limit': 1
        }

    def get_result(self):
        r = requests.get(url=self.uri, params=self.payloads, headers=self.headers)
        return r.json()

    def get_count(self):
        result_dict = self.get_result()
        mapping = Dict(result_dict)
        count = mapping.total_results
        return count



class FuncQueue(FuncQuery):
    def __init__(self, flag, q):
        '''

        :param flag: 0 --> port open; 1 --> port block
        :param q: queue.Queue()
        '''
        super(FuncQueue, self).__init__(flag)
        self.q = q
        self.flag = flag

    def listqueue(self, line):
        '''

        :param line: ip port
        :return:
        '''
        if self.test_stat(line):
            self.q.put(self.test_stat(line))

    def sizequeue(self):
        return self.q.qsize()
zero_list = []
def t(m):

    a = FuncQuery(label=m)
    count = a.get_count()
    if count == 0:
        zero_list.append(m)

t_list = []

for m in machine.machines:
    c = threading.Thread(target=t, args=(m,))

    c.start()
    t_list.append(c)

for j in t_list:
    j.join()

print(zero_list)