#!/usr/bin/env python3
from json import dumps
from subprocess import check_output


def return_temperature() -> int:
    
    temp = check_output("cat /sys/class/thermal/thermal_zone*/temp", shell=True, text=True).split("\n")

    return int(temp[0][:2])

def return_cpu_usage() -> float:

    cpu = check_output("cat /proc/stat | grep cpu", shell=True, text=True).split("\n")
    cpu = cpu[0].split(" ")

    calc = (int(cpu[2]) / int(cpu[5])) * 100

    return float(str(calc).split(".")[0]+"."+str(calc).split(".")[1][:1])

def return_ram_usage() -> float:

    totalRam = check_output("cat /proc/meminfo | grep MemTotal", shell=True, text=True).split(" ")[-2]
    freeRam = check_output("cat /proc/meminfo | grep MemFree", shell=True, text=True).split(" ")[-2]

    calc = 100 - ((int(freeRam) / int(totalRam)) * 100)

    return float(str(calc).split(".")[0]+"."+str(calc).split(".")[1][:1])

def critical_check() -> dict:

    data = {"text":"","tooltip":""}

    value = return_cpu_usage()
    if value >= 80.0:
        data["text"] = '<span color="#ff8000"></span>'
        data["tooltip"] += f'CPU usage: <span color="#ff8000">{value}%</span>\n'
    else:
        data["tooltip"] += f'CPU usage: {value}%\n'
    value = return_ram_usage()
    if value >= 80.0:
        data["text"] = '<span color="#ff8000"></span>'
        data["tooltip"] += f'RAM usage: <span color="#ff8000">{value}%</span>\n'
    else:
        data["tooltip"] += f'RAM usage: {value}%\n'
    value = return_temperature()
    if value >= 80:
        data["text"] = '<span color="#ff1500"></span>'
        data["tooltip"] += f'CPU temp: <span color="#ff1500">{value}°C</span>'
    else:
        data["tooltip"] += f'CPU temp:  {value}°C'

    return data




print(dumps(critical_check()), flush=True)