# ~*~ coding:utf-8 ~*~

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

__all__ =  ["url_for", "enum", "pagination", "plain_pagination", 'logger']

import logging
''' logging in templates 
    usage: {{ logger.debug('blah')}}
'''
logger = logging.getLogger('templates')
mlogger = logging.getLogger(__name__)

def url_for(view_name, *args, **kwargs):
    return reverse(view_name, args=args, kwargs=kwargs)

def enum(l):
    ''' enumerate starting from 1'''
    i = 1
    for item in l:
        yield (i, item)
        i += 1


def _addPageNumToRequest(pagenum, request, identifier="page"):
    req = '?%s=%s' % (identifier, pagenum)
    if request:
        req += "&".join(["%s=%s" % (key, val) for key, val in request.GET.items() if key != identifier])
    return req

def ipag(number, i, req=None, identifier='page'):
    ''' inner pagination '''
    if number == i:
        return "<li class='currentpage'><a href='%s'>%d</a></li>\n" % (_addPageNumToRequest(i, req, identifier),i) 
    return "<li><a href='%s'>%d</a></li>\n" % (_addPageNumToRequest(i, req, identifier),i) 

def pagination(page, req=None, step=10, identifier='page'):
    ''' simple horrendous pagination code :'
        usage: {{ pagination(page_obj, request, step)}}
    '''
    total = page.paginator.num_pages

    if total == 1:
        return ""

    first = ipag(page.number, 1, req, identifier)
    last = ipag(page.number, total, req, identifier)

    tail = head = ""

    end = total - 1
    start = 2

    if page.number >= 2 + step:
        start = page.number - step
        head += '<li><span class="more" rel="%d-%d">...</span></li>\n' % (2, start)

    if page.number <= end - step:
        end = page.number + step
        tail += '<li><span class="more" rel="%d-%d">...</span></li>\n' % (end, total-1)

    data  = ''
    for i in range(start, end + 1):
         data += ipag(page.number, i, req)

    prev_link = u"<li class='previous disabled'>%s</li>\n" %  _('Previous')
    if page.has_previous():
        prev_link = u"<li class='previous'><a href='%s'>« %s </a></li>\n" % \
        (_addPageNumToRequest(page.previous_page_number(), req, identifier), _('Previous'))

    next_link = u"<li class='next disabled'>%s</li>\n" % _('Next') 
    if page.has_next():
        next_link = u"<li class='next'><a href='%s'> » %s </a></li>\n" % \
                ( _addPageNumToRequest(page.next_page_number(), req, identifier), _('Next'))

    return u"<ul id='pagination' class='horizontal'>%s%s%s%s%s%s%s</ul>" %(prev_link, first, head, data, tail, last, next_link)


def plain_pagination(curr, total, req=None, step=10):

    if total == 1:
        return ""

    first = ipag(curr, 1, req)
    last = ipag(curr, total, req)

    tail = head = ""

    end = total - 1
    start = 2

    if curr > 2 + step:
        start = curr - step
        head += '<li><span class="page_more" rel="%d-%d">...</span></li>\n' % (2, start)

    if curr < end - step:
        end = curr + step
        tail += '<li><span class="page_more" rel="%d-%d">...</span></li>\n' % (end, total-1)

    data  = ''
    for i in range(start, end + 1):
         data += ipag(curr, i, req)

    prev_link = u"<li class='previous disabled'>previous</li>\n" 
    if curr > 1:
        prev_link = u"<li class='previous'><a href='%s'>« previous</a></li>\n" % _addPageNumToRequest(curr - 1, req)

    next_link = u"<li class='next disabled'>next</li>\n" 
    if curr < total:
        next_link = u"<li class='next'><a href='%s'>next »</a></li>\n" % _addPageNumToRequest(curr + 1, req)

    return u"<ul id='plain_pagination' class='horizontal'>%s%s%s%s%s%s%s</ul>" %(prev_link, first, head, data, tail, last, next_link)

