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

adb help // List all comands

== Adb Server
adb kill-server
adb start-server 

== Adb Reboot
adb reboot
adb reboot recovery 
adb reboot-bootloader
adb root //restarts adb with root permissions

== Shell
adb shell    // Open or run commands in a terminal on the host Android device.

== Devices
adb usb
adb devices   //show devices attached
adb devices -l //devices (product/model)
adb connect ip_address_of_device

== Get device android version
adb shell getprop ro.build.version.release 

== LogCat
adb logcat
adb logcat -c // clear // The parameter -c will clear the current logs on the device.
adb logcat -d > [path_to_file] // Save the logcat output to a file on the local system.
adb bugreport > [path_to_file] // Will dump the whole device information like dumpstate, dumpsys and logcat output.

== Files
adb push [source] [destination]    // Copy files from your computer to your phone.
adb pull [device file location] [local file location] // Copy files from your phone to your computer.

== App install
adb -e install path/to/app.apk

-d                        - directs command to the only connected USB device...
-e                        - directs command to the only running emulator...
-s <serial number>        ...
-p <product name or path> ...
The flag you decide to use has to come before the actual adb command:

adb devices | tail -n +2 | cut -sf 1 | xargs -IX adb -s X install -r com.myAppPackage // Install the given app on all connected devices.

== Uninstalling app from device
adb uninstall com.myAppPackage
adb uninstall <app .apk name>
adb uninstall -k <app .apk name> -> "Uninstall .apk withour deleting data"

adb shell pm uninstall com.example.MyApp
adb shell pm clear [package] // Deletes all data associated with a package.

adb devices | tail -n +2 | cut -sf 1 | xargs -IX adb -s X uninstall com.myAppPackage //Uninstall the given app from all connected devices

== Update app
adb install -r yourApp.apk  //  -r means re-install the app and keep its data on the device.
adb install –k <.apk file path on computer> 

== Home button
adb shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN

== Activity Manager
adb shell am start -a android.intent.action.VIEW
adb shell am broadcast -a 'my_action'

adb shell am start -a android.intent.action.CALL -d tel:+972527300294 // Make a call

// Open send sms screen with phone number and the message:
adb shell am start -a android.intent.action.SENDTO -d sms:+972527300294   --es  sms_body "Test --ez exit_on_sent false

// Reset permissions
adb shell pm reset-permissions -p your.app.package 
adb shell pm grant [packageName] [ Permission]  // Grant a permission to an app. 
adb shell pm revoke [packageName] [ Permission]   // Revoke a permission from an app.


// Emulate device
adb shell wm size 2048x1536
adb shell wm density 288
// And reset to default
adb shell wm size reset
adb shell wm density reset

== Print text
adb shell input text 'Wow, it so cool feature'

== Screenshot
adb shell screencap -p /sdcard/screenshot.png

$ adb shell
shell@ $ screencap /sdcard/screen.png
shell@ $ exit
$ adb pull /sdcard/screen.png

---
adb shell screenrecord /sdcard/NotAbleToLogin.mp4

$ adb shell
shell@ $ screenrecord --verbose /sdcard/demo.mp4
(press Control + C to stop)
shell@ $ exit
$ adb pull /sdcard/demo.mp4

== Key event
adb shell input keyevent 3 // Home btn
adb shell input keyevent 4 // Back btn
adb shell input keyevent 5 // Call
adb shell input keyevent 6 // End call
adb shell input keyevent 26  // Turn Android device ON and OFF. It will toggle device to on/off status.
adb shell input keyevent 27 // Camera
adb shell input keyevent 64 // Open browser
adb shell input keyevent 66 // Enter
adb shell input keyevent 67 // Delete (backspace)
adb shell input keyevent 207 // Contacts
adb shell input keyevent 220 / 221 // Brightness down/up
adb shell input keyevent 277 / 278 /279 // Cut/Copy/Paste

