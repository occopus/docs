# Extension for Sphinx to document Info Broker keys

from docutils import nodes

class ibkey(nodes.Admonition, nodes.Element):
    pass

class ibkeylist(nodes.General, nodes.Element):
    pass

def visit_ibkey_node(self, node):
    self.visit_admonition(node)

def depart_ibkey_node(self, node):
    self.depart_admonition(node)

from docutils.parsers.rst import Directive

class IBKeyListDirective(Directive):
    def run(self):
        return [ibkeylist('')]

from sphinx.util.compat import make_admonition
from sphinx.locale import _

class IBKeyDirective(Directive):
    has_content = True

    def run(self):
        env = self.state.document.settings.env

        targetid = 'ibkey-{0}'.format(env.new_serialno('ibkey'))
        targetnode = nodes.target('', '', ids=[targetid])

        ad = make_admonition(ibkey, self.name, [_('IB Key')], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)

        if not hasattr(env, 'ibkey_all_ibkeys'):
            env.ibkey_all_ibkeys = list()
        env.ibkey_all_ibkeys.append(dict(
            docname=env.docname,
            lineno=self.lineno,
            ibkey=ad[0].deepcopy(),
            target=targetnode))

        return [targetnode] + ad

def purge_ibkeys(app, env, docname):
    if not hasattr(env, 'ibkey_all_ibkeys'):
        return

    env.ibkey_all_ibkeys = [i for i in env.ibkey_all_ibkeys
                            if i['docname'] != docname]

def process_ibkey_nodes(app, doctree, fromdocname):
    env = app.builder.env

    for node in doctree.traverse(ibkeylist):
        content = list()

        for key_info in env.ibkey_all_ibkeys:
            docname  = key_info['docname']

            para = nodes.paragraph()
            filename = env.doc2path(docname, base=None)
            description = (
                _("(Original entry: '{0}':{1} ").format(filename,
                                                        key_info['lineno']))
            para += nodes.Text(description, description)

            newnode = nodes.reference('', '')
            innernode = nodes.emphasis(_('here'), _('here'))
            newnode['refdocname'] = docname
            newnode['refuri'] = app.builder.get_relative_uri(
                fromdocname, docname)
            newnode['refuri'] += "#{0}".format(key_info['target']['refid'])
            newnode.append(innernode)

            para += newnode
            para += nodes.Text('.)', '.)')

            content.append(key_info['ibkey'])
            content.append(para)

        node.replace_self(content)


def setup(app):
    #app.add_config_value('xxx', False, False)
    app.add_node(ibkeylist)
    app.add_node(ibkey,
                 html=(visit_ibkey_node, depart_ibkey_node),
                 latex=(visit_ibkey_node, depart_ibkey_node),
                 text=(visit_ibkey_node, depart_ibkey_node))
    app.add_directive('ibkey', IBKeyDirective)
    app.add_directive('ibkeylist', IBKeyListDirective)
    app.connect('doctree-resolved', process_ibkey_nodes)
    app.connect('env-purge-doc', purge_ibkeys)
