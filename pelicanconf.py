AUTHOR = 'dword4'
SITENAME = 'dword4'
SITEURL = 'https://dword4.github.io'

PATH = 'content'
#THEME = '/home/dhynes/pelican-themes/tuxlite_zf'
THEME = '/home/dhynes/.pyenv/versions/3.10.7/envs/blog-dev/lib/python3.10/site-packages/pelican/themes/tuxlite_zf'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

TYPOGRIFY = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('DazedPro', 'https://www.dazedpro.com/'),
         ('mikep', 'https://mpietruszka.com/'))

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
