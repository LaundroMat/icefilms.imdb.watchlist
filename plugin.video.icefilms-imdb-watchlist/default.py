import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, sys
import re
import feedparser
from BeautifulSoup import BeautifulSoup
import requests

_WATCHLIST_FEED_URL = "http://rss.imdb.com/user/ur0531641/watchlist"
_ICEFILMS_URL = "http://www.icefilms.info/"

_ADDON_NAME = 'plugin.video.imdb-watchlist'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_id = int(sys.argv[1])
_addon_url = sys.argv[0]
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())


def get_watchlist_entries(feed=_WATCHLIST_FEED_URL):
    d = feedparser.parse(feed)
    return [{'title': entry.title, 'available_links': len(check_for_links(entry.title))} for entry in d.entries]


def check_for_links(title):
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
    return soup.findAll("a", href=re.compile("ip.php"), text=title)


entries = get_watchlist_entries()
for entry in entries:
    url = urllib.quote_plus(_ICEFILMS_URL)
    listitem = xbmcgui.ListItem(label="%s (%i)" % (entry['title'], entry['available_links']))
    listitem.setInfo(
        type="video",
        infoLabels={
            'Title': entry['title'],
            'playcount': str(entry['available_links'])}
    )

    # URL required by icefilms plugin is of the form
    # http://www.icefilms.info/ip.php?v=193445&

    xbmcplugin.addDirectoryItem(
        _addon_id,
        url="plugin://plugin.video.icefilms/?mode=555&url=%s&search=%s&nextPage=0" % (url, entry),
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


