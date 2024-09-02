#!/usr/bin/env python3

from datetime import datetime
from os import system

now = datetime.now()

if int(now.hour) <= 18 and int(now.hour) >= 7:
    with open("/home/main/.config/hypr/hyprpaper.conf", "w") as f:
        f.write("""
preload = /home/main/.config/hypr/wallpaper-day.jpg
wallpaper = eDP-1, /home/main/.config/hypr/wallpaper-day.jpg
                """)
    system("hyprpaper")
else:
    with open("/home/main/.config/hypr/hyprpaper.conf", "w") as f:
        f.write("""
preload = /home/main/.config/hypr/wallpaper-night.jpg
wallpaper = eDP-1, /home/main/.config/hypr/wallpaper-night.jpg
                """)
    system("hyprpaper")