#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'james fallisgaard'
SITENAME = u'jamesnewbrain'
SITEURL = ''

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = False
RELATIVE_URLS = False

# Markdown Plugins
MD_EXTENSIONS = (
    'codehilite',
    'toc',
    'extra',
)

DISQUS_SITENAME = 'jamesnewbrain'

PLUGIN_PATH = 'plugins'
PLUGINS = ['extract_toc']

THEME = "themes/elegant"
