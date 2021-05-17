from django import template

register = template.Library()

@register.simple_tag()
def two_column_layout(breakpoint, column_layout, horizontal_padding):
    layout={}
    layout['left'], layout['right'] = column_layout.split('-') 
    
    if breakpoint == '-':
        breakpoint = ''
        layout['horizontal_padding'] = 'px-' + str(horizontal_padding)
        layout['breakpoint_pixels'] = '0px'
        layout['pre_breakpoint_bottom_pad'] = ''
    else:
        layout['horizontal_padding'] = 'px' + breakpoint + '-' + str(horizontal_padding)
        if breakpoint == '-sm':
            layout['breakpoint_pixels'] = '575px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-sm-0'
        elif breakpoint == '-md':
            layout['breakpoint_pixels'] = '767px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-md-0'
        else:
            layout['breakpoint_pixels'] = '991px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-lg-0'

    layout['left'] = breakpoint + (('-' + layout['left']) if layout['left'] else '')
    layout['right'] = breakpoint + (('-' + layout['right']) if layout['right'] else '')

    return layout
    
@register.simple_tag()
def three_column_layout(breakpoint, column_layout, horizontal_padding):
    layout={}
    layout['left'], layout['centre'], layout['right'] = column_layout.split('-') 
    if breakpoint == '-':
        breakpoint = ''
        layout['horizontal_padding'] = 'px-' + str(horizontal_padding)
        layout['breakpoint_pixels'] = '0px'
        layout['pre_breakpoint_bottom_pad'] = ''
    else:
        layout['horizontal_padding'] = 'px' + breakpoint + '-' + str(horizontal_padding)
        if breakpoint == '-sm':
            layout['breakpoint_pixels'] = '575px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-sm-0'
        elif breakpoint == '-md':
            layout['breakpoint_pixels'] = '767px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-md-0'
        else:
            layout['breakpoint_pixels'] = '991px'
            layout['pre_breakpoint_bottom_pad'] = 'pb-3 pb-lg-0'

    layout['left'] = breakpoint + (('-' + layout['left']) if layout['left'] else '')
    layout['centre'] = breakpoint + (('-' + layout['centre']) if layout['centre'] else '')
    layout['right'] = breakpoint + (('-' + layout['right']) if layout['right'] else '')
    return layout
