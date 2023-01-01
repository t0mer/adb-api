from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen
import time
from os import path


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

