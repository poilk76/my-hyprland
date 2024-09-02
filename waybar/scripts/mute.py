#!/usr/bin/env python3
from subprocess import check_output
from os import system

volume = check_output('wpctl get-volume @DEFAULT_AUDIO_SINK@', shell=True, text=True).replace("\n", "")

if volume.split(" ")[-1] == "[MUTED]":
    system('wpctl set-mute @DEFAULT_AUDIO_SINK@ 0')
else:
    system('wpctl set-mute @DEFAULT_AUDIO_SINK@ 1')