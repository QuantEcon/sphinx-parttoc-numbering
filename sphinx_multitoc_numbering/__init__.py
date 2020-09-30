# -*- coding: utf-8 -*-
"""
    sphinx_multitoc_numbering
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    A sphinx extension for continuous numbering of sections across toctrees.
"""

from typing import Dict, List, Set, Tuple
from typing import cast

from docutils import nodes
from docutils.nodes import Element

from sphinx import addnodes
from sphinx.environment import BuildEnvironment
from sphinx.locale import __
from sphinx.util import url_re, logging

logger = logging.getLogger(__name__)

__version__ = "0.0.1"
"""sphinx-multitoc-numbering version"""


def assign_section_numbers(self, env: BuildEnvironment) -> List[str]:
    """Assign a section number to each heading under a numbered toctree."""
    # a list of all docnames whose section numbers changed
    rewrite_needed = []

    assigned = set()  # type: Set[str]
    old_secnumbers = env.toc_secnumbers
    env.toc_secnumbers = {}
    self.last_chapter_number = 0

    def _walk_toc(
        node: Element, secnums: Dict, depth: int, titlenode: nodes.title = None
    ) -> None:
        # titlenode is the title of the document, it will get assigned a
        # secnumber too, so that it shows up in next/prev/parent rellinks
        for subnode in node.children:
            if isinstance(subnode, nodes.bullet_list):
                numstack.append(0)
                _walk_toc(subnode, secnums, depth - 1, titlenode)
                numstack.pop()
                titlenode = None
            elif isinstance(subnode, nodes.list_item):
                _walk_toc(subnode, secnums, depth, titlenode)
                titlenode = None
            elif isinstance(subnode, addnodes.only):
                # at this stage we don't know yet which sections are going
                # to be included; just include all of them, even if it leads
                # to gaps in the numbering
                _walk_toc(subnode, secnums, depth, titlenode)
                titlenode = None
            elif isinstance(subnode, addnodes.compact_paragraph):
                numstack[-1] += 1
                reference = cast(nodes.reference, subnode[0])

                # if a new chapter is encountered increment the chapter number
                if len(numstack) == 1:
                    self.last_chapter_number += 1
                if depth > 0:
                    number = list(numstack)
                    secnums[reference["anchorname"]] = tuple(numstack)
                else:
                    number = None
                    secnums[reference["anchorname"]] = None
                reference["secnumber"] = number
                if titlenode:
                    titlenode["secnumber"] = number
                    titlenode = None
            elif isinstance(subnode, addnodes.toctree):
                _walk_toctree(subnode, depth)

    def _walk_toctree(toctreenode: addnodes.toctree, depth: int) -> None:
        if depth == 0:
            return
        for (title, ref) in toctreenode["entries"]:
            if url_re.match(ref) or ref == "self":
                # don't mess with those
                continue
            elif ref in assigned:
                logger.warning(
                    __(
                        "%s is already assigned section numbers "
                        "(nested numbered toctree?)"
                    ),
                    ref,
                    location=toctreenode,
                    type="toc",
                    subtype="secnum",
                )
            elif ref in env.tocs:
                secnums = {}  # type: Dict[str, Tuple[int, ...]]
                env.toc_secnumbers[ref] = secnums
                assigned.add(ref)
                _walk_toc(env.tocs[ref], secnums, depth, env.titles.get(ref))
                if secnums != old_secnumbers.get(ref):
                    rewrite_needed.append(ref)

    for docname in env.numbered_toctrees:
        assigned.add(docname)
        doctree = env.get_doctree(docname)
        for toctreenode in doctree.traverse(addnodes.toctree):
            depth = toctreenode.get("numbered", 0)
            if depth:
                # every numbered toctree continues the numbering
                self.last_chapter_number = 0
                numstack = [self.last_chapter_number]
                _walk_toctree(toctreenode, depth)

    return rewrite_needed


def setup(app):
    from sphinx.environment.collectors.toctree import TocTreeCollector

    TocTreeCollector.assign_section_numbers = assign_section_numbers
