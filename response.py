import lease
import requests
from requests import Response


class PubsubResponse:
    """
    Response Class for PubSubhubbub requests
    :param channel_id: str - the channel_id of the channel to subscribe to
    :param callback_url: str - the callback_url to subscribe to the channel
    :param response: Response - the response from the pubsubhubbub request
    """

    def __init__(self, channel_id, callback_url, response):
        self.channel_id = channel_id
        self.callback_url = callback_url
        self.response = response

    def health_check(self) -> bool:
        """
        Checks the health of the pubsubhubbub lease
        :return: bool - True if the lease is valid, otherwise raises Exception
        """
        headers = lease._get_headers()

        params = (
            ('hub.callback', self.callback_url),
            ('hub.topic',
             f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={self.channel_id}'),
            ('hub.secret', ''),
        )

        response = requests.get(
            'https://pubsubhubbub.appspot.com/subscription-details', headers=headers, params=params
        )

        if "unverified" in response.text:
            raise Exception(
                f"Subscription for channel_id: {self.channel_id} and callback_url: {self.callback_url} is unverified, did you return the pubsubhubbub secret from you callback_url?"
            )
        else:
            return True

    def get_response(self) -> Response:
        """
        Returns the response from the pubsubhubbub request
        :return: dict - the response from the pubsubhubbub request
        """
        return self.response