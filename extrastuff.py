import config
from youtube_api import api

sc = api.Youtube(key=config.API_KEY)

info = sc.get_channel_stats("UC295-Dw_tDNtZXFeAPAW6Aw")["items"]
snippet = info["snippet"]
statistics = info["statistics"]

name = snippet["title"]
id = snippet["id"]
published_at = snippet["publishedAt"]

views = statistics["viewCount"]
subscribers = statistics["subscriberCount"]
hidden_subscriber_count = statistics["hiddenSubscriberCount"]



