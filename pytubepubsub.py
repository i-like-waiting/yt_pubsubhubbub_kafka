from lease import create, renew
import response

#import pytubepubsub as pyt
import producer
import json

yt_channel_id = "UCqK_GSMbpiV8spgD3ZGloSw"
callback_url = "http://7e9f-81-100-231-74.ngrok.io/feed"

""" 
yt-to-discord - YouTube push notifications to Discord webhooks
Copyright (C) 2021  Bryan Cuneo
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xmltodict
import yaml

#from discord_webhook import DiscordWebhook
from flask import Flask, request
from xml.parsers.expat import ExpatError


try:
    with open("./config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    print("Unable to load config file: 'config.yaml'")
    print("Exiting...")
    exit(1)

app = Flask(__name__)


@app.route("/feed", methods=["GET", "POST"])
def feed():
    """Accept and parse requests from YT's pubsubhubbub.
    https://developers.google.com/youtube/v3/guides/push_notifications
    """

    challenge = request.args.get("hub.challenge")
    if challenge:
        # YT will send a challenge from time to time to confirm the server is alive.
        return challenge

    try:
        # Parse the XML from the POST request into a dict.
        xml_dict = xmltodict.parse(request.data)
        # Parse out the video URL.
        video_url = xml_dict["feed"]["entry"]["link"]["@href"]
        channel_id = xml_dict["feed"]["entry"]["yt:channelId"]
        title = xml_dict["feed"]["title"]
        video_url = xml_dict["feed"]["entry"]["author"]["uri"]
        published = xml_dict["feed"]["entry"]["published"]
        updated = xml_dict["feed"]["entry"]["updated"]
        payload = {
            title: title,
            video_url: video_url,
            channel_id: channel_id,
            published: published,
            updated: updated

        }
        producer.send_json('yt_videos', payload)
        print(title, ' ', video_url)

    except (ExpatError, LookupError):
        # request.data contains malformed XML or no XML at all, return FORBIDDEN.
        return "", 403

    # Everything is good, return NO CONTENT.
    return "", 204


if __name__ == "__main__":
    app.run()