from django import template
from django.db.models import Sum

from ..models import Visitor

register = template.Library()


class VisitorsOnSite(template.Node):
    """
    Injects the number of active users on your site as an integer into the context
    """

    def __init__(self, varname, type=None):
        """
        :param varname:
        :param type: same_page/ pv / uv
        """
        self.varname = varname
        self.type = type

    def render(self, context):
        if self.type == 'same_page':
            try:
                request = context['request']
                count = Visitor.objects.active().filter(
                    url=request.path).count()
            except KeyError:
                raise template.TemplateSyntaxError(
                    "Please add 'django.core.context_processors.request' to your TEMPLATE_CONTEXT_PROCESSORS if you want to see how many users are on the same page.")
        elif self.type == 'pv':
            pv_dict = Visitor.objects.aggregate(pv=Sum('page_views'))
            count = pv_dict.get('pv', 0)
        elif self.type == 'uv':
            count = Visitor.objects.all().count()
        else:
            count = Visitor.objects.active().count()

        context[self.varname] = count
        return ''


def visitors_on_site(parser, token):
    """
    Determines the number of active users on your site and puts it into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitors_on_site usage: {% visitors_on_site as visitors %}')

    return VisitorsOnSite(varname)


register.tag(visitors_on_site)


def visitors_on_page(parser, token):
    """
    Determines the number of active users on the same page and puts it into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitors_on_page usage: {% visitors_on_page as visitors %}')

    return VisitorsOnSite(varname, type='same_page')


register.tag(visitors_on_page)


def pv_on_site(parser, token):
    """
    pv into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'pv_on_site usage: {% pv_on_site as pv %}')

    return VisitorsOnSite(varname, type='pv')


register.tag(pv_on_site)


def uv_on_site(parser, token):
    """
    uv into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'uv_on_site usage: {% uv_on_site as uv %}')

    return VisitorsOnSite(varname, type='uv')


register.tag(uv_on_site)
