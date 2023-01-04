import os
import sys
from datetime import datetime
import math
import xml.etree.ElementTree as ET


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def read_settings():
    filetypes = None
    filename = None
    filesize = 0
    startstop = None

    tree = ET.parse('settings.xml')
    root = tree.getroot()

    for filetype in root.findall('filetype'):
        if filetypes == None:
            filetypes = []
        filetypes.append(filetype.text)

    try:
        start = root.find("starthour").text.split(":")
        stop = root.find("stophour").text.split(":")
        startstop = (int(int(start[0]) * 60 + int(start[1])), int(int(stop[0]) * 60 + int(stop[1])))
    except:
        pass
    try:
        filesize = int(root.find("filesize").text)
    except:
        pass
    try:
        filename = str(root.find("nameregex").text) + ".*"
    except:
        pass

    return filetypes, filename, filesize, startstop


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def danger(var):
    if var == True:
        return "success"
    else:
        return "danger"

def saved(var):
    if var == True:
        return "Saved"
    else:
        return "Unsaved"