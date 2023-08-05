#!/usr/bin/python
import re

filenames = open("testfilenames", "r")

for index, source_filename in enumerate(filenames):
    print("Start:         '" + source_filename.strip() + "'")

    # Strip newlines
    filename = source_filename.strip()

    # Lets remove any file extension
    filename_extension = ""
    try:
        regex = re.compile(r"(.*)(\.[a-zA-Z\d]{1,5}$)")
        filename_extension = regex.search(filename).group(2)
        filename = regex.sub(r"\1", filename)
    except:
        pass

    # Rationalize all dots and underscores into spaces
    try:
        regex = re.compile(r"[_\.]")
        filename = regex.sub(" ", filename)
    except:
        pass

    # Look for a release group tag
    # These are fairly reliably within [] at the start
    filename_release_group = ""
    try:
        regex = re.compile(r"^(\[(.+?)\]\s?)")
        filename_release_group = regex.search(filename).group(2)
        filename = regex.sub(r"\0", filename)
    except:
        pass

    # Some groups put a hash in the end, lets remove that
    filename_hash = ""
    try:
        regex = re.compile(r"\s?\[([\dA-Z]{8})\]$")
        filename_hash = regex.search(filename).group(1)
        filename = regex.sub(r"\0", filename)
    except:
        pass

    print("Release Group: '" + filename_release_group + "'")
    print("Extension:     '" + filename_extension + "'")
    print("Hash:          '" + filename_hash + "'")
    print("Filename:      '" + filename + "'")
    print("\n")
    if index == 10:
        break
