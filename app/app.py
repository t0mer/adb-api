import time
import yaml
import json
import shutil
import uvicorn
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

for device in devices["devices"]:
    try:

        logger.info("Adding device " + device["name"] + " With IP: " + device["ip"])
        adb_device = AdbDeviceTcp(device["ip"], device["port"], default_transport_timeout_s=9.)
        adb_device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        adb_devices.append(AndriodDevice(id=device["id"],port=device["port"],name=device["name"],ip=device["ip"],device=adb_device))
    except Exception as e:
        logger.error("Error adding ADB Device with IP: " + device["ip"])
        logger.error(str(e))

# print(adb_devices[0].device.shell('echo "CPU threads: $(grep -c processor /proc/cpuinfo)"'))
#ls sys/class/thermal/

@app.get('/remotes/mibox', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('mibox.html', context={'request': request})

@app.get('/api/devices', include_in_schema=False)
def devices_lis(request: Request):
    json_devices = jsonable_encoder(devices)
    return JSONResponse(content=json_devices)

@app.get('/api/{device}/properties', include_in_schema=False)
def properties(device:str, request: Request):
    properties = {}
    adb_device = next(d for d in adb_devices if d.ip == device)
    
    device_props = adb_device.device.shell("getprop")
    for prop in device_props.splitlines():
        k= prop.split(':')[0].replace('[','').replace(']','')
        v= prop.split(':')[1].replace('[','').replace(']','')
        properties[k] = v
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


# print(adb_devices[0].shell("pm list packages -3"))
# print(adb_devices[0].shell("ip wlan0"))
# print(adb_devices[0].shell("cat /proc/meminfo | grep MemTotal"))





if __name__ == "__main__":
    load_keys()
    logger.info("Virtual remote is up and running")
    uvicorn.run(app, host="0.0.0.0", port=80)