#!/usr/bin/python3

import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager

import psutil

"""
Provide a blurred screenshot for i3lock.

This script screenshots each monitor, blurs it, adds a lock icon,
and uses this as the background for i3lock to have a "blurred screen"
lock effect.
"""

# The lock file to prevent multiple lock screens from triggering
LOCK_FILE_PATH = f"/tmp/{os.geteuid()}-lockscreen.lock"

# The image of a lock to superimpose on the screenshots
LOCK_IMAGE_PATH = "/usr/local/scripts/dat/lock.png"

# Regular expression for monitor dimensions from xrandr
MONITOR_DIMENSION_REGEX = re.compile(
    r"^([\w\-]+) connected [^\d]*(\d+)x(\d+)\+(\d+)\+(\d+)",
)

# The pixelation effect. These two numbers need to multiply to 10,000.
SMALL_SCALE_PERCENT = 5
LARGE_SCALE_PERCENT = 2000
assert SMALL_SCALE_PERCENT * LARGE_SCALE_PERCENT == 10000


@contextmanager
def lock_file(path):
    file = open(path, "x")
    try:
        yield
    finally:
        file.close()
        os.remove(path)


class Monitor:
    def __init__(self, name, width, height, offset_x, offset_y):
        self.name = name
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def size_and_position(self):
        return f"{self.width}x{self.height}+{self.offset_x}+{self.offset_y}"

    def position(self):
        return f"+{self.offset_x}+{self.offset_y}"

    def filename(self, directory):
        return os.path.join(directory, f"{self.name}.png")

    def __hash__(self):
        return hash(self.name)


def get_monitors_dimensions():
    monitors = []
    xrandr_output = subprocess.check_output(["xrandr", "--query"], encoding="utf-8")
    for line in xrandr_output.splitlines():
        match = MONITOR_DIMENSION_REGEX.match(line)
        if match is None:
            # Not a connected monitor, skip
            continue

        name = match[1]
        width = int(match[2])
        height = int(match[3])
        offset_x = int(match[4])
        offset_y = int(match[5])
        monitors.append(Monitor(name, width, height, offset_x, offset_y))

    return monitors


def capture_and_blur(directory, monitor):
    image_output = monitor.filename(directory)
    proc_screenshot = subprocess.Popen(
        ["maim", "-u", f"--geometry={monitor.size_and_position()}", "/dev/stdout"],
        stdout=subprocess.PIPE,
    )
    proc_convert = subprocess.Popen(
        [
            "convert",
            "/dev/stdin",
            "-scale",
            f"{SMALL_SCALE_PERCENT}%",
            "-scale",
            f"{LARGE_SCALE_PERCENT}%",
            "/dev/stdout",
        ],
        stdin=proc_screenshot.stdout,
        stdout=subprocess.PIPE,
    )
    proc_composite = subprocess.Popen(
        [
            "composite",
            "-gravity",
            "Center",
            LOCK_IMAGE_PATH,
            "/dev/stdin",
            image_output,
        ],
        stdin=proc_convert.stdout,
        stdout=subprocess.DEVNULL,
    )
    return proc_composite


def merge_images(directory, monitors):
    full_output = os.path.join(directory, "image.png")

    # Screenshot full desktop as base image
    # This is guaranteed to have the correct dimensions we need
    subprocess.check_call(["maim", "-u", full_output])

    for monitor in monitors:
        # Impose the partial image on the incomplete one
        image_input = monitor.filename(directory)
        subprocess.check_call(
            [
                "convert",
                full_output,
                image_input,
                "-geometry",
                monitor.position(),
                "-compose",
                "over",
                "-composite",
                full_output,
            ],
        )

    return full_output


def run_i3lock(image_path):
    subprocess.check_call(["i3lock", "-i", image_path])


def turn_off_screen():
    subprocess.check_call(["xset", "dpms", "force", "suspend"])


def i3lock_running():
    for proc in psutil.process_iter():
        if proc.name() == "i3lock":
            return True
    return False


def perform_lock():
    with lock_file(LOCK_FILE_PATH):
        with tempfile.TemporaryDirectory(prefix="lockscreen-") as directory:
            # Get monitor data
            monitors = get_monitors_dimensions()

            # Start blur jobs
            processes = []
            for monitor in monitors:
                processes.append(capture_and_blur(directory, monitor))

            # Wait for jobs
            for process in processes:
                process.communicate()

            # Merge images and display i3lock
            image_path = merge_images(directory, monitors)
            run_i3lock(image_path)
            turn_off_screen()


if __name__ == "__main__":
    if not i3lock_running():
        perform_lock()
