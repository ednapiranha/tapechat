import web
import urllib
import re
from user import User
from feed import Feed
from tapechat_tag import TapeChatTag

VALID_TAGS = ['a']

render = web.template.render('templates/')

urls = (
  '/','index',
  '/tags/(.*)','tags',
  '/delete/(.*)/([0-9]+)','delete',
  '/user/new','user_add',
  '/login','login',
  '/logout','logout',
  '/feed/new','feed_add'
)
app = web.application(urls, globals())

def layout_processor(handle):
  result = handle()
  return render.layout(result)

app.add_processor(layout_processor)
    
# tags
class index:  
  def GET(self):
    try:
      user_id = web.config.session_parameters['user_id']
    except: user_id = 0
      
    # try:
    chat_tag = TapeChatTag()  
    if web.input(page = 'page')['page']:
      chat_tag.page_value = web.input(page = 'page')['page']
    chat_tag.generate(user_id=user_id)
    return render.index(chat_tag.all_entries,chat_tag.next_page,chat_tag.prev_page,user_id)
    # except: return render.index('',-1,-1,user_id)

class tags:
  def GET(self,tag_word):
    chat_tag = TapeChatTag()
    try:
      user_id = web.config.session_parameters['user_id']
    except: user_id = 0
    return render.tags(chat_tag.tag_text(tag_word,user_id),urllib.unquote(tag_word),user_id)

class delete:
  def GET(self,tag_word,text_id):
    try:
      chat_tag = TapeChatTag()
      chat_tag.delete_text(tag_word,text_id)
      raise web.seeother('/tags/' + tag_word)
    except: raise web.seeother('/')

# feeds
class feed_add:
  def GET(self):
    user_id = web.config.session_parameters['user_id']
    error_message = None
    return render.feed_add(error_message,user_id)
  
  def POST(self):
    feed = Feed()
    if feed.add(web.input(url = 'url')['url']):
      raise web.seeother('/')
    else:
      user_id = web.config.session_parameters['user_id']
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
    user = User()
    if user.login(email,password):
      raise web.seeother('/')
    else:
      error_message = "Invalid email/password" 
      return render.login(error_message)

class logout:
  def GET(self):
    user = User()
    user.logout()
    raise web.seeother('/login')

class user_add:
  def GET(self):
    error_message = None
    return render.user_add(error_message)

  def POST(self):
    email = web.input(email = 'email')['email']
    password = web.input(password = 'password')['password']
    user = User()
    if user.create(email,password):
      raise web.seeother('/')
    else:
      error_message = "Invalid email/password" 
      return render.user_add(error_message)

if __name__ == '__main__': app.run()