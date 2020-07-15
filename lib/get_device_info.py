import re
import subprocess

from lib.console import console_out


def devices_list():
    detected_devices = subprocess.Popen('adb devices', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        shell=True).stdout.read()
    detected_devices = detected_devices.decode()
    detected_devices = re.split('[\n\r]', detected_devices)
    detected_devices.remove("List of devices attached")
    while "" in detected_devices:
        detected_devices.remove("")
    duts = list()
    console_out("\nADB connection details:")
    for dev in detected_devices:
        dev = dev.split("\t")
        if dev[-1] == "device":
            duts.append(dev[0])
            print("Device %s connected successfully, manufacturer: %s, model: %s, android version: %s."
                  % (dev[0], manufacturer(dev[0]), model(dev[0]), android_version(dev[0])))
        if dev[-1] == "offline":
            print("Device %s is offline, please check device status and reconnect it." % dev[0])
        if dev[-1] == "unauthorized":
            print("Device %s is unauthorized, please reconnect it and allow the USB debug permission." % dev[0])
    print("Total %s devices detected, %s devices online" % (str(len(detected_devices)), str(len(duts))))
    return duts


def manufacturer(device_id):
    manufacturer_name = subprocess.Popen('adb -s ' + device_id + ' shell getprop ro.product.manufacturer',
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read()
    manufacturer_name = manufacturer_name.decode()
    manufacturer_name = manufacturer_name.strip()
    return str(manufacturer_name)


def model(device_id):
    model_name = subprocess.Popen('adb -s ' + device_id + ' shell getprop ro.product.model',
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read()
    model_name = model_name.decode()
    model_name = model_name.strip()
    return str(model_name)


def android_version(device_id):
    android_version_code = subprocess.Popen('adb -s ' + device_id + ' shell getprop ro.build.version.release',
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True).stdout.read()
    android_version_code = android_version_code.decode().strip()
    return str(android_version_code)
