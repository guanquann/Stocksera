import os
import sys
import yaml
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

with open("config.yaml") as config_file:
    td_config_keys = yaml.load(config_file, Loader=yaml.Loader)
    if not td_config_keys:
        print("Please create an TD Ameritrade Developer Account first!")
        exit()
    client_id = td_config_keys["TDA_CLIENT_ID"]
    refresh_token = td_config_keys["TDA_REFRESH_TOKEN"]


def get_access_token():
    """
    Get Access Token using your TD Ameritrade Client ID and Refresh Token
    """
    r = requests.post(
        'https://api.tdameritrade.com/v1/oauth2/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': f'{client_id}@AMER.OAUTHAP',
        }
    )
    access_token = r.json()["access_token"]

    td_config_keys["TDA_CLIENT_ID"] = client_id
    td_config_keys["TDA_REFRESH_TOKEN"] = refresh_token
    td_config_keys["TDA_ACCESS_TOKEN"] = access_token

    with open('config.yaml', 'w') as outfile:
        yaml.dump(td_config_keys, outfile, default_flow_style=False)

    return td_config_keys


if __name__ == '__main__':
    get_access_token()
