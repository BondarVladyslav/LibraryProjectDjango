from django import template
from books.views import menu
register = template.Library()


@register.simple_tag()
def get_menu_data():
    return menu