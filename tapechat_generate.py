import feedparser
import re
import urllib
from redis import Redis
from BeautifulSoup import BeautifulSoup
from auto_tagify import AutoTagify
from tapechat_tag import TapeChatTag
from time import time

VALID_TAGS = ['p']
tag = AutoTagify()
tag.link = '/tags'
tapechat_tag = TapeChatTag()
r = Redis()
text_unique = []

feeds = r.sort("global:feeds",desc=True)
circle_sym = re.compile('(&#8226;)|(\xe2\x80\xa2)')
p_tags = re.compile('(<p>)|(</p>)')

for feed_id in feeds:
  feed = r.get("fid:" + str(feed_id) + ":url")
  rss = feedparser.parse(feed)
  for entry in rss.entries:
    if not r.exists("guid:" + str(entry.guid) + ":fid"):
      clean_text = BeautifulSoup(entry.summary)
      for t in clean_text.findAll(True):
        if t.name not in VALID_TAGS: t.hidden = True
      tag.text = p_tags.sub(' ',clean_text.renderContents())
      sanitized_text = tag.generate()
      text_id = r.incr("global:nextTextId")
      r.set("text:" + str(text_id), sanitized_text)  
      r.set("guid:" + str(entry.guid) + ":fid", feed_id)
      r.set("text:" + str(text_id) + ":timestamp",str(time()))
      r.set("text:" + str(text_id) + ":uid", r.get("fid:" + str(feed_id) + ":uid"))
      for tag_word in set(tag.tag_list()):
        tag_word = circle_sym.sub('',str(tag_word))
        if len(urllib.unquote(tag_word)) > 2:
          tag_word = urllib.quote(str(tag_word))
          if not r.exists("word:" + tag_word + ":tid"): 
            tapechat_tag.add(tag_word,feed_id)
          r.incr("word:" + tag_word + ":count")
          r.incr("tid:" + str(r.get("word:" + tag_word + ":tid")) + ":count")
          r.incr("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":" + tag_word + ":count")
          r.push("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":" + tag_word + ":texts",text_id)
          r.push("word:" + tag_word + ":texts",text_id)
r.save()