0 -->  "KEYCODE_0" 
1 -->  "KEYCODE_SOFT_LEFT" 
2 -->  "KEYCODE_SOFT_RIGHT" 
3 -->  "KEYCODE_HOME" 
4 -->  "KEYCODE_BACK" 
5 -->  "KEYCODE_CALL" 
6 -->  "KEYCODE_ENDCALL" 
7 -->  "KEYCODE_0" 
8 -->  "KEYCODE_1" 
9 -->  "KEYCODE_2" 
10 -->  "KEYCODE_3" 
11 -->  "KEYCODE_4" 
12 -->  "KEYCODE_5" 
13 -->  "KEYCODE_6" 
14 -->  "KEYCODE_7" 
15 -->  "KEYCODE_8" 
16 -->  "KEYCODE_9" 
17 -->  "KEYCODE_STAR" 
18 -->  "KEYCODE_POUND" 
19 -->  "KEYCODE_DPAD_UP" 
20 -->  "KEYCODE_DPAD_DOWN" 
21 -->  "KEYCODE_DPAD_LEFT" 
22 -->  "KEYCODE_DPAD_RIGHT" 
23 -->  "KEYCODE_DPAD_CENTER" 
24 -->  "KEYCODE_VOLUME_UP" 
25 -->  "KEYCODE_VOLUME_DOWN" 
26 -->  "KEYCODE_POWER" 
27 -->  "KEYCODE_CAMERA" 
28 -->  "KEYCODE_CLEAR" 
29 -->  "KEYCODE_A" 
30 -->  "KEYCODE_B" 
31 -->  "KEYCODE_C" 
32 -->  "KEYCODE_D" 
33 -->  "KEYCODE_E" 
34 -->  "KEYCODE_F" 
35 -->  "KEYCODE_G" 
36 -->  "KEYCODE_H" 
37 -->  "KEYCODE_I" 
38 -->  "KEYCODE_J" 
39 -->  "KEYCODE_K" 
40 -->  "KEYCODE_L" 
41 -->  "KEYCODE_M" 
42 -->  "KEYCODE_N" 
43 -->  "KEYCODE_O" 
44 -->  "KEYCODE_P" 
45 -->  "KEYCODE_Q" 
46 -->  "KEYCODE_R" 
47 -->  "KEYCODE_S" 
48 -->  "KEYCODE_T" 
49 -->  "KEYCODE_U" 
50 -->  "KEYCODE_V" 
51 -->  "KEYCODE_W" 
52 -->  "KEYCODE_X" 
53 -->  "KEYCODE_Y" 
54 -->  "KEYCODE_Z" 
55 -->  "KEYCODE_COMMA" 
56 -->  "KEYCODE_PERIOD" 
57 -->  "KEYCODE_ALT_LEFT" 
58 -->  "KEYCODE_ALT_RIGHT" 
59 -->  "KEYCODE_SHIFT_LEFT" 
60 -->  "KEYCODE_SHIFT_RIGHT" 
61 -->  "KEYCODE_TAB" 
62 -->  "KEYCODE_SPACE" 
63 -->  "KEYCODE_SYM" 
64 -->  "KEYCODE_EXPLORER" 
65 -->  "KEYCODE_ENVELOPE" 
66 -->  "KEYCODE_ENTER" 
67 -->  "KEYCODE_DEL" 
68 -->  "KEYCODE_GRAVE" 
69 -->  "KEYCODE_MINUS" 
70 -->  "KEYCODE_EQUALS" 
71 -->  "KEYCODE_LEFT_BRACKET" 
72 -->  "KEYCODE_RIGHT_BRACKET" 
73 -->  "KEYCODE_BACKSLASH" 
74 -->  "KEYCODE_SEMICOLON" 
75 -->  "KEYCODE_APOSTROPHE" 
76 -->  "KEYCODE_SLASH" 
77 -->  "KEYCODE_AT" 
78 -->  "KEYCODE_NUM" 
79 -->  "KEYCODE_HEADSETHOOK" 
80 -->  "KEYCODE_FOCUS" 
81 -->  "KEYCODE_PLUS" 
82 -->  "KEYCODE_MENU" 
83 -->  "KEYCODE_NOTIFICATION" 
84 -->  "KEYCODE_SEARCH" 
85 -->  "KEYCODE_MEDIA_PLAY_PAUSE"
86 -->  "KEYCODE_MEDIA_STOP"
87 -->  "KEYCODE_MEDIA_NEXT"
88 -->  "KEYCODE_MEDIA_PREVIOUS"
89 -->  "KEYCODE_MEDIA_REWIND"
90 -->  "KEYCODE_MEDIA_FAST_FORWARD"
91 -->  "KEYCODE_MUTE"
92 -->  "KEYCODE_PAGE_UP"
93 -->  "KEYCODE_PAGE_DOWN"
94 -->  "KEYCODE_PICTSYMBOLS"
...
122 -->  "KEYCODE_MOVE_HOME"
123 -->  "KEYCODE_MOVE_END"
// https://developer.android.com/reference/android/view/KeyEvent.html


