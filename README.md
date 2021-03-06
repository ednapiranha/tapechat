# Tapechat Beta

Tapechat is a small web.py app that takes RSS feeds and tagifies words in each RSS entry.

## Requires:
* [Python 2.6+](http://www.python.org/ "Python")
* [web.py](http://webpy.org/ "web.py")
* [Redis 1.02](http://code.google.com/p/redis/ "Redis")
* [redis-py](http://github.com/andymccurdy/redis-py "redis-py")
* [BeautifulSoup](http://pypi.python.org/pypi/BeautifulSoup/ "Beautiful Soup") (pip install BeautifulSoup)
* [auto_tagify](http://pypi.python.org/pypi?:action=display&name=auto_tagify "auto_tagify") (easy_install auto_tagify or pip install auto_tagify)
* [feedparser](http://http://feedparser.org/ "feedparser")
* [simplejson] (http://pypi.python.org/pypi/simplejson "simplejson") (easy_install simplejson or pip install simplejson)
* [web_user_auth](http://github.com/ednapiranha/web_user_auth/blob/master/web_user_auth.py "web_user_auth")


## How to use:
Start the server by loading tapechat.py and create a user account. Add RSS feeds and then run tapechat_generate.py to process the feeds. If you want to process feeds on an automated basis, set a cron job on tapechat_generate.py.

This is still in development, so more updates will be coming soon.