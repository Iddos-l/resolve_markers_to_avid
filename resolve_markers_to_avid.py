#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Script exports markers to Avid Media Composer
# generats a tab delimited file to import in Avid
#
# Iddos, Bootqe color studio, iddolahman@gmail.com


import os, csv
from pathlib import Path as path
from python_get_resolve import GetResolve

desDir = path.home() / 'temp'
if not path.exists(desDir):
    desDir.mkdir()
os.chdir(desDir)

def frames2TC (frames, fps, offset):
    h = str(int((frames + offset) / (fps*3600)))
    m = str(int(frames / (fps*60)) % 60)
    s = str(int((frames % (fps*60))/fps))
    f = str(frames % (fps*60) % fps)
    return f'{h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}:{f.zfill(2)}'

resolve = GetResolve()

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
fps = int(float(project.GetSetting('timelineFrameRate')))
currentTimeline = project.GetCurrentTimeline()
offset = currentTimeline.GetStartFrame()
markers = currentTimeline.GetMarkers()
csvfile = path(currentTimeline.GetName() + '.csv')
txtfile = path(currentTimeline.GetName() + '.txt')
csvColumns = ['name', 'TC', 'track', 'color', 'note', 'duration']
flag = 0

for key in markers:
    markers[key]['track'] = 'V2'
    markers[key]['TC'] = frames2TC(int(key), fps, offset)
    markers[key]['duration'] = '1'

if csvfile.is_file():
	path(csvfile).unlink()

if txtfile.is_file():
	path(txtfile).unlink()

try:
	with open(csvfile, 'a') as c:
		writer = csv.DictWriter(c, fieldnames=csvColumns)
		writer.writeheader()
		for key in markers:
			writer.writerow(markers[key])
except Exception as ex:
	print(ex)


try:
    with open(csvfile, 'r') as source:
        with open(txtfile, 'a') as dest:
            for line in source:
                if not flag:
                    flag = 1
                    pass
                else:
                    dest.writelines(line.replace(',', '\t'))
except Exception as ex:
	print(ex)

if csvfile.is_file():
	path(csvfile).unlink()

print('Done...')
print(f'Created file: {desDir}\\{txtfile}')
