
import requests
from datetime import datetime
import json

def get_records_from_reddit(number_of_records=100):
    reddit_url = f"https://www.reddit.com/r/all/hot.json?limit={number_of_records}"
    reddit_headers = {'User-agent' : 'sebis reddit bot 0.0.1'}
    r = requests.get(url = reddit_url, headers = reddit_headers)
    reddit_data = r.json()
    now = datetime.now()
    now_iso = now.isoformat()
    now_epoch = now.timestamp()
    reddit_data['date'] = now_iso
    reddit_data['_id'] = now_epoch
    return reddit_data

def main():
    results = get_records_from_reddit(2)
    # store result in mongodb
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client['reddit']

    for post in results['data']['children']:
        post['date'] = results['date']
        post['_id'] = datetime.now().timestamp()
        db.posts.insert_one(post)




if __name__ == '__main__':
    main()

