import config
from youtube_api import api
import json

sc = api.Youtube(key=config.API_KEY, headers={"Accept": "application/json"})

channel_data = dict()
for channel_id in config.CHANNEL_IDS:
    channel_stats = sc.get_specific_channel_stats(channel_id)
    channel_data[channel_id] = channel_stats

with open(f"./channel_data/channel_id_to_info.json", "w") as outfile:
    json.dump(channel_data, outfile)
