import yaml
import requests

with open("config.yaml") as config_file:
    config_keys = yaml.load(config_file, Loader=yaml.Loader)

# https://developer.twitter.com/en/portal/dashboard
bearer_token = config_keys["TWITTER_BEARER_TOKEN"]


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request(
        "GET",
        url,
        auth=bearer_oauth,
    )
    if response.status_code != 200:
        raise Exception(
            "Request returned an errors: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()
