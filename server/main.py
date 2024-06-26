import http
from time import sleep
from fastapi import FastAPI, Response
import yaml
import requests
from threading import Thread
import json

last_config = ""
all_version = {}
in_prod = True

def infinite_loop_check_config():
    while(True):
        sleep(10)
        check_config()

def check_config():
    global last_config
    global all_version
    global in_prod

    response = requests.get('http://localhost:8080/api/v1/namespaces/default/configmaps/pmu-version-config')
    if(response.status_code != 200):
        print("not found pmu-version-config")
    else:
        json_response = json.loads(response.text)

        if(json_response["data"]["config"] != last_config):
            last_config = json_response["data"]["config"]
            config = yaml.load(last_config, Loader=yaml.FullLoader)
            print("New config loaded: '" + last_config + "'")
            in_prod = config["prod"]
            all_version =  config["versions"]

check_config()

app = FastAPI()

if(in_prod):
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:   
    app = FastAPI()

@app.get("/{env_name}.txt")
def version(env_name: str):
    if(last_config == ""):
        response = Response(content="Config not found")
        return response
    if(all_version.get(env_name) == None):
        response = Response(content="Environnement not found")
        response.status_code = http.HTTPStatus.NOT_FOUND
        return response
    
    version = all_version[env_name]
    response = Response(content=version)
    return response

check_config_thread = Thread(target = infinite_loop_check_config, daemon=True)
check_config_thread.start()