== ShPref
# replace org.example.app with your application id

# Add a value to default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.PUT --es key key_name --es value "hello world!"'

# Remove a value to default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.REMOVE --es key key_name'

# Clear all default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.CLEAR --es key key_name'

# It's also possible to specify shared preferences file.
adb shell 'am broadcast -a org.example.app.sp.PUT --es name Game --es key level --ei value 10'

# Data types
adb shell 'am broadcast -a org.example.app.sp.PUT --es key string --es value "hello world!"'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key boolean --ez value true'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key float --ef value 3.14159'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key int --ei value 2015'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key long --el value 9223372036854775807'

# Restart application process after making changes
adb shell 'am broadcast -a org.example.app.sp.CLEAR --ez restart true'

== Monkey
adb shell monkey -p com.myAppPackage -v 10000 -s 100 // monkey tool is generating 10.000 random events on the real device

== Paths
/data/data/<package>/databases (app databases)
/data/data/<package>/shared_prefs/ (shared preferences)
/data/app (apk installed by user)
/system/app (pre-installed APK files)
/mmt/asec (encrypted apps) (App2SD)
/mmt/emmc (internal SD Card)
/mmt/adcard (external/Internal SD Card)
/mmt/adcard/external_sd (external SD Card)

adb shell ls (list directory contents)
adb shell ls -s (print size of each file)
adb shell ls -R (list subdirectories recursively)

== Device onformation
adb get-statе (print device state)
adb get-serialno (get the serial number)
adb shell dumpsys iphonesybinfo (get the IMEI)
adb shell netstat (list TCP connectivity)
adb shell pwd (print current working directory)
adb shell dumpsys battery (battery status)
adb shell pm list features (list phone features)
adb shell service list (list all services)
adb shell dumpsys activity <package>/<activity> (activity info)
adb shell ps (print process status)
adb shell wm size (displays the current screen resolution)
dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp' (print current app's opened activity)

== Package info
adb shell list packages (list package names)
adb shell list packages -r (list package name + path to apks)
adb shell list packages -3 (list third party package names)
adb shell list packages -s (list only system packages)
adb shell list packages -u (list package names + uninstalled)
adb shell dumpsys package packages (list info on all apps)
adb shell dump <name> (list info on one package)
adb shell path <package> (path to the apk file)

==Configure Settings Commands
adb shell dumpsys battery set level <n> (change the level from 0 to 100)
adb shell dumpsys battery set status<n> (change the level to unknown, charging, discharging, not charging or full)
adb shell dumpsys battery reset (reset the battery)
adb shell dumpsys battery set usb <n> (change the status of USB connection. ON or OFF)
adb shell wm size WxH (sets the resolution to WxH)


== Device Related Commands
adb reboot-recovery (reboot device into recovery mode)
adb reboot fastboot (reboot device into recovery mode)
adb shell screencap -p "/path/to/screenshot.png" (capture screenshot)
adb shell screenrecord "/path/to/record.mp4" (record device screen)
adb backup -apk -all -f backup.ab (backup settings and apps)
adb backup -apk -shared -all -f backup.ab (backup settings, apps and shared storage)
adb backup -apk -nosystem -all -f backup.ab (backup only non-system apps)
adb restore backup.ab (restore a previous backup)
adb shell am start|startservice|broadcast <INTENT>[<COMPONENT>]
-a <ACTION> e.g. android.intent.action.VIEW
-c <CATEGORY> e.g. android.intent.category.LAUNCHER (start activity intent)

