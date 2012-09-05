__author__ = 'mguillech'
import os
from django.template.loader_tags import register

@register.filter
def basename(path):
    return os.path.basename(str(path))
