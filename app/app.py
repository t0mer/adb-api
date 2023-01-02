import time
import uvicorn
from os import path
from loguru import logger
from fastapi import FastAPI, Request
from adb_shell.auth.keygen import keygen
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb





KEYS_PATH = './keys/adb'
signer = None

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
    global signer
    generate_keys()
    with open(KEYS_PATH) as f:
        priv = f.read()
    with open(KEYS_PATH + '.pub') as f:
        pub = f.read()
    signer = PythonRSASigner(pub, priv)



app = FastAPI(title="Virtual Remote for android tv", description="Virtualy control you android tv devices", version="1.0.0",  contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/virtual-remote"})
logger.info("Configuring app")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")
templates = Jinja2Templates(directory="templates/")


@app.get('/remotes/mibox', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('mibox.html', context={'request': request})


if __name__ == "__main__":
    load_keys()
    logger.info("Virtual remote is up and running")
    uvicorn.run(app, host="0.0.0.0", port=80)