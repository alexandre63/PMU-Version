import http
from fastapi import FastAPI, Response
import yaml
import requests
import json

in_prod = True

def get_config():
    global in_prod

    response = requests.get('http://localhost:8080/api/v1/namespaces/default/configmaps/pmu-version-config')
    if(response.status_code != 200):
        print("not found pmu-version-config")
        return {}
    else:
        json_response = json.loads(response.text)#parse in json the http response
        return yaml.load(json_response["data"]["config"], Loader=yaml.FullLoader)#http response to dict config

config = get_config()
if(config != {} and config["prod"]):
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:   
    app = FastAPI()

@app.get("/{env_name}.txt")
def version(env_name: str):
    config = get_config()
    if(config == {}):
        response = Response(content="Config not found")
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        return response
    versions_config = config["versions"]
    if(versions_config.get(env_name) == None):
        response = Response(content="Environnement not found")
        response.status_code = http.HTTPStatus.NOT_FOUND
        return response
    
    version = versions_config[env_name]
    response = Response(content=version)
    return response
