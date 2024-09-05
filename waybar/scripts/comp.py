#!/usr/bin/env python3
from json import dumps, loads
from subprocess import check_output


def cpu_temp() -> int:
    
    temp = check_output("cat /sys/class/thermal/thermal_zone*/temp", shell=True, text=True).split("\n")

    return int(temp[0][:2])

def disk_free():

    data = check_output("df -H /dev/sda2 | grep disk", shell=True, text=True).split("  ")

    return data[3]


def cpu_usage() -> float:

    cpu = check_output("cat /proc/stat | grep cpu", shell=True, text=True).split("\n")
    cpu = cpu[0].split(" ")

    calc = (int(cpu[2]) / int(cpu[5])) * 100.0

    return calc

def cpu_model() -> str:

    return check_output('cat /proc/cpuinfo | grep "model name"', shell=True, text=True).split("\n")[0].split(":")[-1]

def ram_usage():

    totalRam = check_output("cat /proc/meminfo | grep MemTotal", shell=True, text=True).split(" ")[-2]
    freeRam = check_output("cat /proc/meminfo | grep MemFree", shell=True, text=True).split(" ")[-2]

    calc = 100 - ((int(freeRam) / int(totalRam)) * 100)

    return (float(str(calc).split(".")[0]+"."+str(calc).split(".")[1][:1]), (int(totalRam)-int(freeRam)),totalRam)

def drawing(data:list) -> list:

    chars:list = ['╭','╮','╰','╯','─','│']

    treasholders = create_treasholders(data)

    result = [f" {str(treasholders[4-i]*1.0)[:4]}% |" for i in range(5)]

    for i in range(len(data)-1):
        position = get_position(data[i], treasholders)
        next_position = get_position(data[i+1], treasholders)
        result[position] += chars[-2]
        for j in range(5):
            if j != position:
                result[j] += " "
        if position == next_position:
            result[position] += chars[-2]
            for j in range(5):
                if j != next_position:
                    result[j] += " "
        elif position > next_position:
            result[position] += chars[3]
            result[next_position] += chars[0]
            for j in range(5):
                if j != position and j != next_position and j in [x for x in range(next_position+1,position)]:
                    result[j] += chars[-1]
                elif j != position and j != next_position:
                    result[j] += " "
        else:
            result[position] += chars[1]
            result[next_position] += chars[2]
            for j in range(5):
                if j != position and j != next_position and j in [x for x in range(position+1,next_position)]:
                    result[j] += chars[-1]
                elif j != position and j != next_position:
                    result[j] += " "

    for i in range(5):
        result[i] += " |\n"

    return result

def get_position(val, ref) -> int:

    if val > ref[4]:
        return 0
    elif val > ref[3]:
        return 1
    elif val > ref[2]:
        return 2
    elif val > ref[1]:
        return 3
    else:
        return 4
    
def create_treasholders(data):

    treasholders = [min(data)]

    calc = (max(data) - min(data)) / 5.0

    for i in range(4):
        treasholders.append(treasholders[-1]+calc)

    return treasholders
    
def cpu_data(mem) -> tuple:
    
    data:str = "CPU stats:\n"

    usage_val = cpu_usage()

    alarm = False

    if cpu_temp() >= 80: alarm = True

    data += f' Model:{cpu_model()}  \n'
    data += f' Temperature: {cpu_temp()}°C\n'
    data += f' Usage:                 {str(cpu_usage())[:4]}%\n'

    if len(mem["cpu_usage"]) >= 20:
        mem["cpu_usage"].pop(0)
    
    mem["cpu_usage"].append(usage_val)

    for line in drawing(mem["cpu_usage"]):
        data += line


    return (data,mem,alarm)

def ram_data(mem) -> tuple:

    data = "\nRAM stats:\n"

    usage = ram_usage()

    data += f' Usage:           {int(usage[1]/1024)}MB/{int(int(usage[2])/1024)}MB {usage[0]}%\n'

    if len(mem["ram_usage"]) >= 20:
        mem["ram_usage"].pop(0)
    
    mem["ram_usage"].append(int(usage[0]))

    for line in drawing(mem["ram_usage"]):
        data += line
    
    return (data,mem)

def disk_data():

    data = "\nDISK stats:\n"

    data += f" Free: {disk_free()} "

    return data

def main() -> dict:
    
    data:dict = {"text":"󰍹","tooltip":""}

    with open("/home/main/.config/waybar/scripts/mem.json", 'r') as f:
        mem = loads(f.read())

    cpu = cpu_data(mem)
    ram = ram_data(mem)
    data["tooltip"] += cpu[0]
    mem = cpu[1]
    if cpu[2]: data["text"] = "<span color='#ff1500'>󰍹</span>"
    data["tooltip"] += ram[0]
    mem = ram[1]
    data["tooltip"] += disk_data()
    data["tooltip"] = data['tooltip'][:-1]

    with open("/home/main/.config/waybar/scripts/mem.json", 'w') as f:
        f.write(dumps(mem))

    return data

print(dumps(main()), flush=True)
