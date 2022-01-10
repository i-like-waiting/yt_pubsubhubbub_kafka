import requests
from response import PubsubResponse


def _get_headers():
    """
    Returns headers used to request pubsubhubbub
    :return: dict - the headers
    """
    return {
        "authority": "pubsubhubbub.appspot.com",
        "cache-control": "max-age=0",
        "origin": "https://pubsubhubbub.appspot.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "referer": "https://pubsubhubbub.appspot.com/subscribe",
        "accept-language": "en-US,en;q=0.9",
    }


def create(channel_id: str, callback_url: str, lease_seconds: int = None) -> PubsubResponse:
    """
    Creates a pubsubhubbub subscription
    :param channel_id: str - the channel id to subscribe to
    :param callback_url: str - the callback url to send the updates to
    :param lease_seconds: int - the lease time in seconds, defaults to None
    :return: Response - the response from the pubsubhubbub server
    """
    headers = _get_headers()

    data = {
        "hub.callback": callback_url,
        "hub.topic": f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
        "hub.verify": "async",
        "hub.mode": "subscribe",
        "hub.verify_token": "",
        "hub.secret": "",
    }

    if lease_seconds is None:
        data["hub.lease_seconds"] = str(60 * 60 * 24 * 10)  # max 10 days
    else:
        data["hub.lease_seconds"] = str(lease_seconds)

    response = requests.post(
        "https://pubsubhubbub.appspot.com/subscribe",
        headers=headers,
        data=data
    )

    return PubsubResponse(channel_id, callback_url, response)


def renew(channel_id: str, callback_url: str) -> PubsubResponse:
    """
    Renew the pubsubhubbub lease
    :param channel_id: str - the channel id to subscribe to
    :param callback_url: str - the callback url to send the updates to
    :return: PubsubResponse - the response from the pubsubhubbub server
    """
    return create(channel_id, callback_url)