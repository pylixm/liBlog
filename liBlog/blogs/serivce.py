# -*- coding: utf-8 -*-
import mistune
from mistune_contrib.toc import TocMixin
from mistune_contrib.highlight import HighlightMixin


class TocRenderer(TocMixin, HighlightMixin, mistune.Renderer):

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%s"><a href="#%s" class="headerlink"></a>%s</h%d>\n' % (
            level, self.toc_count, text, text, level)
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv
