import web
from random import choice

chars = string.letters + string.digits
new_auth = ''.join([str(''.join(str(i) for i in choice(chars))) for i in range(50)])

web.config.session_parameters['secret_key'] = str(new_auth)
web.config.session_parameters['cookie_name'] = "tapechat_session_id"
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['expired_message'] = 'Session expired'