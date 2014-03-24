import gdata.youtube
import gdata.youtube.service

# url:
#     feed url
# type:
#     subscriptions
#     favorites
def get_all(url, type):
	result = list()
	
	# set the parameters
	correct_url = url + "?start-index=%d&max-results=50&v=2"
	
	page = 0
	while True:
		# the max result from a request is 50. if you need to get more than 50, you need to use de start-index parameter
		index = page * 50 + 1
		
		# get the list from youtube's server
		yt_feed = yt_service.GetYouTubeVideoFeed(correct_url % index)
		
		# if the list has 0 elements, that means you need to stop the requests
		if len(yt_feed.entry) == 0:
			break
		
		# process the result for each value
		for entry in yt_feed.entry:
			if entry is not None:
				if type == "subscriptions":
					result.append("%s;%s;%s" % (type, entry.title.text.split(':')[-1].strip(), entry.link[2].href))
				
				elif type == "favorites":
					if entry.link[2].type == "application/atom+xml":
						result.append("%s;%s;https://m.youtube.com/details?v=%s" % (type, entry.title.text, entry.link[2].href.split("/")[-1]))
					elif entry.link[2].type == "text/html":
						result.append("%s;%s;%s" % (type, entry.title.text, entry.link[2].href))
		page = page + 1
	
	return result
		
# -------------------------------------------------------------------------------------

# default username from account
user_profile = "default"

# feeds url
url_favorites = "http://gdata.youtube.com/feeds/api/users/%s/favorites" % user_profile
url_watch_later = "https://gdata.youtube.com/feeds/api/users/%s/watch_later" % user_profile
url_history = "https://gdata.youtube.com/feeds/api/users/%s/history" % user_profile
url_subscriptions = "https://gdata.youtube.com/feeds/api/users/%s/subscriptions" % user_profile

print "connecting"
yt_service = gdata.youtube.service.YouTubeService()
yt_service.email = 'EMAIL@HERE.COM' #put your youtube email here
yt_service.password = 'PASSWORD'             # put your password here
yt_service.ProgrammaticLogin()

print "downloading playlists"
export_list = list()
export_list.extend(get_all(url_subscriptions, "subscriptions"))
export_list.extend(get_all(url_favorites, "favorites"))

print "writing file"
writer = open("/Users/User/Desktop/youtube_backup.csv", "w")
for item in export_list:
	writer.write(item + "\n")
writer.close()

print "end"

