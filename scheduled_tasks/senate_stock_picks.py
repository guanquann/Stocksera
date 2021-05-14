import os
import requests
import json
import yaml
import re

# Get JSON of existing members
existing_member_req = requests.get('https://theunitedstates.io/congress-legislators/legislators-current.json')
existing_members = existing_member_req.json()

# Get JSON of Previous members
prev_member_req = requests.get('https://theunitedstates.io/congress-legislators/legislators-historical.json')
prev_members = prev_member_req.json()


def bioid(senator):
    regex = re.compile('[^a-zA-Z]')
    #First parameter is the replacement, second parameter is your input string
    first_name = regex.sub('', senator['first_name'].split()[0].lower())
    last_name = regex.sub('', senator['last_name'].split()[0].lower())

    for member in existing_members:
        print(member['name'])
        if 'official_full' not in member['name'].keys():
            member['name']['official_full'] = f"{member['name']['first']} {member['name']['last']}"

        if first_name in member['name']['official_full'].lower() and last_name in member['name']['official_full'].lower():
            return member['id']['bioguide']

    for member in prev_members:
        print(member['name'])
        if first_name in member['name']['first'].lower() and last_name in member['name']['last'].lower():
            return member['id']['bioguide']

    # Some members have nickname first names like William Cassidy.
    # when that is that case just hope to match a last name...
    for member in existing_members:
        if last_name == member['name']['last'].lower() or last_name in member['name']['official_full'].lower():
            return member['id']['bioguide']

    for member in prev_members:
        if last_name in member['name']['last'].lower():
            return member['id']['bioguide']

    return None

def add_details_to_daily_reports():
    daily_reports = []
    for filename in os.listdir('../data'):
        if filename.endswith(".json"):
            daily_reports.append(os.path.join('../data', filename))

    for file in daily_reports:
        with open(file, "r") as read_file:
            file_data = json.load(read_file)

        for senator in file_data:
            senator['bioguide'] = bioid(senator)
            if senator['bioguide'] == None:
                print('FAILED TO FIND ID FOR SENATOR')
                print(senator['first_name'])
                print(senator['last_name'])
                print(file)
                exit()

        with open(file, "w") as write_file:
            write_file.write(json.dumps(file_data))

def add_details_to_daily_agg():
    file = '../aggregate/all_daily_summaries.json'
    with open(file, "r") as read_file:
        file_data = json.load(read_file)

    for senator in file_data:
        senator['bioguide'] = bioid(senator)
        if senator['bioguide'] == None:
            print('FAILED TO FIND ID FOR SENATOR')
            print(senator['first_name'])
            print(senator['last_name'])
            print(file)
            exit()

    with open(file, "w") as write_file:
        write_file.write(json.dumps(file_data))

def add_details_to_senator_agg():
    file = '../aggregate/all_transactions_for_senators.json'
    with open(file, "r") as read_file:
        file_data = json.load(read_file)

    for senator in file_data:
        senator['bioguide'] = bioid(senator)
        if senator['bioguide'] == None:
            print('FAILED TO FIND ID FOR SENATOR')
            print(senator['first_name'])
            print(senator['last_name'])
            print(file)
            exit()

    with open(file, "w") as write_file:
        write_file.write(json.dumps(file_data))

def files_to_yaml():
    files = []
    for filename in os.listdir('../data'):
        if filename.endswith(".json"):
            files.append(os.path.join('../data', filename))
    for filename in os.listdir('../aggregate'):
        if filename.endswith(".json"):
            files.append(os.path.join('../aggregate', filename))

    for file in files:
        with open(file, "r") as read_file:
            file_data = json.load(read_file)

            with open(f"{file}.yaml", 'w') as write_file:
                write_file.write(yaml.dump(file_data))

add_details_to_daily_reports()
add_details_to_daily_agg()
add_details_to_senator_agg()
files_to_yaml()