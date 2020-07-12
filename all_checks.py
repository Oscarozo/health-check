#!/usr/bin/env python3.8
import sys
import os
import shutil
import socket


def check_reboot():
    """Returns true if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")


def check_disk_full(disk, min_gb, min_percent):
    """Returns true if there isnt enough space"""
    du = shutil.disk_usage(disk)
    # Calculate percentage of free space
    percent_free = 100 * du.free / du.total
    # calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False


def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full("/", min_gb=2, min_percent=10)


def check_no_network():
    """Returns True if it fails to resolve Google's URL"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main():
    checks = [
        (check_reboot, "Pending reboot."),
        (check_root_full, "root partition full."),
        (check_no_network, "No working network :(")
    ]

    everything_ok = True

    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)

    print("Everythin is ok...")
    sys.exit(0)


main()
