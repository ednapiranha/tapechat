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
    self.start_pos = 0
    self.text_entries = ''
    
  def generate(self,user_id):
    if self.next_page < 0: self.next_page = 0
    if self.prev_page < 0: self.prev_page = 0
    if self.page_value < 0: self.page_value = 0
     
    try:
      self.next_page = int(self.page_value) + 1
      self.start_pos = (self.next_page - 1) * 100 + 1
      self.prev_page = self.next_page - 2
    except: pass
    
    if user_id < 1:
      tag_list = r.lrange("global:tags",self.start_pos,100 * (self.next_page + 1))
    else:
      tag_list = r.lrange("uid:" + str(web.config.session_parameters['user_id']) + ":tags",self.start_pos,100 * (self.next_page + 1))

    # try:
    for tag_id in tag_list:
      tag_word = r.get("tid:" + str(tag_id) + ":word")
      try:
        if user_id < 1:
          tag_count = r.get("word:" + str(tag_word) + ":count")
        else:
          tag_count = r.get("uid:" + str(web.config.session_parameters['user_id']) + ":" + str(tag_word) + ":count")
        font_size = math.log(tag_count * 100, math.e) * 3
        self.all_entries += '<li><a href="' + tag.link + '/' + tag_word +'" style="font-size: ' + str(font_size) + 'px;">' + urllib.unquote(tag_word) + ' (' + str(tag_count)  +')</a></li>'
      except: 
        pass
    # except: pass

  def tag_text(self,tag_word,user_id):
    self.text_entries = ''
    try:
      if user_id < 1:
        for text_id in r.lrange("word:" + str(tag_word) + ":texts",0,100):
          self.text_entries += '<li>' + urllib.unquote(r.get("text:" + str(text_id))) + '</li>'
      else:
        for text_id in r.lrange("uid:" + str(web.config.session_parameters['user_id']) + ":" + tag_word + ":texts",0,100):
          self.text_entries += '<li>' + urllib.unquote(r.get("text:" + str(text_id))) + ' <a href="/delete/' + tag_word + '/' + str(text_id) + '">delete</a></li>'
    except: self.text_entries = '<li>No such tag found</li>'
    return self.text_entries

  def add(self,tag_word,feed_id):
    if not r.exists("word:" + str(tag_word) + ":tid"):
      tag_id = r.incr("global:nextTagId")
      user_id = r.get("fid:" + str(feed_id) + ":uid")
      r.set("tid:" + str(tag_id) + ":word",clean_quotes.sub('',(urllib.quote(clean_word.sub('',tag_word)))))
      r.set("word:" + str(tag_word) + ":tid", tag_id)
      r.push("global:tags",tag_id)
      r.set("uid:" + str(r.get("fid:" + str(feed_id) + ":tid")),tag_id)
    if not r.exists("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tid"):
      r.push("uid:" + str(r.get("fid:" + str(feed_id) + ":uid")) + ":tags",tag_id)
    r.save()

  def delete_text(self,tag_word,text_id):
    if web.config.session_parameters['user_id'] and r.get("text:" + str(text_id) + ":uid") == web.config.session_parameters['user_id']:
      r.delete("text:" + str(text_id))
      r.lrem("word:" + str(tag_word) + ":texts",text_id)
      r.decr("word:" + str(tag_word) + ":count")
      r.decr("uid:" + str(web.config.session_parameters['user_id']) + ":" + str(tag_word) + ":count")
      r.lrem("uid:" + str(web.config.session_parameters['user_id']) + ":" + str(tag_word) + ":texts",text_id)
      r.save()

  def _format_time(self,time):
    if int(time) < 10:
      return '0' + str(time)
    return str(time)

  def _format_date(self,text):
    date = datetime.utcfromtimestamp(float(text))
    return '<span>' + str(date.year) + '/' + str(date.month) + '/' + str(date.day) + ' ' + self._format_time(date.hour) + ':' + self._format_time(date.minute) + ' </span> '