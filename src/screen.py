import re
from PIL import Image
import subprocess

re_screenindex = re.compile(r"^\s*([0-9])+:.*$")
re_screenname = re.compile(r"\s(\S+)$")
re_witdhheight = re.compile(r"^\s*[0-9]+:\s*\+\*?\S+\s+([0-9]+)/[0-9]+x([0-9]+)/[0-9]+.*$")

def get_screen_index(xrandr_line):
    screen_index_match = re_screenindex.findall(xrandr_line)
    
    if len(screen_index_match) != 1:
        print("failed to match index for %s" % xrandr_line)
        exit(1)
        
    if screen_index_match[0].isdigit():
        return int(screen_index_match[0])
    
    print("failed to convert index to int for %s" % xrandr_line)
    exit(1)

def get_screen_name(xrandr_line):
    screen_name_match = re_screenname.findall(xrandr_line)
    
    if len(screen_name_match) != 1:
        print("failed to match screen name for %s" % xrandr_line)
        exit(1)
    
    return screen_name_match[0]

def get_screen_resolution(xrandr_line):
    screen_res_match = re_witdhheight.findall(xrandr_line)
    
    if len(screen_res_match) != 1:
        print("failed to match screen width and height for %s" % xrandr_line)
        exit(1)

    if len(screen_res_match[0]) != 2:
        print("failed to match screen width and height for %s" % xrandr_line)
        exit(1)
    
    if screen_res_match[0][0].isdigit() and screen_res_match[0][1].isdigit():
        return int(screen_res_match[0][0]), int(screen_res_match[0][1])
    
    print("failed to convert width or height to int for %s" % xrandr_line)
    exit(1)

class Screen:
    def __init__(self, xrandr_line):
        self.index = get_screen_index(xrandr_line)
        self.name = get_screen_name(xrandr_line)
        self.width, self.height = get_screen_resolution(xrandr_line)
        
    def __str__(self):
        return "Screen index : %d, name: %s, %dx%d" % (self.index, self.name, self.width, self.height)

    def create_img(self, img):
        print("creating canvas with size %dx%d" % (self.width, self.height))
        canvas = Image.new('RGB', (self.width, self.height))
        x_coord = int((self.width - img.width) / 2)
        y_coord = int((self.height - img.height) / 2)
        print("pasting image at coordinates %d, %d", (x_coord, y_coord))
        canvas.paste(img, (x_coord, y_coord))
        name = "/tmp/%s.jpeg" % self.name
        print("saving image as %s" % name)
        canvas.save(name)
        return name
        

    def resize_if_needed(self, img_path):
        img = Image.open(img_path)
        img_width = img.width
        img_height = img.height
        
        print("%s: image %s is %dx%d" % (self, img_path, img_width, img_height))

        if img_width < self.width or img_height < self.height:
            print("%s is too small (%d, %d) for screen %s, creating canvas and centering" % (img_path, img_width, img_height, self))
            return self.create_img(img)
    
        return img_path


def get_screens():
    xrandr_res = subprocess.run(["xrandr", "--listmonitors"], stdout=subprocess.PIPE)

    if xrandr_res.returncode != 0:
        print("xrandr failed to run")
        exit(1)

    screen_strs = xrandr_res.stdout.decode("utf-8").splitlines()[1:]
    
    screens = []
    
    for screen_str in screen_strs:
        print(screen_str)
        screens.append(Screen(screen_str))

    return screens
