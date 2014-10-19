import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, sys
import re
import feedparser
from BeautifulSoup import BeautifulSoup
import requests

# TODO:
# When looking for available links, remove "The" (i.e. 'The Hunger Games' -> 'Hunger Games')

_WATCHLIST_FEED_URL = "http://rss.imdb.com/user/ur0531641/watchlist"
_ICEFILMS_URL = "http://www.icefilms.info/"

_ADDON_NAME = 'plugin.video.imdb-watchlist'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_id = int(sys.argv[1])
_addon_url = sys.argv[0]
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())


def get_watchlist_entries(feed=_WATCHLIST_FEED_URL):
    d = feedparser.parse(feed)
    return [{'title': entry.title, 'icefilms_link': get_movie_link(entry.title)} for entry in d.entries]


def get_movie_link(title):
    # Get title first letter
    if title[0].isalpha():
        url = _ICEFILMS_URL + "movies/a-z/" + title[0].upper()
    else:
        url = _ICEFILMS_URL + "movies/a-z/1"

    try:
        xbmc.log("Looking in %s for %s" % (url, title))
    except UnicodeEncodeError:
        xbmc.log("Looking for movies title that generates a UnicodeEncodeError so I won't name it here.")
    html = requests.get(url)

    soup = BeautifulSoup(html.content)
    # All links to movies have "ip.php" in their href
    # This returns a list of (if there's a match) NavigableStrings (containing the movie title)
    # Each NavigableString's parent is a Tag, whose 'href' attribute is the URL to pass to icefilms plugin.
    link = soup.find("a", href=re.compile("ip.php"), text=title)
    if link:
        return link.parent["href"]
    else:
        return None


entries = get_watchlist_entries()
for entry in entries:
    url = urllib.quote_plus(_ICEFILMS_URL)
    listitem = xbmcgui.ListItem(label=entry['title'])
    link = entry['icefilms_link']
    listitem.setInfo(
        type="video",
        infoLabels={
            'Title': entry['title'],
            'playcount': "1" if link else "0"}
    )

    # URL required by icefilms plugin is of the form
    # http://www.icefilms.info/ip.php?v=193445&

    movie_sources_url = "plugin://plugin.video.icefilms/"
    if entry['icefilms_link']:
        movie_sources_url += "?mode=100&url=%s" % _ICEFILMS_URL + entry['icefilms_link']
    else:
        movie_sources_url += "?mode=555&url=%s&search=%s&nextPage=0" % (url, entry['title'])

    xbmcplugin.addDirectoryItem(
        _addon_id,
        url=movie_sources_url,
        listitem=listitem,
        totalItems=len(entries),
        isFolder=True
        )

xbmcplugin.addSortMethod(
    _addon_id,
    xbmcplugin.SORT_METHOD_VIDEO_TITLE
)

xbmcplugin.addSortMethod(
    _addon_id,
    xbmcplugin.SORT_METHOD_PLAYCOUNT
)

xbmcplugin.endOfDirectory(_addon_id, updateListing=True)


