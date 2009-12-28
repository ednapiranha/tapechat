import web
from random import choice

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