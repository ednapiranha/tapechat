# Tapechat Beta

Tapechat is a small web.py app that takes RSS feeds and tagifies words in each RSS entry.

## Requires:
* [Python 2.6+](http://www.python.org/ "Python")
* [web.py](http://webpy.org/ "web.py")
* [Redis 1.02](http://code.google.com/p/redis/ "Redis")
* [redis-py](http://github.com/andymccurdy/redis-py "redis-py")
* [auto_tagify](http://pypi.python.org/pypi?:action=display&name=auto_tagify "auto_tagify") if you have easy_install or pip: easy_install auto_tagify or pip install auto_tagify)


## How to use:
Start the server by loading tapechat.py and create a user account. Add RSS feeds and then run tapechat_generate.py to process the feeds. If you want to process feeds on an automated basis, set a cron job on tapechat_generate.py.

This is still in development, so more updates will be coming soon.