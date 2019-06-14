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
from markdown.treeprocessors import Treeprocessor


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


class SpoilerLinkTreeprocessor(Treeprocessor):
    """
    The history notation used on reddit.

    This notation relied on a hack, so links to specific urls are considered spoiler tags.
    """
    TAGS = ["/s", "/spoiler", "#s", "#spoiler"]

    def run(self, root):
        links = root.findall(".//a")
        for link in links:
            if link.get("href") in self.TAGS:
                link.tag = "span"
                link.attrib.clear()
                link.attrib["class"] = "spoiler"


def makeExtension(**kwargs):  # pragma: no cover
    """ Return an instance of the SpoilerExtension """
    return SpoilerExtension(**kwargs)
