
import csv
import datetime
import requests as r
import time

ENDPOINT = 'http://www.cbcmusic.ca/Component/Playlog/GetPlaylog?stationId=99&date={}'

def fetch_shows_of_day(date):
    response = r.get(ENDPOINT.format(date))
    return response.json()


def extract_specific_show(data, show_name):
    to_return = {}

    for program in data['programs']:
        if program['Title'].lower() == show_name.lower():
            to_return = program

    return to_return


def string_of_list(l):
    stripped_l = [x.strip() for x in l]
    return ','.join(stripped_l)


def clean_up_track_data(track):
    return {'album': track['Album'].strip(),
            'title': track['Title'].strip(),
            'artists': string_of_list(track['Artists']),
            'composers': string_of_list(track['Composers']),
            'time': track['Date'].strip()}


def save_episode(episode_data, date_string):
    with open('episodes/{}.csv'.format(date_string), 'w') as episode_file:
        field_names = ['album', 'title', 'artists', 'composers', 'time']
        writer = csv.DictWriter(episode_file, field_names)
        writer.writeheader()

        track_counter = 0
        for track in episode_data['Tracks']:
            clean_track = clean_up_track_data(track)

            writer.writerow(clean_track)

            track_counter += 1

        print('Saved {} tracks from {}'.format(track_counter, date_string))


def fetch_episode_of_day(date):
    data = fetch_shows_of_day(date)
    episode = extract_specific_show(data, 'The Signal')

    return episode


def save_show_of_day(date):
    print('Fetching shows of {}'.format(date))
    episode = fetch_episode_of_day(date)

    if episode:
        save_episode(episode, date)


if __name__ == '__main__':
    current_time = datetime.date(2017, 9, 3) # The signal last aired on sept 2nd 2017
    min_time = datetime.date(2005, 1, 1) # It lasted for about ten years

    while current_time > min_time:
        date = current_time.strftime('%Y-%m-%d')

        save_show_of_day(date)

        current_time = current_time - datetime.timedelta(days=1)
