import requests
import threading
import queue
from addict import Dict
import auth_config
import machine


headers = {
    'Authorization': auth_config.http_header.get('Authorization',0),
}

uri = 'http://10.1.11.23:9000/api/search/universal/relative'


for m in machine.machines:
    payload = {
        'query': 'label:{0} | stats count(status)'.format(m),
        'range': 90,
        'limit': 1
    }
    print(payload)

    r=requests.get(url=uri, params=payload, headers=headers)
    result_dict = r.json()
    mapping = Dict(result_dict)
    count = mapping.total_results
    print(count)
