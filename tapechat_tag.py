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
record_max_length = 50

class TapeChatTag():
  def __init__(self):
    self.all_entries = ''
    self.next_page = 1
    self.prev_page = 0
    self.page_value = 0
    self.start_pos = 0
    self.text_entries = ''  
    
  def generate(self,user_id):
    if self.next_page < 0: self.next_page = 0
    if self.prev_page < 0: self.prev_page = 0
    if self.page_value < 0: self.page_value = 0
     
    try:
      self.next_page = int(self.page_value) + 1
      self.start_pos = (self.next_page - 1) * record_max_length + 1
      self.prev_page = self.next_page - 2
    except: pass
    
    if user_id < 1:
      tag_list = r.sort("global:tags",by="tid:*:count",desc=True,start=self.start_pos,num=record_max_length * (self.next_page + 1))
    else:
      tag_list = r.sort("uid:" + str(web.config.session_parameters['user_id']) + ":tags",by="tid:*:count",desc=True,start=self.start_pos,num=100 * (self.next_page + 1))

    for tag_id in tag_list:
      tag_word = r.get("tid:" + str(tag_id) + ":word")
      try:
        if user_id < 1:
          tag_count = r.get("word:" + str(tag_word) + ":count")
        else:
          tag_count = r.get("uid:" + str(web.config.session_parameters['user_id']) + ":" + str(tag_word) + ":count")
        font_size = math.log(tag_count * 100, math.e) * 3
        self.all_entries += '<li class="tag"><a href="' + tag.link + '/' + tag_word +'" class="highlight" style="font-size: ' + str(font_size) + 'px;">' + urllib.unquote(tag_word) + ' (' + str(tag_count)  +')</a></li>'
      except: 
        pass
        
  def generate_stream(self,tag_counter):
    self.all_entries = ''
    tag_id = r.lindex("global:tags",int(tag_counter))
    try:
      tag_word = r.get("tid:" + str(tag_id) + ":word").encode('utf-8','ignore')
      tag_count = r.get("word:" + urllib.unquote(tag_word) + ":count")
      self.all_entries += '<li class="tags"><span>' + urllib.unquote(urllib.unquote(tag_word)) + '(' + str(tag_count)  +')</span> <div class="content"><ul>' + self.tag_text(urllib.unquote(tag_word),0) + '<li class="close">close</li></ul></div></li>'
    except:
      pass

  def tag_text(self,tag_word,user_id):
    self.text_entries = ''
    tag_word = urllib.quote(tag_word.encode('utf-8','ignore'))
    # try:
    if user_id < 1:
      for text_id in r.lrange("word:" + tag_word + ":texts",0,record_max_length):
        self.text_entries += '<li>' + r.get("text:" + str(text_id)) + '</li>'
    else:
      for text_id in r.lrange("uid:" + str(web.config.session_parameters['user_id']) + ":" + tag_word + ":texts",0,record_max_length):
        self.text_entries += '<li>' + r.get("text:" + str(text_id)) + '</li>'
    # except: self.text_entries = '<li>No such tag found</li>'
    return self.text_entries

  def add(self,tag_word,feed_id):
    if not r.exists("word:" + str(tag_word) + ":tid"):
      tag_id = r.incr("global:nextTagId")
      user_id = r.get("fid:" + str(feed_id) + ":uid")
      r.set("tid:" + str(tag_id) + ":word",urllib.quote(clean_quotes.sub('',clean_word.sub('',tag_word))))
      r.set("word:" + str(tag_word) + ":tid", tag_id)
      r.push("global:tags",tag_id)
      r.set("uid:" + str(r.get("fid:" + str(feed_id) + ":tid")),tag_id)
    if not r.exists("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tid"):
      r.push("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tags",tag_id)
    r.save()

  def _format_time(self,time):
    if int(time) < 10:
      return '0' + str(time)
    return str(time)

  def _format_date(self,text):
    date = datetime.utcfromtimestamp(float(text))
    return '<span>' + str(date.year) + '/' + str(date.month) + '/' + str(date.day) + ' ' + self._format_time(date.hour) + ':' + self._format_time(date.minute) + ' </span> '