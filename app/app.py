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
# from device import Device
from datetime import datetime
from google_play_scraper import app as app_scrap
from fastapi import FastAPI, Request
from androiddevice import AndriodDevice
from adb_shell.auth.keygen import keygen
from sqliteconnector import SqliteConnector
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse


KEYS_PATH = './config/adb'

def generate_keys():
    """ 
    Generates keys if not exists
    """
    if not path.exists(KEYS_PATH) or not path.exists((KEYS_PATH + '.pub')):
        keygen(KEYS_PATH)

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


signer = load_keys()
adb_devices=[]
devices = read_devices_list()
app = FastAPI(title="Virtual Remote for android tv", description="Virtualy control you android tv devices", version="1.0.0",  contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/virtual-remote"})
app.mount("/dist", StaticFiles(directory="dist"), name="dist")
templates = Jinja2Templates(directory="templates/")
connector = SqliteConnector()


if not os.path.exists('dist/screenshots'):
   os.makedirs('dist/screenshots')


def connect_to_device(adb_device):
    try:
        adb_device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
    except Exception as e:
        logger.error("Unable to connect: " + str(e))

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
    connect_to_device(adb_device)
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
    connect_to_device(adb_device)
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
    connect_to_device(adb_device)
    systemapps = adb_device.device.shell("pm list packages -s").splitlines()
    for sysap in systemapps:
        sysapp_id = sysap.split(':')[1]
        sysapps[sysapp_id]=get_app_details(sysapp_id)
    sysapps_json = jsonable_encoder(sysapps)
    return JSONResponse(content=sysapps_json)    

@app.get('/api/{device}/apps/3rd')
def sysapps(device:str, request: Request):
    apps = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    connect_to_device(adb_device)
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
    connect_to_device(adb_device)
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

@app.get("/api/{device}/{keyevent}")
def command(device:str,keyevent: str,request: Request):
    response = {}
    try:
        adb_device = next(d for d in adb_devices if d.ip == device)
        connect_to_device(adb_device)
        logger.info(adb_device.device.shell("input keyevent " + keyevent))
        response["success"] = True
        response["message"] = "keyevent command executed successfuly"
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as e:
        response["success"] = False
        response["message"] = str(e)
        return JSONResponse(content=jsonable_encoder(response))

@app.get('/api/{device}/{app}/open')
def open_app(device: str, app: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    connect_to_device(adb_device)
    adb_device.device.shell("monkey -p "+ app +" -c android.intent.category.LAUNCHER 1")


@app.get('/api/{device}/start')
def open_app(device: str, activity: str, request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    connect_to_device(adb_device)
    adb_device.device.shell("am start -n " + activity)




@app.get('/api/{device}/{app}/close')
def close_app(device: str, app: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    connect_to_device(adb_device)
    adb_device.device.shell("am force-stop  "+ app )


@app.get('/api/{device}/execute/{command}')
def execute_command(device: str, command: str,  request: Request):
    adb_device = next(d for d in adb_devices if d.ip == device)
    connect_to_device(adb_device)
    return(adb_device.device.shell(command).splitlines())

@app.get('/api/screenshot/get/{device}/{image}', response_class=FileResponse)
def screenshot(device: str, request: Request, image: str):
    try:
        adb_device = next(d for d in adb_devices if d.ip == device)
        connect_to_device(adb_device)
        img_name = str(uuid.uuid4())
        adb_device.device.shell('screencap -p "/sdcard/' + image + '.png"')
        adb_device.device.pull("/sdcard/" + image + ".png", "dist/screenshots/" + image + ".png")
        try:
            adb_device.device.shell('rm -f "/sdcard/' + image + '.png"')
        except Exception as e:
            logger.error("Error delete image from the device. " + str(e))
        return "dist/screenshots/" + image + ".png"
    except Exception as e:
        logger.error("Error taking screenshot. " + str(e))

    

def get_app_details(app:str):
    try:
        app_details={}
        if connector.is_app_info_exists(app):
            data = connector.get_app_info_by_id(app)[0]
            app_details["appname"] = data[1]
            app_details["appurl"] = data[2]
            app_details["appimage"] = data[3]

        else:
            appinfo = app_scrap(
                            app,
                            lang='en', # defaults to 'en'
                            country='il', # defaults to 'us'
    )
            app_details["appname"] = appinfo["title"]
            app_details["appurl"] = appinfo["url"]
            app_details["appimage"] = appinfo["icon"]
            connector.add_app_info(app, app_details["appname"],app_details["appurl"],app_details["appimage"],datetime.now())
        return app_details
    except Exception as e:
        logger.error("Error getting app info. " + str(e))
        app_details["appname"] = ""
        app_details["appurl"] = ""
        app_details["appimage"] = ""
        connector.add_app_info(app, app_details["appname"],app_details["appurl"],app_details["appimage"],datetime.now())
        return app_details



if __name__ == "__main__":
    load_keys()
    logger.info("Virtual remote is up and running")
    adb_device = adb_devices[0]
    uvicorn.run(app, host="0.0.0.0", port=80)
    
    
    


