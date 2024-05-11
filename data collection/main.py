import config
from youtube_api import api
import json

sc = api.Youtube(key=config.API_KEY, headers={"Accept": "application/json"})

count = 0
info = sc.get_video_ids_from_channel("UC3MLnJtqc_phABBriLRhtgQ", 149)

# Max size of video id's per request is 50
video_ids_per_request = info["video_ids_per_request"]  # contains list of lists that hold video keys
videos_fetched = info["videos_fetched"]

videos_analytics = sc.get_videos_analytics(video_ids_per_request)

print(videos_analytics)