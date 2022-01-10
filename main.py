
# code to read kafka and process the data
from kafka import KafkaConsumer
import json
import basic_functions as bf
import urllib
import requests


def extract_values(message):
    video_title = message['video_title']
    video_url = message['video_url']
    channel_id = message['channel_id']
    published = message['published']
    updated = message['updated']
    return video_title, video_url, channel_id, published, updated


def get_messages():
    consumer = KafkaConsumer('yt_test',
                             bootstrap_servers='localhost:9092')
    for message in consumer:
        print(message)
        print(message.value)
        json_msg = json.loads(message.value)
        video_title, video_url, channel_id, published, updated = extract_values(json_msg)
    return video_title, video_url, channel_id, published, updated


def get_description(url):
    # video description
    pass


def get_symbols():
    db = bf.use_db()
    conn = db.get_conn
    sql_text = "select symbol from symbols where length(symbol) >2"
    df = db.read_db(sql_text)
    print(df['symbol'])
    symbols = df['symbol'].tolist()
    return symbols


def extract_coin(text, symbols):
    text_list = text.split()
    symbol_list = []
    for symbol in symbols:
        for tit in text_list:
            if symbol == tit.lower():
                symbol_list.append(symbol)
    # extract coin name from video title
    return symbol_list


def get_top_ranking(text):
    rank = 99999
    for symbol in text:
        print(symbol)
        if symbol['market_cap_rank'] < rank:
            rank = symbol['market_cap_rank']
            highest_symbol = symbol
    return highest_symbol
    # function to get current CMC/ Coingecko ranking


if __name__ == '__main__':
    video_title, video_url, channel_id, published, updated = get_messages()
