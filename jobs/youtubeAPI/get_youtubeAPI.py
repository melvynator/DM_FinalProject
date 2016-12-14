# -*- coding: utf-8 -*-
import json
import httplib2
import sys
import codecs
import os
from urlparse import urlparse
import settings  # This is import your own YOUTUBE_API_KEY.
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
MYDIR = os.path.dirname(os.path.abspath(__file__))

def get_videoInfo(json_data):
	with open(os.path.join(MYDIR, 'YoutubeCategories.json'), 'r') as f:
		category_dic = json.load(f)

	json_data = json.loads(json_data)
	video_id = urlparse(json_data["youtube_link"]).query.split('=')[1]

	h = httplib2.Http(".cache")
	(data, content) = h.request("https://www.googleapis.com/youtube/v3/videos?part=id,snippet,statistics&fields=items(statistics,snippet(publishedAt,title,description,categoryId,tags))&id=%s&key=%s" % (video_id, settings.YOUTUBE_API_KEY), "GET")

	if (data["status"] == '200' or data["status"] == '304'):
		content = json.loads(content)
		snippet = content["items"][0]["snippet"]
		statistics = content["items"][0]["statistics"]
		snippet["categoryId"] = category_dic[snippet["categoryId"]]

		json_data.update(snippet)
		json_data.update({"statistics": statistics})

		with codecs.open(os.path.join(MYDIR, 'videoInfoData.json'), 'w', encoding='utf8') as handle:
			handle.write(json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8'))

		return "Finish youtube API crawler and file is videoInfoData.json."
	else:
		print "HTTP error in get_videoInfo."


def get_categories():
	h = httplib2.Http(".cache")
	(data, content) = h.request("https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key=%s" % (settings.YOUTUBE_API_KEY), "GET")
	data = json.loads(content)
	category_dic = {}
	for key in data["items"]:
		category_dic[key["id"]] = key["snippet"]["title"]
	with open(os.path.join(MYDIR, 'YoutubeCategories.json'), 'w') as outfile:
		json.dump(category_dic, outfile)


get_categories()

# get_videoInfo('{"url_youtube":"https://www.youtube.com/watch?v=j2ft_4b8vm8"}')  # Basic useage.
