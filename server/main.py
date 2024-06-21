import http
import os
from fastapi import FastAPI, Response
import uvicorn
import yaml

app = FastAPI()

all_version = {}

def open_config():
    config_path = "/server/config/config.yaml"
    if(not os.path.exists(config_path)):
        raise Exception("config not exists(/server/config/config.yaml not exists)")
    if(not os.path.isfile(config_path)):
        raise Exception("config is not a file(/server/config/config.yaml is not a file)")

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        for env_name in data["versions"]:
            all_version[env_name] = str(data["versions"][env_name])
    print(all_version)


@app.get("/{env_name}.txt")
def version(env_name: str):
    if(all_version.get(env_name) == None):
        response = Response(content="Environnement not found")
        response.status_code = http.HTTPStatus.NOT_FOUND
        return response
    
    raw_version = all_version[env_name]
    version = raw_version[0:raw_version.index(";")]# remove deployment timestamp
    response = Response(content=version)
    return response

open_config()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)