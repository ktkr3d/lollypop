#!/usr/bin/python
# Copyright (c) 2014-2015 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gio

from gettext import gettext as _
from locale import getdefaultlocale
import wikipedia

class Wikipedia:
    """
        Init wikipedia
    """
    def __init__(self):
        language=getdefaultlocale()[0][0:2]
        wikipedia.set_lang(language)
        # Translators: Put here words added by wikipedia in band search
        # Ex: Muse_(band), Peaches(musician)
        self._search_str = _("musician;band")

    """
        Get artist infos
        @param artist as str
        @return (url as str, image url as str, content as str)
    """
    def get_artist_infos(self, artist):
        if not Gio.NetworkMonitor.get_default().get_network_available():
            return (None, None, None)
        try:
            page = self._search_page(artist)
            if page is None:
                return (None, None, None)
            content = page.content
            url = page.url
            img = None
            for image in page.images:
                if image.lower().endswith('.jpg'):
                    img = image
                    break
            return (url, img, content)
        except:
            return (None, None, None)

#######################
# PRIVATE             #
#######################
    """
        Search music page
        @param artist as string
        @return page as WikipediaPage
    """
    def _search_page(self, artist, items=None):
        if items is None:
            item = None
            items = self._search_str.split(';')
        elif items:
            item = items.pop(0)
        else:
            return None
        try:
            if item:
                page = wikipedia.page("%s\_\(%s\)" % (artist, item))
            else:
                page = wikipedia.page(artist)
        except:
            print("%s\_\(%s\)" % (artist, item))
            return self._search_page(artist, items)
        return page
