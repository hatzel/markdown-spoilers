"""
Spoiler Extension for Python-Markdown
=======================================

Adds spoiler handling to Python-Markdown.

See <https://Python-Markdown.github.io/extensions/spoilers>
for documentation.

Copyright The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""
from . import Extension
from .. import util
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor

REDDIT_NOTATION_PATTERN = r'>!(?P<spoiler>.*?)!<'

class SpoilerExtension(Extension):
    """Spoiler Extension. """

    def __init__(self, **kwargs):
        self.config = {}
        super(SpoilerExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add pieces to Markdown. """
        md.registerExtension(self)

        # Execute after links were parsed
        md.treeprocessors.register(SpoilerLinkTreeprocessor(self), 'spoiler_links', 0)
        spoiler_processor = SpoilerInlineProcessor(REDDIT_NOTATION_PATTERN)
        md.inlinePatterns.register(spoiler_processor, 'spoiler_reddit', 165)


class SpoilerLinkTreeprocessor(Treeprocessor):
    """
    The history notation used on reddit.

    This notation relied on a hack, so links to specific URLs are considered spoiler tags.
    """
    TAGS = ["/spoiler", "/s", "#spoiler", "#s"]

    def run(self, root):
        links = root.findall(".//a")
        for link in links:
            if link.get("href") in self.TAGS:
                if link.get("title") is not None:
                    text = link.text
                    link.text = link.get("title")
                    mark_spoiler(link, topic=text)
                else:
                    mark_spoiler(link)
            else:
                for tag in self.TAGS:
                    if link.get("href") is not None \
                       and link.get("href").startswith(tag + " "):
                        new_text = link.attrib["href"][len(tag) + 1:]
                        mark_spoiler(link, topic=link.text)
                        link.text = new_text
                        break


class SpoilerInlineProcessor(InlineProcessor):
    """Processor for reddit's new inline spoiler syntax."""

    def handleMatch(self, m, data):
        spoiler = make_spoiler_tag(m.group("spoiler"))
        return spoiler, m.start(0), m.end(0)


def make_spoiler_tag(text=None, topic=None):
    """Create spoiler tree element."""
    spoiler = util.etree.Element("span")
    spoiler.attrib["class"] = "spoiler"
    if text is not None:
        spoiler.text = text
    if topic is not None:
        spoiler.attrib["topic"] = topic
    return spoiler


def mark_spoiler(element, topic=None):
    """Make tree element a spoiler span."""
    element.tag = "span"
    element.attrib.clear()
    element.attrib["class"] = "spoiler"
    if topic is not None:
        element.attrib["topic"] = topic


def makeExtension(**kwargs):  # pragma: no cover
    """ Return an instance of the SpoilerExtension """
    return SpoilerExtension(**kwargs)
