from praw import Reddit
import urllib
from PIL import Image
import os, shutil
from time import sleep
import json

f = open('keys.json')
data = json.loads(f.read())
f.close()

reddit = Reddit(client_id=data['client_id'], client_secret=data['client_secret'], user_agent='IamXander')

submissions = reddit.subreddit('earthporn+ExposurePorn+AnimalPorn+RoadPorn+carporn+CityPorn+VillagePorn+ruralporn+MostBeautiful').top('month')

# 'approved_by', 'archived', 'author', 'author_flair_css_class', 'author_flair_text', 'banned_at_utc', 'banned_by', 'brand_safe', 'can_gild',
#'can_mod_post', 'clear_vote', 'clicked', 'comment_limit', 'comment_sort', 'comments', 'contest_mode', 'created', 'created_utc', 'crosspost',
#'delete', 'disable_inbox_replies', 'distinguished', 'domain', 'downs', 'downvote', 'duplicates', 'edit', 'edited', 'enable_inbox_replies',
#'flair', 'fullname', 'gild', 'gilded', 'hidden', 'hide', 'hide_score', 'id', 'id_from_url', 'is_crosspostable', 'is_reddit_media_domain', 'is_self',
#'is_video', 'likes', 'link_flair_css_class', 'link_flair_text', 'locked', 'media', 'media_embed', 'mod', 'mod_note', 'mod_reason_by', 'mod_reason_title',
#'mod_reports', 'name', 'num_comments', 'num_crossposts', 'num_reports', 'over_18', 'parent_whitelist_status', 'parse', 'permalink', 'pinned', 'post_hint',
#'preview', 'quarantine', 'removal_reason', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'secure_media', 'secure_media_embed', 'selftext',
#'selftext_html', 'shortlink', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_type', 'suggested_sort', 'thumbnail',
#'thumbnail_height', 'thumbnail_width', 'title', 'unhide', 'unsave', 'ups', 'upvote', 'url', 'user_reports', 'view_count', 'visited', 'whitelist_status'

folder = 'images'
for the_file in os.listdir(folder):
	file_path = os.path.join(folder, the_file)
	try:
		if os.path.isfile(file_path):
			os.remove(file_path)
	except Exception as e:
		print(e)

i = 0
for s in submissions:
	print(s.url)
	if s.url[-3:] != 'png' and s.url[-3:] != 'jpg' and s.url[-4:] != 'jpeg':
		continue
	dotIdx = s.url.rfind('.')
	loc = 'images/img_' + str(i) + s.url[dotIdx:]

	numTries = 5
	success = False
	for dl in range(numTries):
		try:
			print('trying to download... Try number: ' + str(dl))
			urllib.request.urlretrieve(s.url, loc)
			success = True
			break
		except:
			print('error trying again... Waiting 10 seconds')
			sleep(10)
	if not success:
		continue
	im = Image.open(loc)
	width, height = im.size
	print(width, height)
	im.close()
	if width < 1920 or height < 1080:
		os.remove(loc)
		continue
	if i >= 30:
		break;
	i += 1

# import ctypes
# loc = "C:/Users/Xander/Desktop/workspace/windowsBackground/" + loc
# print(loc)
# ctypes.windll.user32.SystemParametersInfoW(20, 0, loc , 0)