adb shell am start -a android.intent.action.VIEW -d URL (open URL)
adb shell am start -t image/* -a android.intent.action.VIEW (opens gallery)

== Logs
adb logcat [options] [filter] [filter] (view device log)
adb bugreport (print bug reports)

== Other
adb backup // Create a full backup of your phone and save to the computer.
adb restore // Restore a backup to your phone.
adb sideload //  Push and flash custom ROMs and zips from your computer.

fastboot devices
// Check connection and get basic information about devices connected to the computer.
// This is essentially the same command as adb devices from earlier. 
//However, it works in the bootloader, which ADB does not. Handy for ensuring that you have properly established a connection.


--------------------------------------------------------------------------------
Shared Preferences

# replace org.example.app with your application id

# Add a value to default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.PUT --es key key_name --es value "hello world!"'

# Remove a value to default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.REMOVE --es key key_name'

# Clear all default shared preferences.
adb shell 'am broadcast -a org.example.app.sp.CLEAR --es key key_name'

# It's also possible to specify shared preferences file.
adb shell 'am broadcast -a org.example.app.sp.PUT --es name Game --es key level --ei value 10'

# Data types
adb shell 'am broadcast -a org.example.app.sp.PUT --es key string --es value "hello world!"'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key boolean --ez value true'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key float --ef value 3.14159'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key int --ei value 2015'
adb shell 'am broadcast -a org.example.app.sp.PUT --es key long --el value 9223372036854775807'

# Restart application process after making changes
adb shell 'am broadcast -a org.example.app.sp.CLEAR --ez restart true'
--------------------------------------------------------------------------------

=== Few bash snippets ===
@Source (https://jonfhancock.com/bash-your-way-to-better-android-development-1169bc3e0424)

=== Using tail -n
//Use tail to remove the first line. Actually two lines. The first one is just a newline. The second is “List of devices attached.”
$ adb devices | tail -n +2

=== Using cut -sf
// Cut the last word and any white space off the end of each line.
$ adb devices | tail -n +2 | cut -sf -1

=== Using xargs -I
// Given the -I option, xargs will perform an action for each line of text that we feed into it.
// We can give the line a variable name to use in commands that xargs can execute.
$ adb devices | tail -n +2 | cut -sf -1 | xargs -I X echo X aw yiss

=== Three options below together
// Will print android version of all connected devices
adb devices | tail -n +2 | cut -sf -1 | xargs -I X adb -s X shell getprop ro.build.version.release  

=== Using alias
-- Example 1 
alias tellMeMore=echo
tellMeMore "hi there"
Output => hi there
-- Example 2
// Define alias
alias apkinstall="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X install -r $1"
// And you can use it later 
apkinstall ~/Downloads/MyAppRelease.apk  // Install an apk on all devices
-- Example 3
alias rmapp="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X uninstall $1"
rmapp com.example.myapp // Uninstall a package from all devices
-- Example 4
alias clearapp="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X shell pm clear $1"
clearapp com.example.myapp  // Clear data on all devices (leave installed)
-- Example 5
alias startintent="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X shell am start $1"
startintent https://twitter.com/JonFHancock // Launch a deep link on all devices


Setting up your .bash_profile
Finally, to make this all reusable even after rebooting your computer (aliases only last through the current session), we have to add these to your .bash_profile. You might or might not already have a .bash_profile, so let’s make sure we append to it rather than overwriting it. Just open a terminal, and run the following command

touch .bash_profile && open .bash_profile

This will create it if it doesn’t already exist, and open it in a text editor either way. Now just copy and paste all of the aliases into it, save, and close.

alias startintent="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X shell am start $1"
alias apkinstall="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X install -r $1"
alias rmapp="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X uninstall $1"
alias clearapp="adb devices | tail -n +2 | cut -sf 1 | xargs -I X adb -s X shell pm clear $1"


===============================================================
Sources:
- Internet
- https://www.automatetheplanet.com/adb-cheat-sheet/