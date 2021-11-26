from time import localtime, strftime
import json


def app(env, start_responce):
    
    host = env["HTTP_HOST"]
    uri = env["RAW_URI"]
    
    url = host + uri
    dtime = strftime("%H:%M:%S", localtime())
    
    data = {
        "time": dtime,
        "url": url
    }

    json_data = str.encode(json.dumps(data))
    
    start_responce("200 OK", [
        ("Content-Type", "application/json"),
        ("Content-Lenght", str(len(json_data)))
    ])
    
    return iter([json_data])
