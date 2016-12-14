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


def get_video_id_from_link(youtube_link):
	video_id = urlparse(youtube_link).query.split('=')[1]
	return video_id

def get_youtube_categories_mapping_table():
	with open(os.path.abspath(os.path.join(MYDIR, '../../data/YoutubeCategories.json.json')), 'r') as f:
		return json.load(f)

def get_youtube_video_info(youtube_video_id):
	h = httplib2.Http(".cache")
	(data, content) = h.request("https://www.googleapis.com/youtube/v3/videos?" +
		"part=id,snippet,statistics&fields=items(statistics,snippet(publishedAt,title,description,categoryId,tags))&id=%s&key=%s" % (youtube_video_id, settings.YOUTUBE_API_KEY), "GET")
	if data["status"] == '200' or data["status"] == '304':
		print "Finish crawling youtube_id: " + youtube_video_id
		return content
	else:
		print "Something error in get_youtube_video_info: " + content

def output_data(json_data):
	with codecs.open(os.path.abspath(os.path.join(MYDIR, '../../data/data_crawled_with_youtube_info.json')), 'w', encoding='utf8') as handle:
		handle.write(json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8'))

def merge_data(origin_data, youtube_data):
	content = json.loads(youtube_data)
	if content["items"] == []:
		# Youtube video have been blocked or deleted.
		return None
	snippet = content["items"][0]["snippet"]
	statistics = content["items"][0]["statistics"]

	youtube_categories_mapping_table = get_youtube_categories_mapping_table()
	snippet["categoryId"] = youtube_categories_mapping_table[snippet["categoryId"]]

	origin_data.update(snippet)
	origin_data.update({"statistics": statistics})

def get_categories():
	h = httplib2.Http(".cache")
	(data, content) = h.request("https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key=%s" % (settings.YOUTUBE_API_KEY), "GET")
	data = json.loads(content)
	category_dic = {}
	for key in data["items"]:
		category_dic[key["id"]] = key["snippet"]["title"]
	with open(os.path.abspath(os.path.join(MYDIR, '../../data/YoutubeCategories.json.json')), 'w') as outfile:
		json.dump(category_dic, outfile)

def get_video_info(all_json_data):
	for video in all_json_data:
		youtube_id = get_video_id_from_link(all_json_data[video]["youtube_link"])
		youtube_video_data = get_youtube_video_info(youtube_id)
		# print youtube_video_data   # Decommnet this if need debug.
		merge_data(all_json_data[video], youtube_video_data)
	output_data(all_json_data)


get_categories()
# Lauch youtubeAPI crawler to update original data.
with open(os.path.abspath(os.path.join(MYDIR, '../../data/data_crawled.json')), 'r') as f:
	data_crawled = json.load(f)
get_video_info(data_crawled)
