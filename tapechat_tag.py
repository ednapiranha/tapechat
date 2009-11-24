import urllib
import math
import re
import web
from datetime import datetime
from redis import Redis
from auto_tagify import AutoTagify

tag = AutoTagify()
tag.link = '/tags'
clean_word = re.compile('[\[\],().:"\'?!*<>/\+={}`~\n\r\t]')
clean_quotes = re.compile('(%27)')
r = Redis()

class TapeChatTag():
  def __init__(self):
    self.all_entries = ''
    self.next_page = 1
    self.prev_page = 0
    self.page_value = 0
    self.start_pos = 1
    self.text_entries = ''
    
  def generate(self):
    if self.next_page < 0: self.next_page = 0
    if self.prev_page < 0: self.prev_page = 0
    if self.page_value < 0: self.page_value = 0
     
    try:
      self.next_page = int(self.page_value) + 1
      self.start_pos = (self.next_page - 1) * 100 + 1
      self.prev_page = self.next_page - 2
    except: pass

    try:
      for tag_word in set(r.sort("uid:" + str(web.config.session_parameters['user_id']) + ":tags",by="tid:*:word",get="tid:*:word",alpha=True)):
        # try:
        tag_count = r.llen("word:" + str(tag_word) + ":texts")
        font_size = math.log(tag_count * 100, math.e) * 3
        self.all_entries += '<li><a href="' + tag.link + '/' + tag_word +'" style="font-size: ' + str(font_size) + 'px;">' + urllib.unquote(tag_word) + ' (' + str(tag_count)  +')</a></li>'
        # except: self.page_value = 1
    except:
      pass

  def tag_text(self,tag_word):
    self.text_entries = ''
    try:
      for text_id in set(r.lrange("uid:" + str(web.config.session_parameters['user_id']) + ":" + tag_word + ":texts",0,100)):
        self.text_entries += '<li>' + urllib.unquote(r.get("text:" + str(text_id))) + ' <a href="/delete/' + tag_word + '/' + str(text_id) + '">delete</a></li>'
    except: self.text_entries = '<li>No such tag found</li>'
    return self.text_entries

  def add(self,tag_word,feed_id):
    if not r.exists("word:" + tag_word + ":tid"):
      tag_id = r.incr("global:nextTagId")
      user_id = r.get("fid:" + str(feed_id) + ":uid")
      r.set("tid:" + str(tag_id) + ":word",clean_quotes.sub('',(urllib.quote(clean_word.sub('',tag_word)))))
      r.push("global:tags",tag_id)
      r.set("uid:" + str(r.get("fid:" + str(feed_id) + ":tid")),tag_id)
    if not r.exists("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tid"):
      r.push("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tags",tag_id)

  def _format_time(self,time):
    if int(time) < 10:
      return '0' + str(time)
    return str(time)

  def _format_date(self,text):
    date = datetime.utcfromtimestamp(float(text))
    return '<span>' + str(date.year) + '/' + str(date.month) + '/' + str(date.day) + ' ' + self._format_time(date.hour) + ':' + self._format_time(date.minute) + ' </span> '