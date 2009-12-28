import web
import site
import urllib
import re
import simplejson
import web_user_auth
from web import session
from feed import Feed
from tapechat_tag import TapeChatTag

VALID_TAGS = ['a']
render = web.template.render('templates/', base='layout')
render_plain = web.template.render('templates/', base='plain')
valid_email = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)",re.IGNORECASE)

urls = (
  '/','index',
  '/tags/(.*)','tags',
  '/user/new','user_add',
  '/login','login',
  '/logout','logout',
  '/feed/new','feed_add',
  '/stream', 'index_stream',
  '/tag_stream/([0-9]+)', 'tag_stream'
)
app = web.application(urls, globals())

def layout_processor(handle):
  result = handle()
  return result
  
app.add_processor(layout_processor)

# tags
class index:  
  def GET(self):
    try:
      user_id = session.user_id
    except: user_id = 0
      
    try:
      chat_tag = TapeChatTag()  
      if web.input(page = 'page')['page']:
        chat_tag.page_value = web.input(page = 'page')['page']
      chat_tag.generate(user_id=user_id)
      return render.index(chat_tag.all_entries,chat_tag.next_page,chat_tag.prev_page,user_id)
    except: return render.index('',-1,-1,user_id)

class index_stream:
  def GET(self):
    try:
      user_id = session.user_id
    except: user_id = 0
    return render_plain.index_stream(user_id)

class tag_stream:
  def GET(self,tag_counter):
    try:
      user_id = session.user_id
    except: user_id = 0
    chat_tag = TapeChatTag()
    chat_tag.generate_stream(tag_counter)
    return simplejson.dumps(chat_tag.all_entries)

class tags:
  def GET(self,tag_word):
    chat_tag = TapeChatTag()
    try:
      user_id = session.user_id
    except: user_id = 0
    return render.tags(chat_tag.tag_text(tag_word,user_id),urllib.unquote(tag_word),user_id)

# feeds
class feed_add:
  def GET(self):
    user_id = session.user_id
    error_message = None
    return render.feed_add(error_message,user_id)
  
  def POST(self):
    feed = Feed()
    if feed.add(web.input(url = 'url')['url']):
      raise web.seeother('/')
    else:
      user_id = session.user_id
      error_message = "Invalid feed url"
      render.feed_add(error_message,user_id)

# users
class login:
  def GET(self):
    error_message = None
    return render.login(error_message)

  def POST(self):
    email = web.input(email = 'email')['email']
    password = web.input(password = 'password')['password']
    if web_user_auth.login(email,password):
      raise web.seeother('/')
    else:
      error_message = "Invalid email/password" 
      return render.login(error_message)

class logout:
  def GET(self):
    user = User()
    web_user_auth.logout()
    raise web.seeother('/login')

class user_add:
  def GET(self):
    error_message = None
    return render.user_add(error_message)

  def POST(self):
    email = web.input(email = 'email')['email']
    password = web.input(password = 'password')['password']
    if valid_email.match(email.strip()) and len(password) > 4 and web_user_auth.create(email,password):
      raise web.seeother('/')
    else:
      error_message = "Invalid email/password" 
      return render.user_add(error_message)

if __name__ == '__main__': app.run()