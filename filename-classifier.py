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
        regex = re.compile(r"\.([a-zA-Z\d]{1,5})$")
        match = regex.search(filename)
        if match is not None:
            filename_extension = match.group(1)
            filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Rationalize all dots and underscores into spaces]
    try:
        regex = re.compile(r"[_\.]")
        filename = regex.sub(" ", filename)
    except ValueError:
        print(ValueError)
        
    # Look for a release group tag
    # These are fairly reliably within [] at the start
    filename_release_group = ""
    try:
        regex = re.compile(r"^(\[(.+?)\]\s?)")
        match = regex.search(filename)
        if match is not None:
            filename_release_group = match.group(2)
            filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Some groups put a hash in the end, lets remove that
    filename_hash = ""
    try:
        regex = re.compile(r"\s?\[([\dA-Z]{8})\]")
        match = regex.search(filename)
        if match is not None:
            filename_hash = match.group(1)
            filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Look for a resolution
    valid_resolutions = [r"\s?[(\[](\d{3,4}p?)[)\]]\s?", r'\s?(480p)', r'\s?(720p)', r'\s?(1080p)', r'\s?(\d{3,4}[xX*]\d{3,4})']
    try:
        for resolution in valid_resolutions:
            regex = re.compile(resolution)
            match = regex.search(filename)
            if match is not None:
                filename_resolution = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)
    
    # Look for a rip descriptor
    filename_rip_type = ""
    rip_list = [r'\s?([Bb][Ll][Uu]-?[Rr][Aa][Yy])', r'\s?(DVDRip)', r'\s?(\(DVD\))', r'\s?(DTS-HD)']
    try:
        for rip in rip_list:
            regex = re.compile(rip)
            match = regex.search(filename)
            if match is not None:
                filename_rip_type = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Sometimes there is an audio depth
    filename_audio_depth = ""
    audio_depth_list = [r'\s?(10-?[Bb][Ii][Tt])']
    try:
        for audio_depth in audio_depth_list:
            regex = re.compile(audio_depth)
            match = regex.search(filename)
            if match is not None:
                filename_audio_depth = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Sometimes there is an audio depth
    filename_encoding = ""
    encoding_list = [r'\s?([Hhx]26[45])']
    try:
        for encoding in encoding_list:
            regex = re.compile(encoding)
            match = regex.search(filename)
            if match is not None:
                filename_encoding = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Or an audio format
    filename_audio_format = ""
    audio_formats = [r'\s?(AAC)']
    try:
        for audio_format in audio_formats:
            regex = re.compile(audio_format)
            match = regex.search(filename)
            if match is not None:
                filename_audio_format = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Langauges
    filename_language = ""
    language_list = [r'\s?([Dd]ual-?[Aa]udio)']
    try:
        for language in language_list:
            regex = re.compile(language)
            match = regex.search(filename)
            if match is not None:
                filename_language = match.group(1)
                filename = regex.sub(r"\0", filename)
    except ValueError:
        print(ValueError)

    # Finally any garbage that we may have left behind and not matched on
    garbage_list = [r'\s?\[\]', r'\s?\(\)', r'\s?iAHD']
    for garbage in garbage_list:
        regex = re.compile(garbage)
        match = regex.search(filename)
        if match is not None:
            filename = regex.sub(r"\0", filename)

    print("Release Group: '" + filename_release_group + "'")
    print("Extension:     '" + filename_extension + "'")
    print("Hash:          '" + filename_hash + "'")
    print("Resolution:    '" + filename_resolution + "'")
    print("Rip Type:      '" + filename_rip_type + "'")
    print("Audio Depth:   '" + filename_audio_depth + "'")
    print("Encoding:      '" + filename_encoding + "'")
    print("Language:      '" + filename_language + "'")
    print("Audio Format:  '" + filename_audio_format + "'")
    print("Filename:      '" + filename + "'")
    print("\n")
    if index == 10:
        break
