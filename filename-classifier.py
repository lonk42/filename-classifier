#!/usr/bin/python
import re

filenames = open("allfilenamescut", "r")

for index, source_filename in enumerate(filenames):
    print("Start:         '" + source_filename.strip() + "'")

    # Strip newlines
    filename = source_filename.strip()

    # Lets remove any file extension
    filename_extension = ""
    regex = re.compile(r"\.([a-zA-Z\d]{1,5})$")
    match = regex.search(filename)
    if match is not None:
        filename_extension = match.group(1)
        filename = regex.sub('', filename)

    # If the episode number was revised e.g. '06.5' we want to save this for later
    regex = re.compile(r"(\d{1,4})\.(\d)")
    match = regex.search(filename)
    if match is not None:
        filename = regex.sub(r'\1%\2', filename)

    # Rationalize all dots and underscores into spaces]
    regex = re.compile(r"[_\.]")
    filename = regex.sub(" ", filename)

    # Fix placeholde % with dots
    regex = re.compile(r"(\d{1,4})%(\d)")
    filename = regex.sub(r"\1.\2", filename)

    # Look for a release group tag
    # These are fairly reliably within [] at the start
    filename_release_group = ""
    regex = re.compile(r"^(\[(.+?)\]\s?)")
    match = regex.search(filename)
    if match is not None:
        filename_release_group = match.group(2)
        filename = regex.sub('', filename)

    # Some groups put a hash in the end, lets remove that
    filename_hash = ""
    regex = re.compile(r"\s?\[([\dA-Z]{8})\]")
    match = regex.search(filename)
    if match is not None:
        filename_hash = match.group(1)
        filename = regex.sub('', filename)

    # Look for a resolution
    filename_resolution = ""
    valid_resolutions = [r"\s?[(\[](\d{3,4}p?)[)\]]\s?", r'\s?(480p)', r'\s?(720p)', r'\s?(1080p)', r'\s?(\d{3,4}[xX*]\d{3,4})']
    for resolution in valid_resolutions:
        regex = re.compile(resolution)
        match = regex.search(filename)
        if match is not None:
            filename_resolution = match.group(1)
            filename = regex.sub('', filename)

    # Look for a rip descriptor
    filename_rip_type = ""
    rip_list = [r'\s?([Bb][Ll][Uu]-?[Rr][Aa][Yy])', r'\s?(DVDRip)', r'\s?(\(DVD\))', r'\s?(DTS-HD)']
    for rip in rip_list:
        regex = re.compile(rip)
        match = regex.search(filename)
        if match is not None:
            filename_rip_type = match.group(1)
            filename = regex.sub('', filename)

    # Sometimes there is an audio depth
    filename_audio_depth = ""
    audio_depth_list = [r'\s?(10-?[Bb][Ii][Tt])']
    for audio_depth in audio_depth_list:
        regex = re.compile(audio_depth)
        match = regex.search(filename)
        if match is not None:
            filename_audio_depth = match.group(1)
            filename = regex.sub('', filename)

    # Sometimes there is an encoding standard
    filename_encoding = ""
    encoding_list = [r'\s?([Hhx]26[45])', r'(divx\d{1,4})']
    for encoding in encoding_list:
        regex = re.compile(encoding)
        match = regex.search(filename)
        if match is not None:
            filename_encoding = match.group(1)
            filename = regex.sub('', filename)

    # Or an audio format
    filename_audio_format = ""
    audio_formats = [r'\s?(AAC)', r'\s?(AC3)']
    for audio_format in audio_formats:
        regex = re.compile(audio_format)
        match = regex.search(filename)
        if match is not None:
            filename_audio_format = match.group(1)
            filename = regex.sub('', filename)

    # Langauges
    filename_language = ""
    language_list = [r'\s?([Dd]ual-?[Aa]udio)']
    for language in language_list:
        regex = re.compile(language)
        match = regex.search(filename)
        if match is not None:
            filename_language = match.group(1)
            filename = regex.sub('', filename)

    # To save some trouble we will only allow alphanumeric and simple symbols
    #regex = re.compile(r'[^a-zA-Z0-9!#$&\s\[\]\(\)-_]+')
    #filename = regex.sub('', filename)

    # Discard any garbage that we may have left behind and not matched on
    garbage_list = [r'\s?\[.*\]', r'\s?\(.*\)', r'\s?iAHD']
    for garbage in garbage_list:
        regex = re.compile(garbage)
        filename = regex.sub('', filename)

    # Detect tv style season and episode strings
    filename_season = ""
    filename_episode = ""
    regex = re.compile(r'\s?([Ss][Ee]?([\d]{1,4})\s?[Ee][Pp]?([\d]{1,4}))\s?')
    match = regex.search(filename)
    if match is not None:
        filename_season = int(match.group(2))
        filename_episode = int(match.group(3))
        filename = regex.sub('', filename)

    # If we are left with the pattern ' - 123.5' we know what to do
    regex = re.compile(r'\s?-\s?([\d]{1,4})(\.\d|v\d)?\s?$')
    match = regex.search(filename)
    if match is not None:
        filename_episode = int(match.group(1))
        filename = regex.sub('', filename)

    # Seasons can also be identified as 'S2'
    regex = re.compile(r'[\s-]{1,2}[Ss]E?([\d]{1,3})\s?$')
    match = regex.search(filename)
    if match is not None:
        filename_season = int(match.group(1))
        filename = regex.sub('', filename)

    # If we don't have an episode number yet we might be dash delimited, fix that
    if filename_episode == '':
        regex = re.compile(r"-")
        filename = regex.sub(" ", filename).strip()

        # A number at the end might be our episode now
        regex = re.compile(r"\s?([\d]{1,4})(\.\d|v\d)?$")
        match = regex.search(filename)
        if match is not None:
            filename_episode = int(match.group(1))
            filename = regex.sub('', filename)

    # Kill all dashes anyway
    regex = re.compile(r"-")
    filename = regex.sub(" ", filename).strip()

    # At this point the only left possibly left is the series name
    filename_series = filename

    print("Release Group: '" + filename_release_group + "'")
    print("Extension:     '" + filename_extension + "'")
    print("Hash:          '" + filename_hash + "'")
    print("Resolution:    '" + filename_resolution + "'")
    print("Rip Type:      '" + filename_rip_type + "'")
    print("Audio Depth:   '" + filename_audio_depth + "'")
    print("Encoding:      '" + filename_encoding + "'")
    print("Language:      '" + filename_language + "'")
    print("Audio Format:  '" + filename_audio_format + "'")
    print("Series:        '" + filename_series + "'")
    print("Season:        '" + str(filename_season) + "'")
    print("Episode:       '" + str(filename_episode) + "'")
    print("\n")

    if index == 2:
        break
