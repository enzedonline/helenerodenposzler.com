import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail.features import InlineStyleFeature


def register_inline_styling(
    features,
    feature_name,
    description,
    type_,
    tag='span',
    format=None,
    editor_style=None,
    label=None,
    icon=None
):
    control = {"type": type_, "description": description}
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style

    if not format:
        style_map = {"element": tag}
        markup_map = tag
    else:
        style_map = f'{tag} {format}'
        markup_map = f'{tag}[{format}]'

    features.register_editor_plugin(
        "draftail", feature_name, InlineStyleFeature(control)
    )
    db_conversion = {
        "from_database_format": {markup_map: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: style_map}},
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)


def register_block_feature(
    features,
    feature_name,
    type_,
    description,
    css_class,
    element="div",
    label=None,
    icon=None,
    editor_style=None,
):
    control = {
        "type": type_,
        "description": description,
        "element": element,
    }
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(control, css={"all": ["draftail-editor.css"]}),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                f"{element}[class={css_class}]": BlockElementHandler(type_)
            },
            "to_database_format": {
                "block_map": {
                    type_: {"element": element, "props": {"class": css_class}}
                }
            },
        },
    )


# --------------------------------------------------------------------------------------------------
# SVG icons
# --------------------------------------------------------------------------------------------------

class DRAFTAIL_ICONS:

    underline = [
        "m 38.444913,116.09067 c 0,-38.152504 32.572641,-68.976279 72.889827,-68.976279 h 218.66948 c 40.31718,\
        0 72.88982,30.823775 72.88982,68.976279 0,38.15251 -32.57264,68.97628 -72.88982,\
        68.97628 H 293.5593 v 275.90512 c 0,114.24194 97.94571,206.92882 218.66948,206.92882 120.72378,\
        0 218.66948,-92.68688 218.66948,-206.92882 V 185.06695 h -36.44491 c -40.31719,0 -72.88983,\
        -30.82377 -72.88983,-68.97628 0,-38.152504 32.57264,-68.976279 72.88983,-68.976279 h 218.66948 c 40.31718,\
        0 72.88982,30.823775 72.88982,68.976279 0,38.15251 -32.57264,68.97628 -72.88982,\
        68.97628 h -36.44492 v 275.90512 c 0,190.54696 -163.09098,344.88138 -364.44913,344.88138 -201.35814,\
        0 -364.44913,-154.33442 -364.44913,-344.88138 V 185.06695 h -36.44491 c -40.317186,0 -72.889827,\
        -30.82377 -72.889827,-68.97628 z M 2,943.80601 C 2,905.6535 34.572641,874.82973 74.889826,\
        874.82973 H 949.56774 c 40.31718,0 72.88986,30.82377 72.88986,68.97628 0,38.1525 -32.57268,\
        68.97629 -72.88986,68.97629 H 74.889826 C 34.572641,1012.7823 2,981.95851 2,943.80601 Z"
    ]
    
    decrease_font = [
        "m 431.77869,370.57963 4.20832,6.44496 3.52572,7.20318 231.02312,554.45552 c 13.0862,31.40688 -1.76563,\
         67.47571 -33.17258,80.56191 -29.16349,12.1514 -62.34679,0.2156 -77.41597,-26.70007 L 556.80126,\
         986.0726 495.56947,839.16561 H 269.65966 L 208.48948,986.0726 c -12.15148,29.1636 -44.11958,\
         44.0526 -73.77058,35.5533 l -6.79133,-2.3807 C 98.764017,1007.0937 83.874965,975.12562 92.374306,\
         945.47457 l 2.380709,-6.79128 231.023125,-554.45552 c 18.95572,-45.49378 78.85589,-50.04316 106.00055,\
         -13.64814 z m -49.13332,197.51885 -61.60616,147.8548 h 123.21233 z m 546.85804,-447.4609 c 12.83909,\
         19.32142 9.2291,44.77907 -7.50154,59.85889 l -5.40964,4.19612 -138.67597,92.1504 c -13.55668,\
         9.00856 -30.68387,10.13463 -45.13335,3.37819 l -6.01048,-3.37821 -138.67592,-92.1504 C 566.84294,\
         170.56954 561.0625,141.89114 575.18553,120.63758 588.02462,101.31616 612.893,94.782442 633.27651,\
         104.36501 l 5.96409,3.3616 113.10337,75.08691 113.10443,-75.08692 c 21.25357,-14.123023 49.93198,\
         -8.342584 64.05501,12.91098 z"
    ]
    
    increase_font = [
        "m 480.2209,84.950689 4.06109,6.54669 3.20118,6.93067 331.19841,843.325311 c 12.1572,30.95579 -3.08196,\
        65.90574 -34.03775,78.06294 -28.74458,11.2889 -60.93322,-1.0447 -75.11868,-27.64918 L 706.58049,\
        985.7786 626.83948,782.77723 H 235.96515 l -79.6808,203.00137 c -11.28884,28.7446 -42.23062,\
        43.9377 -71.378178,36.2277 l -6.684746,-2.19 C 49.476807,1008.5275 34.283682,977.58572 41.993644,\
        948.43815 l 2.19004,-6.68479 L 375.38209,98.428049 C 393.4324,52.466792 453.88195,47.974339 480.2209,\
        84.950689 Z M 431.43242,285.07636 283.23619,662.34145 H 579.56843 Z M 773.67972,4.2455454 c 12.10621,\
        -5.6607226 26.13529,-5.6607226 38.24143,0 l 5.87486,3.3021083 135.55096,90.0738253 5.28773,4.101561 c 16.35361,\
        14.74 19.88226,39.62397 7.33249,58.50999 -12.54977,18.88602 -36.85775,25.2725 -56.78192,15.90587 l -5.82963,\
        -3.28588 -110.55565,-73.445424 -110.55475,73.445424 -5.82958,3.28584 c -19.92417,9.36663 -44.23214,\
        2.98015 -56.78191,-15.90587 -12.54983,-18.88602 -9.02113,-43.76999 7.33243,-58.50999 L 632.25391,\
        97.621437 767.8048,7.5476115 Z"
    ]

