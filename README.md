# log_monitor

## USAGE ##
method:
GET

host:
ip:port

secheme:
http

query_uri:
/api/search/universal/relative

args --> label:${label} -->hostname   range:${range} --> timerange
query=label:${label}| stats count(status)&range=${range}&limit=10

http_header:
Authorization:xxxxx


## OUTPUT ##

output:
{
    "query": "xxxxxxx",
	"built_query": "yyyy",
    "used_indices": [
        {
            "index_name": "graylog_765",
            "begin": "1970-01-01T00:00:00.000Z",
            "end": "1970-01-01T00:00:00.000Z",
            "calculated_at": "2018-11-18T11:26:02.040Z",
            "took_ms": 0
        }
    ],
    "messages": [],
    "stats": null,
    "fields": [],
    "time": 5,
    "total_results": 0,
    "from": "2018-11-19T06:08:09.521Z",
    "to": "2018-11-19T06:13:09.521Z",
    "decoration_stats": null
}

keyword: total_results