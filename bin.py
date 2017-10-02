#!/usr/bin/env python3

import csv

from merge import FIELD_NAMES

def increment_count(field, bins):
    if field in bins:
        bins[field] += 1
    else:
        bins[field] = 1


if __name__ == '__main__':
    artists = {}
    songs = {}

    with open('the-signal.csv') as csvfile:
        reader = csv.DictReader(csvfile, FIELD_NAMES)
        next(reader)
        for row in reader:
            increment_count(row['title'], songs)
            increment_count(row['artists'], artists)

    sorted_artists = sorted(artists, key=artists.get, reverse=True)
    for artist in sorted_artists:
        print('{}: {}'.format(artist, artists[artist]))
