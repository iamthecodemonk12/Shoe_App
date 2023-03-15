import builtins as _builtins
import pprint as _pprint

from django import template
from django.utils.html import escape


register = template.Library()

NEW_LINE = "\n"

def _isvalidtag(tag):
    return True # come back to this


@register.filter
def dir(value, arg="pre"):
    tag = str(arg);
    if arg and _isvalidtag(tag):
        code_f = '<{tag}>{txt}</{tag}>'
    else:
        return _builtins.dir(value)
    try:
        return code_f.format(tag=tag, txt=escape(_pprint.pformat(_builtins.dir(value))))
    except Exception as e:
        return "Error in formatting: %s: %s" % (e.__class__.__name__, e)


@register.filter
def stat(value, arg=False):
    # details about an object *arg* represents presence of privates attributes
    types = {}
    show_privates = arg
    for i in _builtins.dir(value):
        name, _type = i, getattr(value, i).__class__.__name__
        if not show_privates and i.startswith('_'):
            continue
        types.setdefault(_type, [])
        types[_type].append(name)
    buffer = ["Documentation on <b>" + escape(repr(value)) + '</b>', "--No doc" or getattr(value, '__doc__')]
    append = buffer.append
    append("-- Objects")
    append(_pprint.pformat(types))
    return '<pre>' + NEW_LINE.join(buffer) + '</pre>'


@register.filter#(name="type")
def gettype(value, arg=None):
    return type(value)


t = ('list', 'tuple', 'dict')

@register.filter(name='type')
def typeout(value, arg=None):
    if arg and arg in t:
        type = getattr(_builtins, arg)
        return type(value)
    return 'invalid arg %s'%(arg)