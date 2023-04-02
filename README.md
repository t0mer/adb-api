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