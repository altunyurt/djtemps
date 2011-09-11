# ~*~ coding:utf-8 ~*~

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.utils import translation
from django.utils.translation import gettext, ngettext
from jinja2 import FileSystemLoader, Environment
import os
import sys

__all__ = ['render_to_response', 'render_to_string']

JINJA_FILTERS = getattr(settings, 'JINJA_FILTERS', [])
JINJA_METHODS = getattr(settings, 'JINJA_METHODS', [])

class DjangoTranslator(object):

    def __init__(self):
        self.gettext = gettext
        self.ngettext = ngettext

class DjangoEnvironment(Environment):

    def get_translator(self, context):
        return DjangoTranslator()


def _import(name):
    mod = None
    if '.' in name:
        module, dotted_name = os.path.splitext(name)
        __import__(module)
        mod = sys.modules[module]
        name = dotted_name.replace('.', '')
    else:
        ''' builtin methods such as str, int etc. '''
        mod = __import__('__builtin__')
    return getattr(mod, name), name


class JinjaRenderer(object):

    template_dirs = getattr(settings,'TEMPLATE_DIRS')
    default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
    global_exts = ['jinja2.ext.i18n', 'djtemps.jinja_extensions.CsrfExtension'] + \
        getattr(settings, 'JINJA_EXTENSIONS', [])
    
    env = DjangoEnvironment(autoescape=False, 
                            loader=FileSystemLoader(template_dirs, 
                                                    encoding="utf-8"), 
                            extensions=global_exts)

    env.install_gettext_translations(translation)
    
    # following are enabled in templates by default. comes handy.
    additional_context = {'settings':settings, 
                          'getattr':getattr, 
                          'str': str,
                          'int': int,
                          'float': float
                         }

    def __init__(self):
        '''
            add the methods or filters in your settings.py file as:
            JINJA_FILTERS = ['mymodule.myfilter']
            JINJA_METHODS = ['mymodule.method', 'somebuiltinmethod']

        '''
        for filter_name in JINJA_FILTERS:
            mod, name = _import(filter_name)
            self.env.filters.update({name: mod})

        for method_name in JINJA_METHODS:
            mod, name = _import(method_name)
            self.additional_context.update({name: mod})


    def render_to_string(self, filename, context={}, context_instance=Context({}), mimetype=None):
        _context = {}
        
        mimetype = mimetype or self.default_mimetype
        template = self.env.get_template(filename)

        for d in context_instance.dicts:
            _context.update(d)

        request = context.pop('request', None)
        if request:
            for d in RequestContext(request, context):
                _context.update(d)
            _context.update({'request':request})

        _context.update(context)

        _context.update(self.additional_context)
        return template.render(**_context)
    
        
    
    def render_to_response(self, filename, context={}, context_instance=Context({}), mimetype=None):
        mimetype = mimetype or self.default_mimetype
        rendered = self.render_to_string(filename, context=context, context_instance=context_instance,
                                    mimetype=mimetype)
        return HttpResponse(rendered, mimetype=mimetype)


j = JinjaRenderer()
render_to_response = j.render_to_response
render_to_string = j.render_to_string
