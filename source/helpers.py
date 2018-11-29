import subprocess
import time
from random import random


def get_tag():
    """Get a random tag from tags.txt file"""
    with open('tags.txt', 'r') as f:
        tags = list(f.readlines())
        tag = random.choice(tags)
    return tag.strip()


def get_place():
    """Get a random geolocation from places.txt file"""
    with open('places.txt', 'r') as f:
        places = list(f.readlines())
        place = random.choice(places)
    return place.strip()


def write_username_to_file(username):
    timestr = time.strftime("%Y-%m-%d")
    filename = f"usernames{timestr}.txt"
    with open(filename, "a") as f:
        f.write(username + "\n")


def kill_process():
    """Kill chromedriver process"""
    subprocess.call("killall chromedriver", shell=True)
