#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

FILE_PATH = sys.argv[1]
# FILE_PATH = "Robot_Maker_Faire_150pc_0.2mm_PLA_Ender-3_100_20h42m3.gcode"

# first_layer_height
global FIRST_LAYER_H
FIRST_LAYER_H = ''
global FIRST_LAYER_H_CLEAN
FIRST_LAYER_H_CLEAN = ''

FIRST_MOVE_GCODE = 'G1 X'

REPLACEMENT = ''
COMBINE_ALERT = '; Combine Z and XY move\n'

global FIRST_MOVE_PATCHED
FIRST_MOVE_PATCHED = False
global COMBINE_ALERT_PATCHED
COMBINE_ALERT_PATCHED = False

global HEADER
HEADER = '; END Header'
global AFTER_HEADER
AFTER_HEADER = False

DEBUG = False

# Open input file
file_input = open(FILE_PATH, "r")
# Open output file
file_output = open(FILE_PATH + ".new", "w")

print('Searching for layer height...')

for search_line in file_input:
  if 'first_layer_height = ' in search_line:
    get_first_layer_height = search_line.split("=")
    get_first_layer_height = get_first_layer_height[1].rstrip("\n").lstrip(" ")
    FIRST_LAYER_H = 'G1 Z' + get_first_layer_height
    FIRST_LAYER_H_CLEAN = 'Z' + get_first_layer_height
  elif COMBINE_ALERT in search_line:
    COMBINE_ALERT_PATCHED = True


print('Layer height found')
print('File: ' + FILE_PATH)
print('First layer height:' + get_first_layer_height)
print('Layer height marker: "' + FIRST_LAYER_H + '"')
print('Adding layer height to first XY move...')


# Move cursor to begining
file_input.seek(0)

# Modify file
for line in file_input:
  if DEBUG:
    print('Line: ' + line)
  if HEADER in line and AFTER_HEADER is False:
    AFTER_HEADER = True
  if FIRST_LAYER_H in line and FIRST_MOVE_PATCHED is False and AFTER_HEADER is True:
    if DEBUG:
      print('############################')
      print('Match found in line: ' + line)
      print('############################')
    if DEBUG:
      print('Replaced line' + REPLACEMENT)
      print('-------------------------------------')
    file_output.write(REPLACEMENT)
  elif FIRST_MOVE_GCODE in line and FIRST_MOVE_PATCHED is False and FIRST_LAYER_H_CLEAN not in line and COMBINE_ALERT_PATCHED is False and AFTER_HEADER is True:
    if DEBUG:
      print('####################')
      print('Patching first move')
      print('Old first move: ' + line)
      print('New first move: ' + line[0:line.rfind(";")].rstrip() + ' ' + FIRST_LAYER_H_CLEAN + ' ' + line[line.rfind(";"):len(line)].rstrip("/n"))
    file_output.write(line[0:line.rfind(";")].rstrip() + ' ' + FIRST_LAYER_H_CLEAN + ' ' + line[line.rfind(";"):len(line)].rstrip("/n"))
    FIRST_MOVE_PATCHED = True
  else:
    file_output.write(line)

print('Completed update')
print('Saving file...')
# Close files
file_input.close()
file_output.close()

# Replace files
os.remove(FILE_PATH)
os.rename(FILE_PATH + ".new", FILE_PATH)
print('File saved.')
