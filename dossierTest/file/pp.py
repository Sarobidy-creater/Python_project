#!/usr/bin/python3

import xml.dom.minidom
import re
import os
import getopt
import sys

xspf_files = dict()
fs_files = list()

def print_usage(progname):
    print(f"Usage: {progname} [options] <directory> <xspf file> ... <xspf file>")
    print("Options:")
    print("  -c   No ANSI color coding")
    print("  -n   No count prefix")

def xspf_parse(playlist_filename, handler):
    xml_data = xml.dom.minidom.parse(playlist_filename)
    for playlist in xml_data.getElementsByTagName("playlist"):
        for tracklist in playlist.getElementsByTagName("trackList"):
            for track in tracklist.getElementsByTagName("track"):
                for location in track.getElementsByTagName("location"):
                    data = re.sub(r"%([0-9a-fA-F]{2})", 
                        lambda x: chr(int(x.group(1), 16)), 
                        location.firstChild.data)
                    track_filename = data.replace("file://", "")
                    handler(playlist_filename, track_filename)

def add_xspf_file(playlist_filename, track_filename):
    if track_filename not in xspf_files:
        xspf_files[track_filename] = list()
    xspf_files[track_filename].append(playlist_filename)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(list(filter(None, sys.argv[1:])), "hcn", ["help", "no-color", "no-count"])
    except getopt.GetoptError as err:
        print(str(err))
        print_usage(sys.argv[0])
        sys.exit(1)

    if len(args) < 2:
        print_usage(sys.argv[0])
        sys.exit(1)

    print_color = True
    print_count = True
    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage(sys.argv[0])
            sys.exit(1)
        elif o in ("-c", "--no-color"):
            print_color = False
        elif o in ("-n", "--no-count"):
            print_count = False

    for filename in args[1:]:
        xspf_parse(filename, add_xspf_file)

    for root, dirs, files in os.walk(args[0]):
        for filename in files:
            fs_files.append(os.path.join(root, filename))

    for fs_file in sorted(fs_files):
        if fs_file in xspf_files:
            count = len(xspf_files[fs_file])
            if count > 1:
                if print_count:
                    sys.stdout.write(f"{count} ")
                if print_color:
                    sys.stdout.write("\x1B[32;1m")  # Green bold
                sys.stdout.write(fs_file)
                if print_color:
                    sys.stdout.write("\x1B[0m")
                sys.stdout.write("\n")
            else:
                if print_count:
                    sys.stdout.write("1 ")
                if print_color:
                    sys.stdout.write("\x1B[32m")  # Green
                sys.stdout.write(fs_file)
                if print_color:
                    sys.stdout.write("\x1B[0m")
                sys.stdout.write("\n")
        else:
            if print_count:
                sys.stdout.write("0 ")
            sys.stdout.write(fs_file)
            sys.stdout.write("\n")

    sys.exit(0)
