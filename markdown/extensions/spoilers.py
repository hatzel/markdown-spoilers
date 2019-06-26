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

REDDIT_NOTATION_PATTERN = r'(\[(?P<tag>.*)\]\s)?>!\s?(?P<spoiler>.*?)\s?!<'


class SpoilerExtension(Extension):
    """Spoiler Extension. """

    def __init__(self, **kwargs):
        self.config = {}
        super(SpoilerExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add pieces to Markdown. """
        md.registerExtension(self)

        # Run after inline patterns parse markdown links
        md.treeprocessors.register(SpoilerLinkTreeprocessor(self), 'spoiler_links', 19)
        spoiler_processor = SpoilerInlineProcessor(REDDIT_NOTATION_PATTERN)

        # Run early in inline pattern process, we need to run before the LinkInlineProcessor
        md.inlinePatterns.register(spoiler_processor, 'spoiler_reddit', 165)

        # Run after SpoilerInlineProcessor to merge some nodes
        md.treeprocessors.register(SpoilerMergeTreeprocessor(self), 'spoiler_merger', 18)


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


class SpoilerMergeTreeprocessor(Treeprocessor):
    """
    Preprocessor to merge some spoiler tags.

    We only merge the specific case when one spoiler tag contains only one spoiler tag with only one of them having
    a topic.
    """

    def run(self, root):
        spoilers = root.findall(".//span[@class='spoiler']")
        for spoiler in spoilers:
            children = spoiler.findall("./span[@class='spoiler']")
            if (len(children) == 1 and (children[0].get("topic") is None or spoiler.get("topic") is None)):
                child = children[0]
                spoiler.text = (spoiler.text or "") + (child.text or "")
                spoiler.attrib["class"] = spoiler.get("class") or child.get("class")
                spoiler.remove(child)


class SpoilerInlineProcessor(InlineProcessor):
    """Processor for reddit's new inline spoiler syntax."""

    def handleMatch(self, m, data):
        spoiler = make_spoiler_tag(m.group("spoiler"), m.group("tag"))
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
