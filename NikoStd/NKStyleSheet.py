def build(selector=None, **kwargs):

    css_content = ""
    for attr in kwargs.keys():
        attr_parsed = attr.replace("_", "-")
        css_content += "%s:%s;" % (attr_parsed, kwargs[attr])

    if selector is not None:
        css_str = "{%s %s}" % (selector, css_content)
    else:
        css_str = "{%s}" % css_content

    return css_str
