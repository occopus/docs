# Extension for Sphinx to document Info Broker keys

from docutils import nodes
from sphinx.util.nodes import nested_parse_with_titles

class declibkey(nodes.General, nodes.Element): pass
class ibkey(nodes.paragraph): pass
class ibkey_content(nodes.paragraph): pass
class ibkeylist(nodes.General, nodes.Element): pass
class iblist_entry(nodes.paragraph): pass

def visit_declibkey_node(self, node): self.visit_raw(node)
def depart_declibkey_node(self, node): self.depart_raw(node)
def visit_ibkey_node(self, node): self.visit_paragraph(node)
def depart_ibkey_node(self, node): self.depart_paragraph(node)
def visit_ibkey_content_node(self, node): self.visit_paragraph(node)
def depart_ibkey_content_node(self, node): self.depart_paragraph(node)
def visit_iblist_entry_node(self, node): self.visit_paragraph(node)
def depart_iblist_entry_node(self, node): self.depart_paragraph(node)

from docutils.parsers.rst import Directive

class DeclIBKey(Directive):
    has_content = True

    def run(self):
        # The declared key is valid in the scope of the parent docstring.
        self.content.parent.declared_ibkey = self.content[0]
        return []

class IBKeyListDirective(Directive):
    def run(self):
        return [ibkeylist('')]

from sphinx.util.compat import make_admonition
from sphinx.locale import _
from docutils.statemachine import ViewList

class IBKeyDirective(Directive):
    has_content = True

    def find_key(self, parent):
        if hasattr(parent, 'declared_ibkey'):
            return parent.declared_ibkey
        elif hasattr(parent, 'parent'):
            return self.find_key(parent.parent)
        else:
            raise Exception(
                'There is no declared key in the scope of this directive.')

    def run(self):
        env = self.state.document.settings.env

        key = self.find_key(self.content.parent)
        refkey = key

        docname = env.docname

        targetnode = nodes.target('', '', ids=[refkey])

        keynode = nodes.literal(key, key)
        label = nodes.strong('@provides', '@provides')
        sep = nodes.inline(': ', ': ')
        doc = ibkey_content(rawsource='\n'.join(self.content))
        doc.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, doc)

        p = ibkey('', '', label, sep, keynode, doc)
        catalog_entry = iblist_entry('', '')

        origentry = nodes.paragraph()
        filename = env.doc2path(docname, base=None)
        description = \
            _("(Original entry: '{0}':{1} ").format(filename, self.lineno)
        origentry += nodes.Text(description, description)

        refnode = nodes.reference('', '')
        innernode = nodes.emphasis(_('here'), _('here'))
        refnode['refdocname'] = docname
        refnode['refuri'] = "{0}#{1}".format(
            env.app.builder.get_target_uri(docname), refkey)

        refnode.append(innernode)

        origentry += refnode
        origentry += nodes.Text('.)', '.)')

        catalog_entry += keynode
        catalog_entry += origentry
        catalog_entry += doc

        if not hasattr(env, 'ibkey_all_ibkeys'):
            env.ibkey_all_ibkeys = dict()

        env.ibkey_all_ibkeys[key] = dict(docname=docname,
                                         catalog_entry=catalog_entry)

        return [targetnode, p]

def purge_ibkeys(app, env, docname):
    if not hasattr(env, 'ibkey_all_ibkeys'):
        return

    env.ibkey_all_ibkeys = dict((k, v)
                                for k, v in env.ibkey_all_ibkeys.iteritems()
                                if v['docname'] != docname)

def process_ibkey_nodes(app, doctree, fromdocname):
    env = app.builder.env

    for node in doctree.traverse(ibkeylist):
        content = list()

        all_ibkeys = env.ibkey_all_ibkeys

        for key in sorted(all_ibkeys.iterkeys()):
            content.append(all_ibkeys[key]['catalog_entry'])

        node.replace_self(content)


def setup(app):
    app.add_node(ibkeylist)
    g = globals()

    for nodename in ['ibkey', 'ibkey_content', 'declibkey', 'iblist_entry']:
        methods = tuple(g['{1}_{0}_node'.format(nodename, role)]
                        for role in ['visit', 'depart'])
        allmethods = dict((k,methods) for k in ['html', 'latex', 'text'])
        app.add_node(g[nodename], **allmethods)

    app.add_directive('ibkey', IBKeyDirective)
    app.add_directive('decl_ibkey', DeclIBKey)
    app.add_directive('ibkeylist', IBKeyListDirective)

    app.connect('doctree-resolved', process_ibkey_nodes)
    app.connect('env-purge-doc', purge_ibkeys)
