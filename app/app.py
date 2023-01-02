import time
import yaml
import shutil
import uvicorn
from os import path
from loguru import logger
from device import Device
from fastapi import FastAPI, Request
from adb_shell.auth.keygen import keygen
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb


def generate_keys():
    """ 
    Generates keys if not exists
    """
    if not path.exists(KEYS_PATH) or not path.exists((KEYS_PATH + '.pub')):
        logger.warning('111')
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
logger.info("Configuring app")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")
templates = Jinja2Templates(directory="templates/")

@app.get('/remotes/mibox', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('mibox.html', context={'request': request})


for device in devices["devices"]:
    try:
        logger.info("Adding device " + device["name"] + " With IP: " + device["ip"])
        adb_device = AdbDeviceTcp(device["ip"], device["port"], default_transport_timeout_s=9.)
        logger.info("Connecting to " + device["name"])
        adb_device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        adb_devices.append(adb_device)
    except Exception as e:
        logger.error("Error adding ADB Device with IP: " + device["ip"])
        logger.error(str(e))


if __name__ == "__main__":
    load_keys()
    logger.info("Virtual remote is up and running")
    uvicorn.run(app, host="0.0.0.0", port=80)