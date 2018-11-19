import requests
from addict import Dict
import auth_config

headers = {
    'Authorization': auth_config.http_header.get('Authorization',0),
}

uri = 'http://10.1.11.23:9000/api/search/universal/relative'

payload = {
    'query':'label:ZheJiang-TZDX-L1-CO-CDN-2-HSM | stats count(status)',
    'range':90,
    'limit':1
}

r=requests.get(url=uri, params=payload, headers=headers)
result_dict = r.json()
mapping = Dict(result_dict)
count = mapping.total_results
