from django.template import Library


register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list():
    pass