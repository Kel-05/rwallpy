#!/usr/bin/env python3

from datetime import datetime
from PIL import Image
import subprocess
import argparse
import random
import time
import os


def calculate_brightness(image_path):
    """
    Calculates the brightness of an image.

    :param image_path: Path to the image file.
    :return: Average brightness of the image.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to grayscale
        grayscale_img = img.convert("L")
        
        # Get pixel data
        pixel_values = list(grayscale_img.getdata())
        
        # Calculate average brightness
        avg_brightness = sum(pixel_values) / len(pixel_values)
        
        return avg_brightness
    except Exception as e:
        print(f"Error: {e}")
        return -1

    
class Wallpaper:
    theme = "*"
    
    def __init__(self, path):
        self.path = path
        self.name = path.split("/")[-1]
        self.category = path.split("/")[-2]

        
    def check_brightness(self):

        if calculate_brightness(self.path) < 128:
            self.theme = "dark"
        else:
            self.theme = "light"

            
    def __str__(self):
        return f"Wallpaper: {self.name}\n\t" \
            f"Path: {self.path}\n\t" \
            f"Category: {self.category}\n\t" \
            f"Theme: {self.theme}"


def get_wallpapers(directory):
    wallpapers = []

    for root, _, files in os.walk(directory):
        for file in files:
            
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)
                wallpapers.append(Wallpaper(path))

    return wallpapers
    
    
def set_wallpaper(path, exec):
    command = exec.split() + [path]
    
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

        
def main():

    # Parse command line arguments
    
    parser = argparse.ArgumentParser(description="Change wallpaper randomly every TIME seconds.")
    b_group = parser.add_mutually_exclusive_group()

    parser.add_argument("-t", "--time",
                        type=int,
                        default=30,
                        help="Time in seconds to change wallpaper.")

    parser.add_argument("-c", "--category",
                        type=str,
                        default="*",
                        help="Category of wallpaper.")

    parser.add_argument("-d", "--directory",
                        type=str,
                        default="~/Pictures/Wallpapers",
                        help="Directory containing wallpapers.")

    parser.add_argument("-e", "--exec",
                        type=str,
                        default="swww img -t any",
                        help="Command to execute to set wallpaper.")

    b_group.add_argument("-b", "--brightness",
                         type=str,
                         default="*",
                         choices=["dark", "light"],
                         help="Brightness of wallpaper. Can be either 'dark' or 'light'.")

    b_group.add_argument("-B",
                         nargs="?",
                         const="08:00 20:00",
                         default=False,
                         help="Change brightness based on time of day. "
                         "You can optionally specify day time and night time [HH:MM HH:MM].")
    
    argv = parser.parse_args()

    
    # Load wallpapers
    
    print("Collecting wallpapers...")
    
    if argv.directory.startswith("~"):
        argv.directory = os.path.expanduser(argv.directory)
    
    if not os.path.isdir(argv.directory):
        print(f"Error: '{argv.directory}' is not a directory")
        exit(1)

        
    wallpapers       = get_wallpapers(argv.directory)
    wlen             = len(wallpapers)
                
    if wlen == 0:
        print("No wallpapers found")
        exit(1)

        
    print(f"Wallpapers collected: {wlen}")

    
    # Filter wallpapers, if necessary
    
    if argv.category != "*":
        print(f"Filtering wallpapers by category: {argv.category}")
        wallpapers = [w for w in wallpapers if w.category == argv.category]

    if argv.brightness != "*":
        print(f"Filtering wallpapers by brightness: {argv.brightness}")
        print("Calculating brightness of wallpapers...")

        for w in wallpapers:
            w.check_brightness()
        
        wallpapers = [w for w in wallpapers if w.theme == argv.brightness]

        
    if argv.B and len(argv.B.split()) >= 2:
        print("Filtering wallpapers dynamically based on time of day...")

        daytime   = datetime.strptime(argv.B.split()[0], "%H:%M").time()
        nighttime = datetime.strptime(argv.B.split()[1], "%H:%M").time()

        print(f"Day time: {daytime}\n"
              f"Night time: {nighttime}")
        
        print("Calculating brightness of wallpapers...")
        
        for w in wallpapers:
            w.check_brightness()

        dark_wallpapers = [w for w in wallpapers if w.theme == "dark"]
        light_wallpapers = [w for w in wallpapers if w.theme == "light"]

        print(f"Dark wallpapers: {len(dark_wallpapers)}")
        print(f"Light wallpapers: {len(light_wallpapers)}")

        if len(dark_wallpapers) == 0 or len(light_wallpapers) == 0:
            print("No wallpapers found for either theme")
            exit(1)

        
    wlen = len(wallpapers)
        
    if wlen == 0:
        print("No wallpapers found")
        exit(1)

        
    print(f"Wallpapers total: {wlen}")


    # Main loop, change wallpaper randomly every TIME seconds
    
    print(f"Changing wallpaper every {argv.time} seconds...", flush=True)
    
    my_wallpapers = wallpapers
    
    while(True):
        time.sleep(argv.time)

        if argv.B and len(argv.B.split()) >= 2:
            current_time = datetime.now().time()
            
            if daytime < current_time < nighttime and argv.brightness != "light":
                print("Changing to day time\n"
                      "Wallpaper theme: light", flush=True)
                
                argv.brightness = "light"
                my_wallpapers = light_wallpapers
            elif (current_time < daytime or current_time > nighttime) and argv.brightness != "dark":
                print("Changing to night time\n"
                      "Wallpaper theme: dark", flush=True)
                
                argv.brightness = "dark"
                my_wallpapers = dark_wallpapers

                
        wallpaper = random.choice(my_wallpapers)

        print(f"Wallpaper chosen:\n\t"
              f"name: {wallpaper.name}\n\t"
              f"category: {wallpaper.category}\n\t"
              f"theme: {wallpaper.theme}", flush=True)
        
        set_wallpaper(wallpaper.path, argv.exec)
        
    
if __name__ == "__main__":
    main()
