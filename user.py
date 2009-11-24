import hashlib
import string
import web
from time import time
from redis import Redis
from random import choice

r = Redis()

class User():   
  def create(self,email,password):
    if len(email.strip()) < 5 or len(password.strip()) < 4 or r.exists("email:" + email + ":uid"): return False
    self.email = email
    self.password = hashlib.md5(password).hexdigest()
    user_id = r.incr("global:nextUserId")
    r.set("uid:" + str(user_id) + ":email",self.email)
    r.set("uid:" + str(user_id) + ":password",self.password)
    r.set("email:" + self.email + ":uid",user_id)
    if self.login(self.email,password):
      return True
    return False
    
  def login(self,email,password):
    uid = r.get("email:" + email + ":uid")
    if not uid:
      return False
    if str(r.get("uid:" + str(uid) + ":password")) != hashlib.md5(password).hexdigest():
      return False

    chars = string.letters + string.digits
    new_auth = ''
    for i in range(50):
      new_auth += choice(chars)  
    r.set("auth:" + str(new_auth) + ":uid",uid)
    web.config.session_parameters['secret_key'] = str(new_auth)
    web.config.session_parameters['user_id'] = uid
    web.config.session_parameters['cookie_name'] = "tapechat_session_id"
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = 86400
    web.config.session_parameters['ignore_expiry'] = True
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['expired_message'] = 'Session expired'
    return True
  
  def is_logged_in(self):
    user_id = r.get("auth:" + web.config.session_parameters['secret_key'] + ":uid")
    if user_id and (user_id == web.config.session_parameters['user_id']):
      return True
    return False
      
  def logout(self):
    web.config.session_parameters['secret_key'] = 'none'
    web.config.session_parameters['user_id'] = 0
    