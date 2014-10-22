icefilms.imdb.watchlist
=======================

Search icefilms to stream movies from your IMDB watchlist to XBMC.

Installation
============

[Download the zip file of the latest release](https://github.com/LaundroMat/icefilms.imdb.watchlist/releases/download/0.9/plugin.video.icefilms-imdb-watchlist.zip) and install it via XBMC [in the usual way](http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file).

You need to have [plugin.video.icefilms](http://superrepo.org/plugin.video.icefilms/) installed before you can use this plugin.

Setting up
==========

Go to settings first and enter the RSS feed URL of your public IMDB watchlist. You can find the URL by going to [imdb.com](http://www.imdb.com) and clicking "watchlist" in the top menu (you need to be logged in). 
Slightly above the bottom of the screen you'll find an RSS icon next to a link "Export this list". Click the RSS icon, and copy that URL in the settings of this plugin.

This plugin has only been tested on Windows 7, XBMC Gotham 13.2 and plugin.video.icefilms 1.5.1.

Enjoy!

PS - The plugin "misuses" the watched status of movies. If a movie in your watchlist is marked as watched, it in fact means that is available for streaming on Icefilms. No more frustration with "no sources found"!

TODO
====

* Make this testable (i.e. seperate XBMC specific routines from the rest)
* Better crawling (i.e. "The Hunger Games" is the same as "Hunger Games, The")
* ...


