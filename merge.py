#!/usr/bin/env python3

import csv
import pathlib
import os
import sys

EPISODE_DIR = 'episodes/'
FIELD_NAMES = ['album', 'title', 'artists', 'composers', 'time', 'date']

def fix_time(track):
    if track['time'] == '10pm':
        track['time'] = '10:00pm'
    if track['time'] == '11pm':
        track['time'] = '11:00pm'

    return track

def append_tracks_of_file(tracklist, f):
    p = pathlib.Path(f)
    with p.open() as track_file:
        reader = csv.DictReader(track_file, FIELD_NAMES)
        next(reader)
        for row in reader:
            row['date'] = p.stem
            tracklist.append(fix_time(row))


if __name__ == '__main__':
    tracklist = []

    for f in os.listdir(EPISODE_DIR):
        file_path = EPISODE_DIR + f
        if os.path.isfile(file_path):
            append_tracks_of_file(tracklist, file_path)

    tracklist.sort(key=lambda x: x['time'])
    tracklist.sort(key=lambda x: x['date'])

    with open('the-signal.csv', 'w') as big_file:
        writer = csv.DictWriter(big_file, FIELD_NAMES)
        writer.writeheader()
        [writer.writerow(x) for x in tracklist]
