import requests
import threading
import queue
from addict import Dict
import auth_config
import machine
import time



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

zero_list = []
def t(m):
    a = FuncQuery(label=m)
    count = a.get_count()
    if count == 0:
        zero_list.append(m)

t_list = []

def timer(func):
    def warrp():
        start_time = time.time()
        func()
        end_time = time.time()
        cost_time = end_time - start_time
        print(cost_time)
    return warrp

# @timer
# def exec():
for m in machine.machines:
    c = threading.Thread(target=t, args=(m,))

    c.start()
    t_list.append(c)

for j in t_list:
    j.join()
# exec()
print(zero_list)