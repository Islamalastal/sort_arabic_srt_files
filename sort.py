"""
script to sort content of arabic srt & text files by time stamp.
@author: Islam Alastal
@date: 13.12.2021
python-version: 3.8
"""

from pathlib import Path
import glob
import re
import os

# set working directory
FILE_PATH = Path(__file__).parent.resolve()
os.chdir(FILE_PATH)


def get_files():
    """function to get all txt and srt files at current directory"""
    # allowed file types
    fileTypes = ("*.txt", "*.srt")
    # files list
    files = []
    for file in fileTypes:
        files.extend(glob.glob(file))
    return files


def sort(files):
    """
    get all lines of each file and sort them by time.
    """
    # main loop, working with all files
    for file in files:
        # open orginal file 
        with open(file, 'r+', encoding="utf-8") as outfile:
            # open new file for the new changes
            with open("0_" + file + "_edited.txt", "w+", encoding="utf-8") as edited_file:
                # some needed variables 
                lines_counter = 0
                next_line = 0
                blocks = {}
                perv_line = ""
                # checking all lines in current file
                for line in outfile:
                    lines_counter +=1

                    # add current line if last line has been matched
                    # means: add text line, if last line was a time stamp line
                    if next_line == lines_counter:
                        blocks[perv_line] = line
                    
                    # reqular expression to get lines with time stamp
                    pattern = r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d"

                    # if time stamp has been natche -> add it as a key in dictionary blocks 
                    matched = re.findall(pattern, line)
                    if matched:
                        for line in matched:
                            blocks[line] = ""
                            # set next line counter  -> 
                            # to use it to save next line after matching this line successfully
                            next_line = lines_counter+1
                    perv_line = line
                
                # sort dictionary by keys (time stamps)
                # and add time stamps & lines to a new file
                dictionary_items = blocks.items()
                for key, value in sorted(dictionary_items):
                    edited_file.write(key+"\n")
                    edited_file.write(value+"\n")


if __name__ == "__main__":
    files = get_files()
    sort(files)
