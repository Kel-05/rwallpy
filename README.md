# rwallpy
It's a python script that randomly applies a wallpaper every TIME seconds. It can filter the pool by category (aka directory) and by brightness (dark or light wallpaper). It can also dinamically change brightness based on the time of day!

It assumes your wallpaper directory to be `~/Pictures/Wallpapers` and your wallpaper backend to be `swww`. These arguments can be changed via the `-d` and `-e` option respectively.

# Dependencies

```
pip install pillow
```

# Usage

```
> rwallpy -h
usage: rwallpy [-h] [-t TIME] [-c CATEGORY] [-d DIRECTORY] [-e EXEC] [-b {dark,light} | -B]

Change wallpaper randomly every TIME seconds.

options:
  -h, --help            show this help message and exit
  -t, --time TIME       Time in seconds to change wallpaper.
  -c, --category CATEGORY
                        Category of wallpaper.
  -d, --directory DIRECTORY
                        Directory containing wallpapers.
  -e, --exec EXEC       Command to execute to set wallpaper.
  -b, --brightness {dark,light}
                        Brightness of wallpaper. Can be either 'dark' or 'light'.
  -B                    Change brightness based on time of day.
```

You can either execute it manually in the background (`./main.py &`) or execute it automatically every new session via a wm (eg. `exec-once = /path/to/main.py` for hyprland).

Don't forget to `chmod +x main.py`!
