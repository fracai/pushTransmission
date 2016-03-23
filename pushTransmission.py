#!/usr/local/python/bin/python -OO

import ConfigParser
import sys

import chump
import os


def read_config(config):
    configuration = ConfigParser.ConfigParser()
    config_path = os.path.join(os.path.dirname(sys.argv[0]), config)

    if not os.path.isfile(config_path):
        sys.exit("Config file not found")

    try:
        fp = open(config_path, "r")
        configuration.readfp(fp)
        fp.close()
    except IOError:
        sys.exit("Config file not readable")

    return configuration


def push(torrent_name):
    configuration = read_config("pushover.cfg")
    api_token = configuration.get("Pushover", "api_token")
    user_key = configuration.get("Pushover", "user_key")

    app = chump.Application(api_token)
    user = app.get_user(user_key)

    title = "Download complete"
    message = torrent_name

    user.send_message(
        message,
        title=title
    )


if 'TR_TORRENT_NAME' not in os.environ:
    sys.exit("Torrent name not set")
else:
    push(os.environ['TR_TORRENT_NAME'])
