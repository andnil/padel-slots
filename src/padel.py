import requests
import json
from datetime import datetime, timedelta
from dateutil import tz
import pandas as pd
import itertools
from operator import itemgetter


class Padel:
    def __init__(self):
        self.__base_url = 'https://playtomic.io/api/v1/availability'

    def __get_wanted_play_dates(self):
        from_date = datetime.now()
        to_date = from_date + timedelta(days=15)

        sundays = pd.date_range(start=str(from_date), end=str(to_date),
                                freq='W-SUN').strftime('%Y-%m-%d').tolist()
        saturdays = pd.date_range(start=str(from_date), end=str(to_date),
                                  freq='W-SAT').strftime('%Y-%m-%d').tolist()

        return sorted(sundays + saturdays)

    def get_free_slots(self):
        courts_map = {
            'af720073-94f8-4140-8f6f-12018b512173': 'Centercourt (Bana 1)',
            '3747cd45-2b90-4da3-9c16-77998dcb37a0': 'Martin Servera (Bana 2)',
            '7bf73f69-e150-4c19-ba0c-223e5899b849': 'Bana 3',
            '6944628c-d493-4988-8202-2e2bcdc42054': 'Bana 4',
            '63110cd0-d47b-46cc-904c-ebb6538e5d11': 'Bana 5',
            'df435aaa-30aa-408a-87bc-148b5659620c': 'Bana 6',
            '391bc185-da3b-48b5-9e0e-11810ffeeecb': 'Bana 7',
            '94115e38-a9c1-4535-8d3d-4325012edd84': 'Bana 8',
            '65142bcf-f4b8-4d72-aa79-28e0d370ac21': 'Samsung QLED (Bana 9)'
        }
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Stockholm')

        play_dates = self.__get_wanted_play_dates()
        response = {}
        for date in play_dates:
            payload = {
                'user_id': 'me',
                'tenant_id': '231100a9-746c-4533-a01c-a65a0fda2507',
                'sport_id': 'PADEL',
                'local_start_min': f'{date}T11:00:00',
                'local_start_max': f'{date}T18:00:00'
            }

            r = requests.get(self.__base_url, params=payload)
            result = r.json()
            available_slots = []

            for court in result:
                for slot in court['slots']:

                    utc = datetime.strptime(
                        f'{date} {slot["start_time"]}', '%Y-%m-%d %H:%M:%S')

                    utc = utc.replace(tzinfo=from_zone)

                    local_time = utc.astimezone(to_zone)
                    if slot['duration'] == 60:
                        available_slots.append(
                            {
                                'name': courts_map[court['resource_id']],
                                'start_date': local_time.strftime('%Y-%m-%d'),
                                'start_time': local_time.strftime('%H:%M'),
                                'duration': slot['duration'],
                                'price': slot['price']
                            })

            sorted_available_slots = sorted(
                available_slots, key=itemgetter('start_date'))
            for key, group in itertools.groupby(sorted_available_slots, key=lambda x: x['start_date']):
                slot_list = []
                for slot in sorted(list(group), key=itemgetter('start_time')):
                    slot_list.append(slot)

                response[key] = slot_list

        return response
