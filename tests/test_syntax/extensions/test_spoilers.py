# -*- coding: utf-8 -*-
"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from __future__ import unicode_literals
from markdown.test_tools import TestCase


class TestSpoilers(TestCase):

    def test_postfix_notation(self):
        """Test postfix spoiler notation."""
        for symbol in ["/spoiler", "#spoiler", "/s", "#s"]:
            self.assertMarkdownRenders(
                'This will be a spoiler: [everybody dies!](%s)' % symbol,
                '<p>This will be a spoiler: '
                '<span class="spoiler">everybody dies!</span></p>',
                extensions=['spoilers'],
            )

    def test_tagged_notation(self):
        """Test tagged spoiler notation."""
        for symbol in ["/spoiler", "#spoiler", "/s", "#s"]:
            self.assertMarkdownRenders(
                'This will be a spoiler: [Season 4](%s everybody dies!)' % symbol,
                '<p>This will be a spoiler: '
                '<span class="spoiler" topic="Season 4">everybody dies!</span></p>',
                extensions=['spoilers'],
            )

    def test_tagged_notation_with_quotes(self):
        """Test tagged spoiler notation."""
        for symbol in ["/spoiler", "#spoiler", "/s", "#s"]:
            self.assertMarkdownRenders(
                'This will be a spoiler: [Season 4](%s "everybody dies!")' % symbol,
                '<p>This will be a spoiler: '
                '<span class="spoiler" topic="Season 4">everybody dies!</span></p>',
                extensions=['spoilers'],
            )

    def test_tagged_notation_multiple(self):
        """Test multiple tagged spoiler notation."""
        for symbol in ["/spoiler", "#spoiler", "/s", "#s"]:
            self.assertMarkdownRenders(
                'This will be a spoiler: [Season 4](%s everybody dies!)' % symbol + \
                ' also they are [Episode 7](%s killed by the monster).' % symbol,
                '<p>This will be a spoiler: '
                '<span class="spoiler" topic="Season 4">everybody dies!</span>'
                ' also they are <span class="spoiler" topic="Episode 7">killed by the monster</span>.'
                '</p>',
                extensions=['spoilers'],
            )

    def test_new_notation(self):
        """Test for reddit's new notation of the format >!Spoiler!<"""
        self.assertMarkdownRenders(
            'This will be a spoiler: >!everybody dies!!<',
            '<p>This will be a spoiler: '
            '<span class="spoiler">everybody dies!''</span></p>',
            extensions=['spoilers'],
        )
