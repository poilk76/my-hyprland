#!/usr/bin/env python3
from json import dumps, loads
from subprocess import check_output


def cpu_temp() -> int:
    
    temp = check_output("cat /sys/class/thermal/thermal_zone*/temp", shell=True, text=True).split("\n")

    return int(temp[0][:2])

def cpu_usage() -> float:

    cpu = check_output("cat /proc/stat | grep cpu", shell=True, text=True).split("\n")
    cpu = cpu[0].split(" ")

    calc = (int(cpu[2]) / int(cpu[5])) * 100

    return float(str(calc).split(".")[0]+"."+str(calc).split(".")[1][:1])

def cpu_model() -> str:

    return check_output('cat /proc/cpuinfo | grep "model name"', shell=True, text=True).split("\n")[0].split(":")[-1]

def ram_usage():

    totalRam = check_output("cat /proc/meminfo | grep MemTotal", shell=True, text=True).split(" ")[-2]
    freeRam = check_output("cat /proc/meminfo | grep MemFree", shell=True, text=True).split(" ")[-2]

    calc = 100 - ((int(freeRam) / int(totalRam)) * 100)

    return (float(str(calc).split(".")[0]+"."+str(calc).split(".")[1][:1]), (int(totalRam)-int(freeRam)),totalRam)

def drawing(data:list) -> list:

    chars:list = ['╭','╮','╰','╯','─','│']

    result = [" 100% | "," 80 % | "," 60 % | "," 40 % | "," 20 % | "]

    for i in range(len(data)-1):
        position = get_position(data[i])
        next_position = get_position(data[i+1])
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

def get_position(val:int) -> int:

    if val > 80:
        return 0
    elif val > 60:
        return 1
    elif val > 40:
        return 2
    elif val > 20:
        return 3
    elif val > 0:
        return 4
    
def cpu_data(mem) -> tuple:
    
    data:str = "CPU stats:\n"

    usage_val = cpu_usage()

    data += f' Model:{cpu_model()}  \n'
    data += f' Temperature: {cpu_temp()}°C\n'
    data += f' Usage:                 {cpu_usage()}%\n'

    if len(mem["cpu_usage"]) >= 20:
        mem["cpu_usage"].pop(0)
    
    mem["cpu_usage"].append(int(usage_val))

    for line in drawing(mem["cpu_usage"]):
        data += line


    return (data,mem)

def ram_data(mem) -> tuple:

    data = "RAM stats:\n"

    usage = ram_usage()

    data += f' Usage:           {int(usage[1]/1024)}MB/{int(int(usage[2])/1024)}MB {usage[0]}%\n'

    if len(mem["ram_usage"]) >= 20:
        mem["ram_usage"].pop(0)
    
    mem["ram_usage"].append(int(usage[0]))

    for line in drawing(mem["ram_usage"]):
        data += line
    
    return (data,mem)

def main() -> dict:
    
    data:dict = {"text":"󰍹","tooltip":""}

    with open("/home/main/.config/waybar/scripts/mem.json", 'r') as f:
        mem = loads(f.read())

    cpu = cpu_data(mem)
    ram = ram_data(mem)
    data["tooltip"] += cpu[0]
    mem = cpu[1]
    data["tooltip"] += ram[0]
    mem = ram[1]

    with open("/home/main/.config/waybar/scripts/mem.json", 'w') as f:
        f.write(dumps(mem))

    return data

print(dumps(main()), flush=True)
