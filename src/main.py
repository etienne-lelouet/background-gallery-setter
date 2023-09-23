#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
from screen import Screen, get_screens
import subprocess
import random
import time
import sys

basefolder = sys.argv[1]
sleep_timer = int(sys.argv[2])

supported_files = [ "PNG", "JPEG" ]

feh_cmdline = [ "feh", "--no-fehbg", "--bg-max" ]

def filter_isfile(file_path):
    return file_path.is_file()

def filter_format(file_path):
    return Image.open(file_path).format in supported_files

def main():

    basefolder = sys.argv[1]
    sleep_timer = int(sys.argv[2])
    print(basefolder)
    print(sleep_timer)
    
    files = filter(filter_isfile, Path(basefolder).iterdir())
    images = list(filter(filter_format, files))
    random.shuffle(images)
    
    cur_index = 0
    
    while True:
        print("new loop")
        screens = get_screens()
        screens.sort(key=lambda screen: screen.index)
        cur_cmdline = [ "feh", "--no-fehbg", "--bg-max" ]
        
        for screen in screens:
            print(screen)
            cur_img = images[cur_index]
            
            while not Path.exists(cur_img):
                print("removing %s" % cur_img)
                cur_img.remove(current_index)
            
            cur_cmdline.append(screen.resize_if_needed(cur_img))
            cur_index = (cur_index + 1) % len(images)
            print("cur_index = %d, len(images) = %d" % (cur_index, len(images)))
            
            print(*cur_cmdline)
            feh_res = subprocess.run(cur_cmdline)
            if feh_res.returncode != 0:
                print("feh failed to run")
                exit(1)
        
        time.sleep(sleep_timer)
        
        

