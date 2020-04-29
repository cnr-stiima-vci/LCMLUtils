from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
   return TemplateResponse(request, 'lcmlutils/index.html', {})

def code(request):
   return TemplateResponse(request, 'lcmlutils/code.html', {})