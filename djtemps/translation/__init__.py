# ~*~ coding:utf-8 ~*~

import re


from django.utils.translation import * 
from django.utils.translation.trans_real import *
import inspect

""" adding jinja templates translation support 
    usage: {% trans %} text to be translated {% endtrans %}

"""
block_re = re.compile(r"""^\s*(blocktrans|trans)(?:\s+|$)""")
endblock_re = re.compile(r"""^\s*(endblocktrans|endtrans)(?:\s+|$)""")


"""
    re-initializing templatize code tobe able to use block_re and endblock_re. thanks to warvariuc
    http://stackoverflow.com/questions/7206048/forcing-imported-method-to-use-local-variables/7209081#7209081
"""

templatize_code = inspect.getsource(templatize)
exec templatize_code




