import urllib
import re
import web
from redis import Redis

clean_url = re.compile('^(feed://)')
r = Redis()

class Feed():
  def add(self,url):
    url = clean_url.sub("http://",url)
    if not r.exists("url:" + str(url) + ":fid"):
      feed_id = r.incr("global:nextFeedId")
      r.set("fid:" + str(feed_id) + ":url",url)
      r.set("url:" + url + ":fid",feed_id)
      r.set("global:feeds",feed_id)
      r.set("uid:" + str(web.config.session_parameters['user_id']) + ":feeds",feed_id)
      r.set("fid:" + str(feed_id) + ":uid",web.config.session_parameters['user_id'])
    return True