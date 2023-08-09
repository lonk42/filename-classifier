#!/usr/bin/python
import argparse
import re

class Filename_Classifier():

    def __init__(self, source_filename, debug=False):
        self.source_filename = source_filename
        self.debug = debug

        self.filename_extension = ""
        self.filename_release_group = ""
        self.filename_hash = ""
        self.filename_audio_depth = ""
        self.filename_resolution = ""
        self.filename_rip_type = ""
        self.filename_encoding = ""
        self.filename_audio_format = ""
        self.filename_language = ""
        self.filename_season = ""
        self.filename_episode = ""
        self.filename_series = ""

        self.deconstruct_filename(self.source_filename)

        print("Release Group: '" + self.filename_release_group + "'")
        print("Extension:     '" + self.filename_extension + "'")
        print("Hash:          '" + self.filename_hash + "'")
        print("Resolution:    '" + self.filename_resolution + "'")
        print("Rip Type:      '" + self.filename_rip_type + "'")
        print("Audio Depth:   '" + self.filename_audio_depth + "'")
        print("Encoding:      '" + self.filename_encoding + "'")
        print("Language:      '" + self.filename_language + "'")
        print("Audio Format:  '" + self.filename_audio_format + "'")
        print("Series:        '" + self.filename_series + "'")
        print("Season:        '" + str(self.filename_season) + "'")
        print("Episode:       '" + str(self.filename_episode) + "'")
        print("\n")

    def deconstruct_filename(self, filename):
        # Strip newlines
        filename = filename.strip()

        # Lets remove any file extension
        regex = re.compile(r"\.([a-zA-Z\d]{1,5})$")
        match = regex.search(filename)
        if match is not None:
            self.filename_extension = match.group(1)
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
        regex = re.compile(r"^(\[(.+?)\]\s?)")
        match = regex.search(filename)
        if match is not None:
            self.filename_release_group = match.group(2)
            filename = regex.sub('', filename)

        # Some groups put a hash in the end, lets remove that
        regex = re.compile(r"\s?\[([\dA-Z]{8})\]")
        match = regex.search(filename)
        if match is not None:
            self.filename_hash = match.group(1)
            filename = regex.sub('', filename)

        # Look for a resolution
        valid_resolutions = [r"\s?[(\[](\d{3,4}p?)[)\]]\s?", r'\s?(480p)', r'\s?(720p)', r'\s?(1080p)', r'\s?(\d{3,4}[xX*]\d{3,4})']
        for resolution in valid_resolutions:
            regex = re.compile(resolution)
            match = regex.search(filename)
            if match is not None:
                self.filename_resolution = match.group(1)
                filename = regex.sub('', filename)

        # Look for a rip descriptor
        rip_list = [r'\s?([Bb][Ll][Uu]-?[Rr][Aa][Yy])', r'\s?(DVDRip)', r'\s?(\(DVD\))', r'\s?(DTS-HD)']
        for rip in rip_list:
            regex = re.compile(rip)
            match = regex.search(filename)
            if match is not None:
                self.filename_rip_type = match.group(1)
                filename = regex.sub('', filename)

        # Sometimes there is an audio depth
        audio_depth_list = [r'\s?(10-?[Bb][Ii][Tt])']
        for audio_depth in audio_depth_list:
            regex = re.compile(audio_depth)
            match = regex.search(filename)
            if match is not None:
                self.filename_audio_depth = match.group(1)
                filename = regex.sub('', filename)

        # Sometimes there is an encoding standard
        encoding_list = [r'\s?([Hhx]26[45])', r'(divx\d{1,4})']
        for encoding in encoding_list:
            regex = re.compile(encoding)
            match = regex.search(filename)
            if match is not None:
                self.filename_encoding = match.group(1)
                filename = regex.sub('', filename)

        # Or an audio format
        audio_formats = [r'\s?(AAC)', r'\s?(AC3)']
        for audio_format in audio_formats:
            regex = re.compile(audio_format)
            match = regex.search(filename)
            if match is not None:
                self.filename_audio_format = match.group(1)
                filename = regex.sub('', filename)

        # Langauges
        language_list = [r'\s?([Dd]ual-?[Aa]udio)']
        for language in language_list:
            regex = re.compile(language)
            match = regex.search(filename)
            if match is not None:
                self.filename_language = match.group(1)
                filename = regex.sub('', filename)

        # Discard any garbage that we may have left behind and not matched on
        garbage_list = [r'\s?\[.*\]', r'\s?\(.*\)', r'\s?iAHD']
        for garbage in garbage_list:
            regex = re.compile(garbage)
            filename = regex.sub('', filename)

        # Detect tv style season and episode strings
        regex = re.compile(r'\s?([Ss][Ee]?([\d]{1,4})\s?[Ee][Pp]?([\d]{1,4}))\s?')
        match = regex.search(filename)
        if match is not None:
            self.filename_season = int(match.group(2))
            self.filename_episode = int(match.group(3))
            filename = regex.sub('', filename)

        # If we are left with the pattern ' - 123.5' we know what to do
        regex = re.compile(r'\s?-\s?([\d]{1,4})(\.\d|v\d)?\s?$')
        match = regex.search(filename)
        if match is not None:
            self.filename_episode = int(match.group(1))
            filename = regex.sub('', filename)

        # Seasons can also be identified as 'S2'
        regex = re.compile(r'[\s-]{1,2}[Ss]E?([\d]{1,3})\s?$')
        match = regex.search(filename)
        if match is not None:
            self.filename_season = int(match.group(1))
            filename = regex.sub('', filename)

        # If we don't have an episode number yet we might be dash delimited, fix that
        if self.filename_episode == '':
            regex = re.compile(r"-")
            filename = regex.sub(" ", filename).strip()

            # A number at the end might be our episode now
            regex = re.compile(r"\s?([\d]{1,4})(\.\d|v\d)?$")
            match = regex.search(filename)
            if match is not None:
                self.filename_episode = int(match.group(1))
                filename = regex.sub('', filename)

        # Kill all dashes anyway
        regex = re.compile(r"-")
        filename = regex.sub(" ", filename).strip()

        # At this point the only left possibly left is the series name
        self.filename_series = filename

# Parse arguments and launch daemon
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filename Classifier, deconstruct common filenames into datasets")
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    parser.add_argument('filenames', metavar='filename(s)', nargs='+', help='Filenames to parse')
    arguments = parser.parse_args()

    for filename in arguments.filenames:
        Filename_Classifier(filename, arguments.debug)