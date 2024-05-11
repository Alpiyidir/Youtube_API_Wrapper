import config
from youtube_api import api
import json

sc = api.Youtube(key=config.API_KEY, headers={"Accept": "application/json"})

video_data = dict()
for channel_id in config.CHANNEL_IDS:
    info = sc.get_videos_analytics_from_channel_id(channel_id)
    json_array = info["videos_analytics"]
    video_data[channel_id] = json_array
    break


with open(f"./video_data/raw_video_data_new.json", "w") as outfile:
    json.dump(video_data, outfile)
