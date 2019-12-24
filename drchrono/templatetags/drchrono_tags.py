from django.template.defaulttags import register


@register.inclusion_tag('drchrono/templatetags/form_errors.html')
def form_errors(form):
    return {'form': form}
