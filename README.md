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

## How to Use ADB-API
ADB-API also includes OpenAPI swagger documentation to help you working with the system. with the swagger you will be able to test the api calls very easely.

[![adb-api swagger](https://techblog.co.il/wp-content/uploads/2023/04/adb-api-swagger.png)](https://techblog.co.il/wp-content/uploads/2023/04/adb-api-swagger.png)

