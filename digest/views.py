# -*- coding: utf-8 -*-
# Create your views here.
from concurrency.views import ConflictResponse
from django.template import loader
from django.template.context import RequestContext

def conflict(request, target=None, template_name='409.html'):
    template = loader.get_template(template_name)
    message = 'Вот не задача, кажется эту новость обновили раньше =( \
            Нужно обновить новость для того чтобы внести правки.'
    ctx = RequestContext(request, {'message': message})
    return ConflictResponse(template.render(ctx))
