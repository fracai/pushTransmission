#!/usr/local/python/bin/python -OO

import ConfigParser
import httplib
import sys
import urllib

import os


def read_config(config):
    configuration = ConfigParser.ConfigParser()
    config_file = os.path.join(os.path.dirname(sys.argv[0]), config)

    if not os.path.isfile(config_file):
        sys.exit("Config file not found")

    try:
        fp = open(config_file, "r")
        configuration.readfp(fp)
        fp.close()
    except IOError:
        sys.exit("Config file not readable")

    return configuration


def push(torrent_name):
    configuration = read_config("pushover.cfg")
    api_token = configuration.get("Pushover", "api_token")
    user_key = configuration.get("Pushover", "user_key")

    title = "Download complete"
    message = torrent_name

    cx = httplib.HTTPSConnection("api.pushover.net:443")
    cx.request(
        "POST",
        "/1/messages",
        urllib.urlencode({
            "token": api_token,
            "user": user_key,
            "title": title,
            "message": message
        }),
        {"Content-type": "application/x-www-form-urlencoded"}
    )


if 'TR_TORRENT_NAME' not in os.environ:
    sys.exit("Torrent name not set")
else:
    push(os.environ['TR_TORRENT_NAME'])
