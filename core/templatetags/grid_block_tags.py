from django import template

register = template.Library()

@register.simple_tag()
def two_column_layout(breakpoint, column_layout):
    layout={}
    layout['left'], layout['right'] = column_layout.split('-') 
    if breakpoint == '-':
        breakpoint = ''
    layout['left'] = breakpoint + (('-' + layout['left']) if layout['left'] else '')
    layout['right'] = breakpoint + (('-' + layout['right']) if layout['right'] else '')
    return layout
    
@register.simple_tag()
def three_column_layout(breakpoint, column_layout):
    layout={}
    layout['left'], layout['centre'], layout['right'] = column_layout.split('-') 
    if breakpoint == '-':
        breakpoint = ''
    layout['left'] = breakpoint + (('-' + layout['left']) if layout['left'] else '')
    layout['centre'] = breakpoint + (('-' + layout['centre']) if layout['centre'] else '')
    layout['right'] = breakpoint + (('-' + layout['right']) if layout['right'] else '')
    return layout
