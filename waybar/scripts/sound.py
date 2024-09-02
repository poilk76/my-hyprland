#!/usr/bin/env python3
from json import dumps, loads
from subprocess import check_output

data = {"text":'󰓃',"tooltip":""}

with open("/home/main/.config/waybar/scripts/mem.json", 'r') as f:

    mem = loads(f.read())

volume = check_output('wpctl get-volume @DEFAULT_AUDIO_SINK@', shell=True, text=True).replace("\n", "")

if volume.split(" ")[-1] == "[MUTED]":
    
    data["text"] = f' '
    data["tooltip"] += f'Volume: MUTED'

elif mem["volume"] != str(float(volume.replace("\n","").split(" ")[-1])*100).split('.')[0]:

    mem["volume"] = str(float(volume.replace("\n","").split(" ")[-1])*100).split('.')[0]

    if mem["volume"] != "0":data["text"] = f'{mem["volume"]}%'
    elif int(mem["volume"]) <= 50: data["text"] = f'{mem["volume"]}%'
    else: data["text"] = f'{mem["volume"]}%'

    with open("/home/main/.config/waybar/scripts/mem.json", 'w') as f:

        f.write(dumps(mem))
    data["tooltip"] += f'Volume: {mem["volume"]}%'
else:
    if mem["volume"] != "0":data["text"] = f' '
    elif int(mem["volume"]) <= 50: data["text"] = f' '
    else: data["text"] = f' '
    data["tooltip"] += f'Volume: {mem["volume"]}%'


print(dumps(data), flush=True)