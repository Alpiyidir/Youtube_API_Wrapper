import requests


class Youtube:
    def __init__(self, key, headers=None):
        self.key = key
        if headers:
            self.headers = headers

    def add_headers(self, headers):
        self.headers = self.headers.update(headers)

    def get_channel_videos_with_api(self, channel_id: str, vid_count_requested):
        # Need to replace character at index 1 of channel_id with U to get link for user uploads
        index = 1
        channel_uploads_id = channel_id[:index] + "U" + channel_id[index + 1:]

        req_string = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails"
        # 50 videos per page
        json_list = []
        remaining_vid_count = vid_count_requested
        while remaining_vid_count > 0:
            if remaining_vid_count >= 50:
                # Maximum results per page is 50
                max_results = 50
            else:
                max_results = remaining_vid_count

            if remaining_vid_count == vid_count_requested:
                json_response = requests.get(
                    f"{req_string}&playlistId={channel_uploads_id}&maxResults={max_results}&key={self.key}").json()
                channel_vid_count = json_response["pageInfo"]["totalResults"]
                if channel_vid_count < vid_count_requested:
                    print(
                        f"Channel only has {channel_vid_count} videos and you requested to fetch {vid_count_requested}, fetching only {channel_vid_count} many videos")
                    remaining_vid_count = channel_vid_count

                    # Changes vid count requested to maximum video count on the channel.

                    vid_count_requested = channel_vid_count
            else:
                next_page_token = json_list[-1]["nextPageToken"]
                json_response = requests.get(
                    f"{req_string}&playlistId={channel_uploads_id}&maxResults={max_results}&pageToken={next_page_token}&key={self.key}").json()

            json_list.append(json_response)

            remaining_vid_count -= max_results

        return {"json": json_list, "videos_fetched": vid_count_requested}

    @staticmethod
    def get_video_ids_from_json_list(json_list):
        video_id_list_per_request = []
        count = 0
        for request in json_list:
            request_ids = []
            for video in request["items"]:
                try:
                    video_id = video["contentDetails"]["videoId"]
                except:
                    print("Couldn't find videoId for {0}".format(count))
                request_ids.append(video_id)

                count += 1
            video_id_list_per_request.append(request_ids)

        return video_id_list_per_request

    def get_video_ids_from_channel(self, channel_id, vid_count_requested):
        info = self.get_channel_videos_with_api(channel_id, vid_count_requested)
        json_list = info["json"]
        videos_fetched = info["videos_fetched"]
        return {"video_ids_per_request": self.get_video_ids_from_json_list(json_list), "videos_fetched": videos_fetched}

    def get_video_analytics(self, video_id):
        return requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status,"
                            "statistics&maxResults=50"
                            f"&id={video_id}&key={self.key}", headers=self.headers).json()

    # video id's per request are in groups of 50 by default
    def get_videos_analytics(self, video_ids_per_request):
        video_info = []
        for video_ids in video_ids_per_request:
            comma_seperated_video_ids = ",".join(map(str, video_ids))
            json = self.get_video_analytics(comma_seperated_video_ids)
            video_info.append(json)
        return video_info

    def get_videos_analytics_from_channel_id(self, channel_id, vid_count_requested=999999):
        info = self.get_video_ids_from_channel(channel_id, vid_count_requested)

        # Max size of video id's per request is 50
        video_ids_per_request = info["video_ids_per_request"]  # contains list of lists that hold video keys
        videos_fetched = info["videos_fetched"]

        videos_analytics = self.get_videos_analytics(video_ids_per_request)

        return {"videos_analytics": videos_analytics, "videos_fetched": videos_fetched}

    def get_channel_stats(self, channel_id):
        # comma_seperated_channel_id_list = ",".join(map(str, channel_id_list))
        return requests.get(
            f"https://youtube.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={channel_id}&key={self.key}").json()

    def get_specific_channel_stats(self, channel_id):
        # Not very efficient, currently gets channel id's one by one but not worth the effort to get all channels at once
        # as this only uses 20 query points (1 per channel)
        info = self.get_channel_stats(channel_id)["items"][0]
        snippet = info["snippet"]
        statistics = info["statistics"]

        name = snippet["title"]
        # id = snippet["id"]
        published_at = snippet["publishedAt"]

        views = statistics["viewCount"]
        subscribers = statistics["subscriberCount"]
        hidden_subscriber_count = statistics["hiddenSubscriberCount"]

        return {"name": name, "published_at": published_at, "views": views, "subscribers": subscribers,
                "hidden_subscriber_count": hidden_subscriber_count}

    def get_channels(self, channel_id):
        return requests.get(
            f"https://youtube.googleapis.com/youtube/v3/search?part=items&channelId={channel_id}&key={self.key}").json()


"""
videos = sc.get_channel_videos(channel_id="UCX6OQ3DkcsbYNE6H8uQQuVA", sort_by="newest", limit=1000)
count = 0

start = time.time()
for video in videos:
    count += 1

end = time.time() - start
print("Videos {0} | Total: {1}s Average: {2}".format(count, end, end / count))
"""

"""

// publish date: date
// madeForKids: bool
// video duration: minutes


raw_json = sc.get_channel_stats_in_bulk(["UCX6OQ3DkcsbYNE6H8uQQuVA", ])
channel_info = raw_json["items"]
for channel in channel_info:
    print(channel)
    subscriber_count = channel["statistics"]["subscriberCount"]
    country = channel["snippet"]["country"]
    print(subscriber_count, country)
"""
