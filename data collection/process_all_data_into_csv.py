import config
from youtube_api import api
import json
import csv
import re

sc = api.Youtube(key=config.API_KEY, headers={"Accept": "application/json"})

# Load json from two files and close files
raw_video = json.load(open("./video_data/raw_video_data.json"))
channel_id_to_info = json.load(open("./channel_data/channel_id_to_info.json"))

with open("final_csv/final.csv", "w") as f:
    wr = csv.writer(f)

    # Set headers
    wr.writerow(
        ["title_length", "view_count", "like_count", "comment_count", "video_length", "tag_count", "category_id",
         "channel_subscriber_count"])
    for channel_id, videos_data_grouped in raw_video.items():
        for video_data_grouped in videos_data_grouped:
            for video_data in video_data_grouped["items"]:
                snippet = video_data["snippet"]
                stats = video_data["statistics"]

                # Checks before parsing video

                if snippet["liveBroadcastContent"] == "live" or snippet["liveBroadcastContent"] == "upcoming":
                    continue

                try:
                    title_length = len(snippet["title"])
                except KeyError:
                    title_length = None
                try:
                    view_count = stats["viewCount"]
                except KeyError:
                    view_count = None
                try:
                    like_count = stats["likeCount"]
                except KeyError:
                    like_count = None
                try:
                    comment_count = stats["commentCount"]
                except KeyError:
                    comment_count = None

                try:
                    # Functionality for duration parsing taken from
                    # https://cheatcode.co/tutorials/how-to-fetch-a-youtube-videos-duration-in-node-js
                    duration_string = video_data["contentDetails"]["duration"].replace("P", "").replace("T", "")
                    duration_regex = re.compile(
                        "^(?:([0-9]?[0-9])D)?(?:([0-9]?[0-9])H)?(?:([0-9]?[0-9])M)?(?:([0-9]?[0-9])S)?$")

                    duration_tuple = re.findall(duration_regex, duration_string)[0]
                    duration = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
                    if duration_tuple[0] != "":
                        duration["days"] = int(duration_tuple[0])

                    if duration_tuple[1] != "":
                        duration["hours"] = int(duration_tuple[1])

                    if duration_tuple[2] != "":
                        duration["minutes"] = int(duration_tuple[2])

                    if duration_tuple[3] != "":
                        duration["seconds"] = int(duration_tuple[3])

                    # Calculates total video length in seconds
                    video_length_in_seconds = 0
                    for time_type, time_amount in duration.items():
                        if time_type == "days":
                            video_length_in_seconds += time_amount * 24 * 60 * 60
                        elif time_type == "hours":
                            video_length_in_seconds += time_amount * 60 * 60
                        elif time_type == "minutes":
                            video_length_in_seconds += time_amount * 60
                        elif time_type == "seconds":
                            video_length_in_seconds += time_amount
                    video_length = video_length_in_seconds
                except KeyError:
                    video_length = None

                video_length = video_length_in_seconds

                try:
                    tag_count = len(snippet["tags"])
                except KeyError:
                    tag_count = None
                try:
                    category_id = snippet["categoryId"]
                except KeyError:
                    category_id = None
                try:
                    channel_subscriber_count = channel_id_to_info[snippet["channelId"]]["subscribers"]
                except KeyError:
                    channel_subscriber_count = None

                wr.writerow([title_length, view_count, like_count, comment_count, video_length, tag_count, category_id,
                             channel_subscriber_count])
