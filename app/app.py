 # -*- coding: utf-8 -*

import os
import yaml
import json
import uuid
import shutil
import uvicorn
import requests
from os import path
from loguru import logger
from device import Device
from fastapi import FastAPI, Request
from androiddevice import AndriodDevice
from adb_shell.auth.keygen import keygen
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb


def generate_keys():
    """ 
    Generates keys if not exists
    """
    if not path.exists(KEYS_PATH) or not path.exists((KEYS_PATH + '.pub')):
        keygen('./keys/adb')

def load_keys():
    """
    Load keys from files
    """
    generate_keys()
    with open(KEYS_PATH) as f:
        priv = f.read()
    with open(KEYS_PATH + '.pub') as f:
        pub = f.read()
    return PythonRSASigner(pub, priv)

def read_devices_list():
    if not path.exists("config/devices.yaml"):
        shutil.copy("devices.yaml","config/devices.yaml")

    with open("config/devices.yaml",'r',encoding='utf-8') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)
            return []

KEYS_PATH = './keys/adb'
signer = load_keys()
adb_devices=[]
devices = read_devices_list()
app = FastAPI(title="Virtual Remote for android tv", description="Virtualy control you android tv devices", version="1.0.0",  contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/virtual-remote"})
app.mount("/dist", StaticFiles(directory="dist"), name="dist")
templates = Jinja2Templates(directory="templates/")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")
USE_PROXY = os.getenv("USE_PROXY")


if not os.path.exists('dist/screenshots'):
   os.makedirs('dist/screenshots')

if bool(USE_PROXY) == True:
    gateway = ApiGateway("https://cse.google.com",access_key_id=AWS_ACCESS_KEY,access_key_secret=AWS_SECRET)
    gateway.start()
    session = requests.Session()
    session.mount("https://cse.google.com", gateway)


for device in devices["devices"]:
    try:

        logger.info("Adding device " + device["name"] + " With IP: " + device["ip"])
        adb_device = AdbDeviceTcp(device["ip"], device["port"], default_transport_timeout_s=9.)
        adb_device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        adb_devices.append(AndriodDevice(id=device["id"],port=device["port"],name=device["name"],ip=device["ip"],device=adb_device))
    except Exception as e:
        logger.error("Error adding ADB Device with IP: " + device["ip"])
        logger.error(str(e))


@app.get('/remotes/{remote}')
def index(remote: str, request: Request):
    return templates.TemplateResponse(remote + '.html', context={'request': request})

@app.get('/api/devices')
def devices_lis(request: Request):
    json_devices = jsonable_encoder(devices)
    return JSONResponse(content=json_devices)

@app.get('/api/{device}/properties')
def properties(device:str, request: Request):
    properties = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    
    device_props = adb_device.device.shell("getprop")
    for prop in device_props.splitlines():
        k= prop.split(':')[0].replace('[','').replace(']','')
        v= prop.split(':')[1].replace('[','').replace(']','')
        properties[k.replace(".","_")] = v
    json_devices = jsonable_encoder(properties)
    return JSONResponse(content=json_devices)

@app.get('/api/{device}/memory')
def memory(device:str, request: Request):
    device_memory = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    meminfo = adb_device.device.shell("cat /proc/meminfo")
    for prop in meminfo.splitlines():
        k= prop.split(':')[0].strip()
        v= prop.split(':')[1].strip()
        device_memory[k] = v
    memory_json = jsonable_encoder(device_memory)
    return JSONResponse(content=memory_json)

@app.get('/api/{device}/apps/system')
def sysapps(device:str, request: Request):
    sysapps = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    systemapps = adb_device.device.shell("pm list packages -s").splitlines()
    i=0
    for sysap in systemapps:
        sysapps[i] = sysap.split(':')[1]
        i+=1
    sysapps_json = jsonable_encoder(sysapps)
    return JSONResponse(content=sysapps_json)    

@app.get('/api/{device}/apps/3rd')
def sysapps(device:str, request: Request):
    apps = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    apps3rd = adb_device.device.shell("pm list packages -3").splitlines()
    for app3rd in apps3rd:
        app_id = app3rd.split(':')[1]
        apps[app_id] = get_app_details(app_id)
    apps3rd_json = jsonable_encoder(apps)
    return JSONResponse(content=apps3rd_json)    


@app.get('/api/{device}/cpu')
def cpu(device:str, request: Request):
    device_cpu = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    cores =adb_devices[0].device.shell("grep -c processor /proc/cpuinfo")
    cpuinfo = adb_device.device.shell("cat /proc/cpuinfo")
    cpu_num = 0
    device_cpu["cores"] = cores.replace("\n","")
    for prop in cpuinfo.splitlines():
        if ":" in prop and not "processor" in prop:
            k= prop.split(':')[0].strip()
            v= prop.split(':')[1].strip()
            device_cpu[k] = v
    
    cpu_json = jsonable_encoder(device_cpu)
    return JSONResponse(content=cpu_json)

@app.get("/api/{device}/{command}")
def command(device:str,command: str,request: Request):
    response = {}
    try:
        adb_device = next(d for d in adb_devices if d.ip == device)
        adb_device.device.shell("input keyevent " + command)
        response["success"] = True
        response["message"] = "Command executed successfuly"
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as e:
        response["success"] = False
        response["message"] = str(e)
        return JSONResponse(content=jsonable_encoder(response))

@app.get('/api/{device}/{app}/open')
def get_app_details(device: str, app: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    adb_device.device.shell("monkey -p "+ app +" -c android.intent.category.LAUNCHER 1")

@app.get('/api/{device}/{app}/close')
def get_app_details(device: str, app: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    adb_device.device.shell("am force-stop  "+ app )


@app.get('/api/{device}/execute/{command}')
def get_app_details(device: str, command: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    return(adb_device.device.shell(command))



@app.get('/api/screenshot/get/{device}')
def screenshot(device: str, request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    img_name = str(uuid.uuid4())
    adb_device.device.shell('screencap -p "/sdcard/' + img_name + '.png"')
    adb_device.device.pull("/sdcard/" + img_name + ".png", "dist/screenshots/" + img_name + ".png")
    result = {}
    result["img"] =  "dist/screenshots" + img_name + ".png"
    result["success"] = True
    return JSONResponse(content=jsonable_encoder(result))


    

# @app.get('/api/app/{app}/details')
def get_app_details(app:str):
    app_details={}
    # url='https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=1&hl=en&source=gcsc&gss=.com&cselibv=c20e9fb0a344f1f9&cx=12515e75ed027d689&q='+ app +'&cse_tok=ALwrddFOhDvzXM0yPEPpmDDLPzzC:1673362684904&sort=&cseclient=hosted-page-client&callback=google.search.cse.api12431'
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={app}&start=1"

    if bool(USE_PROXY) == True:
        logger.info("Getting app info using proxy")
        response = session.get(url, params={"theme": "dark"})
    else:
        logger.info("Getting app info without proxy")
        response = requests.get(url)

    data = json.loads(response.text)
    app_details["appname"] = data["items"][0]["title"]
    app_details["appurl"] = data["items"][0]["link"]
    app_details["appimage"] = data["items"][0]["pagemap"]["cse_image"][0]["src"]
    # app_details_json = jsonable_encoder(app_details)
    # return JSONResponse(content=app_details_json)
    return app_details


if __name__ == "__main__":
    load_keys()
    logger.info("Virtual remote is up and running")
    adb_device = adb_devices[0]

    
    uvicorn.run(app, host="0.0.0.0", port=80)
    
    
    


