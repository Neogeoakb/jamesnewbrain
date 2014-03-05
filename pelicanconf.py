#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Basic site identity
AUTHOR = u'james fallisgaard'
SITENAME = u'jamesnewbrain'
SITEURL = 'http://jamesnewbrain.com'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = u'en'
THEME = "themes/de-Harak"

# Pelican settings
FEED_ALL_ATOM = 'feeds/all.atom.xml'
DELETE_OUTPUT_DIRECTORY = True
DEFAULT_PAGINATION = False
RELATIVE_URLS = True

# Plugins and configuration
MD_EXTENSIONS = (
    'codehilite',
    'toc',
    'extra',
)
PLUGIN_PATH = 'plugins'
PLUGINS = []
DISQUS_SITENAME = 'jamesnewbrain'

# de-Harak theme specific
HEADER_CONTENT = {
    'bio': """
        <p>the online braindump of James Fallisgaard<br>currently working on <a href="./pages/nksaidwhat.html" rel="bookmark" title="Permalink to nksaidwhat">nksaidwhat</a></p> """,
}
NAVBAR_HOME_NAME = 'Posts & Projects'
NAVBAR_EXTRA_BUTTONS = [
    {
        'name': 'GitHub',
        'url': 'http://github.com/jfallisg'},
    {
        'name': '@jamesnewbrain',
        'url': 'http://twitter.com/jamesnewbrain'},
    {
        'name': 'Bing Bong Comics',
        'url': 'http://jamesnewbrain.tumblr.com'},
]
NAVBAR_ABOUT_NAME = 'james new who?'