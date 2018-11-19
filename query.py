import requests
import threading
from addict import Dict
import time
import json
import base64

import machine
import auth_config

class FuncLogin(object):
    def __init__(self):
        self.uri = 'http://10.1.11.23:9000/api/system/sessions'
        self.headers = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
        }
        self.data = {
            "username":"admin",
            "password":"admin",
            "host":"10.1.11.23:9000"
        }

    def get_session_id(self):
        r = requests.post(url=self.uri, data=json.dumps(self.data), headers=self.headers)
        return r.json().get('session_id',0)

    def encode_base64(self):
        s = self.get_session_id() + ':session'
        code = base64.b64encode(s.encode())
        return 'Basic ' + code.decode()

class FuncQuery(object):
    def __init__(self, label):
        self.uri = 'http://10.1.11.23:9000/api/search/universal/relative'
        self.headers = {
            'Authorization': FuncLogin().encode_base64(),
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

@timer
def exec():
    for m in machine.machines:
        c = threading.Thread(target=t, args=(m,))
        c.start()
        t_list.append(c)

    for j in t_list:
        j.join()
exec()
print(zero_list)
