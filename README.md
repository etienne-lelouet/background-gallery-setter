# DESCRIPTION

A python script that regularly sets changes your background to a random picture from a directory you provide.

Supports multiple screens, and tries to match each picture to the best screen, based on the size of the image relative to the size of the screen.

# DEPENDENCIES (as debian testing packages)

```
python3-pil
feh
```

# TODO
- Proper argument parser
- Make it so that the program chooses the "best fit" for each screen
- Make a systemd unit
- Have proper logging
- Use `ImageMagick` to be cooler