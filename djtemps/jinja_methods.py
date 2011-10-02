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


'''
    sayfa sayısı == 1 ise pagination yok
    sayfa sayısı > 1 ise 
        - start = 1
        - end = page.num
        - step = display step , her zaman current page - step/2, current_page + step/2
'''


def pagination(page, req=None, step=3, identifier='page', element="li", 
               current_class = "pagination_current", next_prev_class="pagination_next_prev",
              previous="Previous", next="Next"):

    first = 1
    last = page.paginator.num_pages
    current = page.number 

    if first == last:
        return ''
    
    #ranges, left_r = current-step -> current , right_r = current -> current + step
    left_r = current > first + step and current - step or 1
    right_r = current < last - step and step + current or last
    p_range = range(left_r, right_r + 1)


    def req_str(j):
        rs = "&".join(["%s=%s" % (key, val) for key, val in req.GET.items() if key != identifier])
        return rs and "?%s&%s=%s" % (rs, identifier, j) or "?%s=%s" % (identifier, j)

    
    pagination_str = ""

    if first not in p_range:
        pagination_str += '<%s><a href="%s">1</a></%s><%s>..</%s>' % (element, req_str(first), element, element, element)
    
    for i in p_range:
        if i == current:
            pagination_str += '<%s class="%s"><a href="%s">%d</a></%s>' % (element, current_class, req_str(i), i, element)
            continue

        pagination_str += '<%s><a href="%s">%d</a></%s>' % (element, req_str(i), i, element)

    if last not in p_range:
        pagination_str += '<%s>..</%s><%s><a href="%s">%s</a></%s>' % (element, element, element, req_str(last),
                                                                   last,  element,)

    
    if page.has_previous():
        pagination_str = '<%s><a href="%s">%s</a></%s>%s' % (element,req_str(page.previous_page_number()),
                                                             previous, element, pagination_str)
    else:
        pagination_str = '<%s>%s</%s>%s' % (element,previous,  element, pagination_str)
   
    if page.has_next():
        pagination_str = '%s<%s><a href="%s">%s</a></%s>' % (pagination_str, element,req_str(page.next_page_number()),
                                                             next, element)
    else:
        pagination_str = '%s<%s>%s</%s>' % (pagination_str, element, next,  element)

    return pagination_str




