from pathlib import Path

basefolder = "/media/nas/Images/wallpaper"

for curFile in Path(basefolder).iterdir():
    print(curFile)
