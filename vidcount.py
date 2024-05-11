import json

raw_video = json.load(open("raw_video_data.json"))

count = 0
for channel_id, videos_data_grouped in raw_video.items():
    for video_data_grouped in videos_data_grouped:
        for video_data in video_data_grouped["items"]:
            count += 1

print(count)