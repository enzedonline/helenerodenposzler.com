from django import template

register = template.Library()

@register.simple_tag()
def two_column_layout(value):
    left, right = value['column_layout'].split('-') 
    breakpoint = value['breakpoint']
    horizontal_padding = str(value['horizontal_padding'])
    lcol_collapse_top_pad = rcol_collapse_top_pad = ''

    if breakpoint == '-':
        breakpoint = ''
        lcol_horizontal_padding = f' pr-{horizontal_padding}'
        rcol_horizontal_padding = f' pl-{horizontal_padding}'
        divider = ' divider-right' if value['vertical_border'] else ''
    else:
        lcol_horizontal_padding = f' pr{breakpoint}-{horizontal_padding}'
        rcol_horizontal_padding = f' pl{breakpoint}-{horizontal_padding}'
        divider = ' divider-right' + breakpoint if value['vertical_border'] else ''
        
        if value['order'] == 'right-first':
            left_order = f' order-3 order{breakpoint}-1'
            right_order = ' order-2'
            lcol_collapse_top_pad = f' pt-3 pt{breakpoint}-0'
        else:
            left_order = ''
            right_order = ''
            rcol_collapse_top_pad = f' pt-3 pt{breakpoint}-0'

        hide_left = hide_right = ''
        if value['hide'] == 'hide-right':
            hide_right = ' d-none d' + breakpoint + '-block'
        elif value['hide'] == 'hide-left':
            hide_left = ' d-none d' + breakpoint + '-block'

    left_col = f'col{breakpoint}{("-" + left) if left else ""}'
    right_col = f'col{breakpoint}{("-" + right) if right else ""}'

    return {
        'left': f'{left_col}{lcol_horizontal_padding}{left_order}{hide_left}{divider}{lcol_collapse_top_pad}',
        'right': f'{right_col}{rcol_horizontal_padding}{right_order}{hide_right}{rcol_collapse_top_pad}'
    }
    
@register.simple_tag()
def three_column_layout(value):
    left, centre, right = value['column_layout'].split('-') 
    breakpoint = value['breakpoint']
    horizontal_padding = str(value['horizontal_padding'])
 
    if breakpoint == '-':
        breakpoint = ''
        lcol_horizontal_padding = f' pr-{horizontal_padding}'
        mcol_horizontal_padding = f' px-{horizontal_padding}'
        rcol_horizontal_padding = f' pl-{horizontal_padding}'
        divider = ' divider-right divider-left' if value['vertical_border'] else ''
        hide_sides = ''
    else:
        lcol_horizontal_padding = f' pr{breakpoint}-{horizontal_padding}'
        mcol_horizontal_padding = f' px{breakpoint}-{horizontal_padding}'
        rcol_horizontal_padding = f' pl{breakpoint}-{horizontal_padding}'
        divider = f' divider-right{breakpoint} divider-left{breakpoint}' if value['vertical_border'] else ''
        hide_sides = f' d-none d{breakpoint}-block' if value['hide'] == 'hide-sides' else ''

    left_col = f'col{breakpoint}{("-" + left) if left else ""}'
    centre_col = f'col{breakpoint}{("-" + centre) if left else ""}'
    right_col = f'col{breakpoint}{("-" + right) if left else ""}'

    return {
        'left': f'{left_col}{lcol_horizontal_padding}{hide_sides}',
        'centre': f'{centre_col}{mcol_horizontal_padding}{divider}',
        'right': f'{right_col}{rcol_horizontal_padding}{hide_sides}',
    }

