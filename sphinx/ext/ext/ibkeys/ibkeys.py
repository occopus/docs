# Extension for Sphinx to document Info Broker keys

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.nodes import nested_parse_with_titles

class declibkey(nodes.General, nodes.Element): pass

class keynode(nodes.literal):
    def __init__(self, key):
        super(keynode, self).__init__(key, key)

class keydoc(nodes.line_block):
    def __init__(self, state, content):
        super(keydoc, self).__init__('\n'.join(content))
        nested_parse_with_titles(state, content, self)

class ibkey(nodes.paragraph):
    def __init__(self, refkey, key_elem, doc):
        targetnode = nodes.target('', '', ids=[refkey])

        label = nodes.strong('@provides', '@provides')
        sep = nodes.Text(': ', ': ')
        par = nodes.paragraph('', '', label, sep, key_elem)

        super(ibkey, self).__init__('', '', targetnode, par, doc)

class iblist_entry(nodes.definition_list_item):
    def __init__(self, env, docname, lineno, refkey, key_elem, doc):

        filename = env.doc2path(docname, base=None)
        linktext = "{0}:{1}".format(filename, lineno)
        refnode = nodes.reference('', '', nodes.emphasis(linktext, linktext))
        refnode['refdocname'] = docname
        refnode['refuri'] = "{0}#{1}".format(
            env.app.builder.get_target_uri(docname), refkey)

        origentry = nodes.inline('', '',
                                 nodes.Text(' (', ' ('),
                                 refnode,
                                 nodes.Text(')', ')'))

        entry_header = nodes.term('', '', key_elem, origentry)
        entry_content = nodes.definition('', doc)

        super(iblist_entry, self).__init__('', entry_header, entry_content)

class ibkeylist(nodes.definition_list): pass

def visit_declibkey_node(self, node): self.visit_raw(node)
def depart_declibkey_node(self, node): self.depart_raw(node)
def visit_ibkey_node(self, node): self.visit_paragraph(node)
def depart_ibkey_node(self, node): self.depart_paragraph(node)
def visit_keydoc_node(self, node): self.visit_paragraph(node)
def depart_keydoc_node(self, node): self.depart_paragraph(node)
def visit_iblist_entry_node(self, node):
    self.visit_definition_list_item(node)
def depart_iblist_entry_node(self, node):
    self.depart_definition_list_item(node)
def visit_keynode_node(self, node): self.visit_literal(node)
def depart_keynode_node(self, node): self.depart_literal(node)

class DeclIBKey(Directive):
    has_content = True

    def run(self):
        # The declared key is valid in the scope of the parent docstring.
        self.content.parent.declared_ibkey = self.content[0]
        return []

class IBKeyListDirective(Directive):
    def run(self):
        return [ibkeylist('')]

from sphinx.util.docfields import DocFieldTransformer
from sphinx.directives import ObjectDescription
from sphinx.domains.python import PyObject

class IBKeyDirective(ObjectDescription):
    has_content = True
    doc_field_types = PyObject.doc_field_types

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
        docname = env.docname

        if ':' in self.name:
            self.domain, self.objtype = self.name.split(':', 1)
        else:
            self.domain, self.objtype = '', self.name

        #import yaml
        #def d(x): return yaml.dump(x, default_flow_style=False)
        #print d([i for i in dir(self.) if '' in i])

        key = self.find_key(self.content.parent)

        key_elem = keynode(key)
        doc = keydoc(self.state, self.content) 
        DocFieldTransformer(self).transform_all(doc)

        doc_entry = ibkey(key, key_elem, doc)
        catalog_entry = iblist_entry(
            env, docname, self.lineno, key, key_elem, doc)

        if not hasattr(env, 'ibkey_all_ibkeys'):
            env.ibkey_all_ibkeys = dict()

        env.ibkey_all_ibkeys[key] = dict(docname=docname,
                                         catalog_entry=catalog_entry)

        return [doc_entry]

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

    for nodename in ['ibkey', 'keydoc', 'declibkey', 'iblist_entry',
                     'keynode']:
        methods = tuple(g['{1}_{0}_node'.format(nodename, role)]
                        for role in ['visit', 'depart'])
        allmethods = dict((k,methods) for k in ['html', 'latex', 'text'])
        app.add_node(g[nodename], **allmethods)

    app.add_directive('ibkey', IBKeyDirective)
    app.add_directive('decl_ibkey', DeclIBKey)
    app.add_directive('ibkeylist', IBKeyListDirective)

    app.connect('doctree-resolved', process_ibkey_nodes)
    app.connect('env-purge-doc', purge_ibkeys)
