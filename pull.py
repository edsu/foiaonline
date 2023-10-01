#!/usr/bin/env python3

import os
import re
import json
import time
import logging
import requests
import datetime

logging.basicConfig(filename="pull.log", level=logging.INFO)

http = requests.Session()
form_url = 'https://foiaonline.gov/foiaonline/action/public/search/advancedSearch'
api_url = 'https://foiaonline.gov/foiaonline/api/search/advancedSearch'


def main():

    # get the set of record IDs we've already collected so they aren't written again
    seen_ids = get_seen_ids()

    # we need an CSRF token to interact with the API
    csrf_token = get_token()

    # get records week by week starting in 2004-03-01 
    # initial probing indicated that the first record was received 2004-03-04
    start = datetime.date(2004, 3, 1)
    today = datetime.date.today()

    # request records in time ranges of a week
    # this isn't the most efficient since the records are so sparse at the beginning
    # but it was easier than adapting the time slice dynamically based on the record density
    time_slice = datetime.timedelta(days=7)

    while start < today:
        end = start + time_slice

        # don't search into the future
        if end > today:
            end = today

        print(f'fetching records for {start} - {end}')
        found = get_records(start, end, csrf_token, seen_ids)
        if found == None:
            print(f'hit max 10,000 limit for {start} - {end}')
            break
        else:
            print(f'found {found} records for {start} - {end}')

        # move on to the next slice of time
        start = end


def get_token():
    resp = http.get(form_url)
    if resp.status_code == 200:
        match = re.search('name="x-csrf-token" value="(.+?)" />', resp.text)
        if match:
            return match.group(1)
    return None


def get_records(start, end, csrf_token, seen_ids):
    """
    Fetch the records between start and end using the given CSRF token and the
    set of IDs that have already been written. The total number of records 
    retrieved will be returned. If None is returned that indicates that there
    was an error.
    """

    output = open('data.jsonl', 'a')
    pos = 0
    while True:

        # be gentle
        time.sleep(2)

        # get the records for this time slice at the given position
        query = {
            'lastItemDisplayed': pos,
            'numberOfRecords': 100,
            'receivedDateFrom': start.strftime('%Y-%m-%d'),
            'receivedDateTo': end.strftime('%Y-%m-%d')
        }
        headers = {
            'referer': form_url,
            'x-csrf-token': csrf_token,
        }
        logging.info(f"fetching records for {start} - {end} pos={pos}")
        resp = http.post(api_url, json=query, headers=headers)

        if resp.status_code == 200:
            data = resp.json()

            # if there are 10,000 records we need a smaller time range
            total = data['recordsTotal']
            if total == 10_000:
                logging.error('recordsTotal is 10,000 which means results are truncated')
                return None
            elif total == 0:
                logging.warning(f'no records found for time range: {start} - {end}')
                return 0

            # write out any records we don't already have
            for record in data['data']:
                pos += 1
                if record['id'] in seen_ids:
                    logging.info(f'already have {record["id"]}')
                else:
                    logging.info(f'found {record["id"]}')
                    seen_ids.add(record['id'])
                    output.write(json.dumps(record) + '\n')

            if pos == total:
                logging.info(f'found {total} records for {start} - {end}')
                break

        else:
            # this is bad, so break loudly
            logging.error(f'error when fetching {query}: {resp.text}')
            raise Exception(f"unable to fetch data for {query}")

    return pos


def get_seen_ids():
    """
    Return a set of record IDs that have already been collected.
    """
    seen = set()
    if os.path.isfile('data.jsonl'):
        for line in open('data.jsonl'):
            record = json.loads(line)
            seen.add(record['id'])

    return seen


if __name__ == '__main__':
    main()
