from __future__ import unicode_literals

import re

from .common import InfoExtractor


class EmpflixIE(InfoExtractor):
    _VALID_URL = r'^https?://www\.empflix\.com/videos/.*?-(?P<id>[0-9]+)\.html'
    _TEST = {
        'url': 'http://www.empflix.com/videos/Amateur-Finger-Fuck-33051.html',
        'md5': 'b1bc15b6412d33902d6e5952035fcabc',
        'info_dict': {
            'id': '33051',
            'ext': 'mp4',
            'title': 'Amateur Finger Fuck',
            'description': 'Amateur solo finger fucking.',
            'age_limit': 18,
        }
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        webpage = self._download_webpage(url, video_id)
        age_limit = self._rta_search(webpage)

        video_title = self._html_search_regex(
            r'name="title" value="(?P<title>[^"]*)"', webpage, 'title')
        video_description = self._html_search_regex(
            r'name="description" value="([^"]*)"', webpage, 'description', fatal=False)

        cfg_url = self._html_search_regex(
            r'flashvars\.config = escape\("([^"]+)"',
            webpage, 'flashvars.config')

        # XML is malformed
        cfg_xml = self._download_webpage(
            cfg_url, video_id, note='Downloading metadata')

        formats = [
            {
                'url': item[1],
                'format_id': item[0],
            } for item in re.findall(
                r'<item>\s*<res>([^>]+)</res>\s*<videoLink>([^<]+)</videoLink>\s*</item>', cfg_xml)
        ]

        thumbnail = self._html_search_regex(
            r'<startThumb>([^<]+)</startThumb>', cfg_xml, 'thumbnail', fatal=False)

        return {
            'id': video_id,
            'title': video_title,
            'description': video_description,
            'thumbnail': thumbnail,
            'formats': formats,
            'age_limit': age_limit,
        }
