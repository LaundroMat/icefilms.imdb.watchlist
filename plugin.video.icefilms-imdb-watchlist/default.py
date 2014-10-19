import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, sys
import feedparser
from bs4 import BeautifulSoup

_WATCHLIST_FEED_URL = "http://rss.imdb.com/user/ur0531641/watchlist"

_ADDON_NAME = 'plugin.video.imdb-watchlist'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_id = int(sys.argv[1])
_addon_url = sys.argv[0]
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())


def get_watchlist_entries(feed=_WATCHLIST_FEED_URL):
    d = feedparser.parse(feed)
    return [entry.title for entry in d.entries]


entries = get_watchlist_entries()
for entry in entries:
    url = urllib.quote_plus("http://www.icefilms.info/")
    listitem = xbmcgui.ListItem(label=entry)
    listitem.setInfo(
        type="video",
        infoLabels={'Title': entry}
    )
    xbmcplugin.addDirectoryItem(
        _addon_id,
        url="plugin://plugin.video.icefilms/?mode=555&url=%s&search=%s&nextPage=0" % (url, entry),
        listitem=listitem,
        totalItems=len(entries),
        isFolder=True
        )

xbmcplugin.addSortMethod(_addon_id, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
xbmcplugin.endOfDirectory(_addon_id, updateListing=True)
