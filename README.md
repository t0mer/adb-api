# ADB-API

ADB-API is a python-based application to help us control android-based streamers like Xiaomi and more.
With ADB-API, you can easily do the following things: 

* Create a virtual remote.
* List all devices.
* Get device properties (Version, OS, and more).
* Get device memory usage.
* Get device CPU information.
* Get the list of installed appliances (system and 3rd party).
* Open or Close any installed app.
* Take a screenshot from the device.
* Execute commands.
* Send key events (Single key or key chain).

## Components and Libraries used in ADB-API

* [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production.
* [Uvicorn](https://www.uvicorn.org/) - lightning-fast ASGI server implementation, using uvloop and httptools. 
* [jinja](https://jinja.palletsprojects.com/en/3.0.x/) - fast, expressive, extensible templating engine.
* [aiofile](https://pypi.org/project/aiofile/) - Real asynchronous file operations with asyncio support.
* [loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) - An object to dispatch logging messages to configured handlers.
* [python-multipart](https://pypi.org/project/python-multipart/) - A streaming multipart parser for Python.
* [requests](https://docs.python-requests.org/en/latest/) - elegant and simple HTTP library for Python, built for human beings.
* [google-play-scraper](https://pypi.org/project/google-play-scraper/) - Google-Play-Scraper provides APIs to easily crawl the Google Play Store for Python without any external dependencies!
* [dataclasses-json](https://pypi.org/project/dataclasses-json/) - This library provides a simple API for encoding and decoding dataclasses to and from JSON.
* [adb-shell](https://pypi.org/project/adb-shell/) - A Python implementation of ADB with shell and FileSync functionality.
* [pyyaml](https://pypi.org/project/PyYAML/) - YAML parser and emitter for Python


## Installation and Configuration
In order to use the ADB-API, you need to enable "Develpoer mode" on the Android tv based streamer. to do so, follow the next steps:
1. On your TV device, navigate to Settings.
2. In the Device row, select About.
3. Scroll down to Build and select Build several times until you get the message "You are now a developer!"
4. Return to Settings. In the Preferences row, select Developer options.
5. Select Debugging > USB debugging and select On.
6. Navigate back to the TV home screen.

Now, after you enabled the Developer mode it's time to install the ADB-API docker. to do so, create a file named "docker-compose.yaml" and add the following code:

```yaml
version: "3.7"

services:

  adb_api:
    image: techblog/adb-api
    container_name: adb-api
    privileged: true
    restart: always
    ports:
      - "80:80" 
    volumes:
      - ./adb-api/config:/app/config
```
create a folder named "adb-api/config" on the same level with the yaml file and create a new file named "devices.yaml" with the following content:

```yaml
devices:

  - id: 1
    name: 
    ip: 
    port: 

  - id: 2
    name: 
    ip: 
    port: 
```
And update the devices list according to your devices details.

***You can set the path for the config directory. The one in the code sample is just an example.***

Now, run the following command to install and start the container:
```bash
docker-compose up -d
```

After the container starts, more file will be added to the config directory:
1. 2 key files for connecting the devices (Certificates).
2. sqlite db to speed up the performence of part of the api calls.

You will also see the following message pops up on each of your streamers:

[![Allow adb usb debugging](https://techblog.co.il/wp-content/uploads/2023/04/usb-debug.png)](https://techblog.co.il/wp-content/uploads/2023/04/usb-debug.png)

Make sure to check the "Always allow from this computer" checkbox and click on the OK button. you will also need to restart the container.

## Working with ADB-API
ADB-API also includes OpenAPI swagger documentation to help you working with the system. with the swagger you will be able to test the api calls very easely.

To access the swagger documentation, add "docs" at the end of the server url. for example: http://[]server-address]:[port]/docs

[![adb-api swagger](https://techblog.co.il/wp-content/uploads/2023/04/adb-api-swagger.png)](https://techblog.co.il/wp-content/uploads/2023/04/adb-api-swagger.png)


## API Endpoints

* Get devices list: "/api/devices". returns json with registered devices.

```json

  "devices": [
    {
      "id": 1,
      "name": "Mibox Work-Room",
      "ip": "192.168.0.12",
      "port": 5555
    },
    {
      "id": 2,
      "name": "Mibox Parents",
      "ip": "192.168.0.235",
      "port": 5555
    }
  ]
}
```

* Get device properties: "/api/{device}/properties. returns json with device properties. the device parameter is the ip address of the streamer.

```json
{
  "net_bt_name": " Android",
   "persist_sys_locale": " he-IL",
  "persist_sys_media_avsync": " true",
  "persist_sys_timezone": " Asia/Jerusalem",
  "persist_sys_usb_config": " adb",
  "persist_sys_webview_vmsize": " 139176216",
  "pm_dexopt_ab-ota": " speed-profile",
  "pm_dexopt_bg-dexopt": " speed-profile",
  "pm_dexopt_boot": " verify",
  "pm_dexopt_first-boot": " quicken",
  "pm_dexopt_inactive": " verify",
  "pm_dexopt_install": " speed-profile",
  "pm_dexopt_priv-apps-oob": " false",
  "pm_dexopt_priv-apps-oob-list": " ALL",
  "pm_dexopt_shared": " speed",
  "ro_actionable_compatible_property_enabled": " true",
  "ro_adb_secure": " 1",
  "ro_allow_mock_location": " 0",
 "ro_boot_hardware": " amlogic",
  "ro_boot_oemkey1": " ATV00100021M19",
  "ro_boot_reboot_mode": " cold_boot",
  "ro_boot_rpmb_state": " 0",
  "ro_boot_selinux": " enforcing",
  "ro_boot_serialno": " 18554284042375",
  "ro_boot_vbmeta_avb_version": " 1.1",
  "ro_boot_vbmeta_device": " /dev/block/vbmeta",
  "ro_boot_vbmeta_device_state": " locked",
  "ro_bootimage_build_date": " Tue Sep 28 18",
  "ro_bootimage_build_date_utc": " 1632823795",
  "ro_bootimage_build_fingerprint": " Xiaomi/oneday/oneday",
  "ro_bootloader": " unknown",
  "ro_bootmode": " unknown",
  "ro_build_characteristics": " default",
  "ro_build_date": " Tue Sep 28 18",
  "ro_build_date_utc": " 1632823795",
  "ro_build_description": " oneday-user 9 PI 3933 release-keys",
  "ro_build_display_id": " PI.3933 release-keys",
  "ro_build_expect_bootloader": " 01.01.180822.145544",
  "ro_build_fingerprint": " Xiaomi/oneday/oneday",
  "ro_build_flavor": " oneday-user",
  "ro_build_host": " c5-mitv-bsp-build04.bj",
  "ro_build_id": " PI",
  "ro_build_software_version": " 21.9.28.3933",
  "ro_build_system_root_image": " true",
  "ro_build_user": " jenkins",
  "ro_build_version_preview_sdk": " 0",
  "ro_build_version_release": " 9",
  "ro_build_version_sdk": " 28",
  "ro_com_google_clientidbase": " android-xiaomi-tv",
  "ro_com_google_gmsversion": " Android_9_Pie",
  "ro_config_notification_sound": " pixiedust.ogg",
  "ro_product_brand": " Xiaomi",
  "ro_product_build_date": " Tue Sep 28 18",
  "ro_product_build_date_utc": " 1632823795",
  "ro_product_build_fingerprint": " Xiaomi/oneday/oneday",
  "ro_product_cpu_abi": " armeabi-v7a",
  "ro_product_cpu_abi2": " armeabi",
  "ro_product_cpu_abilist": " armeabi-v7a,armeabi",
  "ro_product_cpu_abilist32": " armeabi-v7a,armeabi",
  "ro_product_cpu_abilist64": " ",
  "ro_product_device": " oneday",
  "ro_product_first_api_level": " 28",
  "ro_product_locale": " en-US",
  "ro_product_manufacturer": " Xiaomi",
  "ro_product_model": " MIBOX4",
  "ro_product_name": " oneday",
  "ro_product_vendor_brand": " Xiaomi",
  "ro_product_vendor_device": " oneday",
  "ro_product_vendor_manufacturer": " Xiaomi",
  "ro_product_vendor_model": " MIBOX4",
  "ro_product_vendor_name": " oneday",

}
```

* Get device memory info: "/api/device/memory". returns the device memory info.

```json
{
  "MemTotal": "2034840 kB",
  "MemFree": "169388 kB",
  "MemAvailable": "1076044 kB",
  "Buffers": "30816 kB",
  "Cached": "996968 kB",
  "SwapCached": "0 kB",
  "Active": "911756 kB",
  "Inactive": "622644 kB",
  "Active(anon)": "508824 kB",
  "Inactive(anon)": "2156 kB",
  "Active(file)": "402932 kB",
  "Inactive(file)": "620488 kB",
  "Unevictable": "2340 kB",
  "Mlocked": "2340 kB",
  "SwapTotal": "262140 kB",
  "SwapFree": "262140 kB",
  "Dirty": "0 kB",
  "Writeback": "0 kB",
  "AnonPages": "508964 kB",
  "Mapped": "532488 kB",
  "Shmem": "2508 kB",
  "Slab": "106952 kB",
  "SReclaimable": "49936 kB",
  "SUnreclaim": "57016 kB",
  "KernelStack": "21504 kB",
  "PageTables": "27004 kB",
  "NFS_Unstable": "0 kB",
  "Bounce": "0 kB",
  "WritebackTmp": "0 kB",
  "CommitLimit": "1279560 kB",
  "Committed_AS": "23159644 kB",
  "VmallocTotal": "263061440 kB",
  "VmallocUsed": "0 kB",
  "VmallocChunk": "0 kB",
  "CmaTotal": "544768 kB",
  "CmaFree": "0 kB",
  "VmapStack": "5496 kB"
}
```

* Get the list of installed applications: "/api/{device}/app/3rd". returns list of installd application qith basic info.

```json
{
  "com.plexapp.android": {
    "appname": "Plex: Stream Movies & TV",
    "appurl": "https://play.google.com/store/apps/details?id=com.plexapp.android&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/slZYN_wnlAZ4BmyTZZakwfwAGm8JE5btL7u7AifhqCtUuxhtVVxQ1mcgpGOYC7MsAaU"
  },
  "il.co.yes.yesgo": {
    "appname": "yes+",
    "appurl": "https://play.google.com/store/apps/details?id=il.co.yes.yesgo&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/8AgNls4adb1Wsp4ZxGGoaSecwbiBT1wmY1cgRLEwjhltrlS2lNcanpXLT_5IidJpbA"
  },
  "il.co.stingtv.atv": {
    "appname": "STINGTV",
    "appurl": "https://play.google.com/store/apps/details?id=il.co.stingtv.atv&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/NrUvKI1NcsLk6_hNxZtxWENvDyuQNvTDvoJqZFmuuFrKcml-5bygxM_oJNyYyTFXBpo"
  },
  "miada.tv.webbrowser": {
    "appname": "Internet Web Browser",
    "appurl": "https://play.google.com/store/apps/details?id=miada.tv.webbrowser&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/wui_0K9RipIlFKLsSbAPFaI9-f6PA4INZ0GKZDThsi57Jm-Olw04T_pqtufhNaTKLw"
  },
  "com.spotify.tv.android": {
    "appname": "Spotify - Music and Podcasts",
    "appurl": "https://play.google.com/store/apps/details?id=com.spotify.tv.android&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/eN0IexSzxpUDMfFtm-OyM-nNs44Y74Q3k51bxAMhTvrTnuA4OGnTi_fodN4cl-XxDQc"
  },
  "com.greenshpits.RLive": {
    "appname": "Radio Live Israel radio online",
    "appurl": "https://play.google.com/store/apps/details?id=com.greenshpits.RLive&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/c5hWYKQ0BJioIyoPegJiibjz93PBYVGT0BUrRCoHvkx_bnqkBCQf91752R7BTKEzIro"
  },
  "com.android.chrome": {
    "appname": "Google Chrome: Fast & Secure",
    "appurl": "https://play.google.com/store/apps/details?id=com.android.chrome&hl=en&gl=il",
    "appimage": "https://play-lh.googleusercontent.com/KwUBNPbMTk9jDXYS2AeX3illtVRTkrKVh5xR1Mg4WHd0CG2tV4mrh1z3kXi5z_warlk"
  }
}
```

* Execute command: "/api/{device}/execute/{command}. returns the command output. for example, getting the current system volume.
The following command "settings get system volume_system" will result the following output:

```json
[
  "7"
]
```

* Send key events: "/api/{device}/{keyevent}". this command simulates one or more key press.
for example, running the sollowing command **"input keyevent 3"** will simulate clicking the **"Home"** button and **"input keyevent 25 25"** will simulate two clicks on the **"Volume Down"** button.

* Open Application: "/api/{device}/{app}/open". this command will open the requested application. for example, the following command **"/api/192.168.0.12/com.plexapp.android/open"** will open the "Plex" application.


## Usefull list of ADB Commands
I have published a list of usefull adb command [Here](https://gist.github.com/t0mer/37b384a37941c25d1e7206849b10967f).